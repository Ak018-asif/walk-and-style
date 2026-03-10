import datetime
import random
import string
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.orders.model import Order, OrderItem
from app.modules.orders.schema import OrderCreate


def _generate_order_number() -> str:
    """Generate a unique order number: WNS-YYYYMMDD-XXXX"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    random_suffix = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=4)
    )
    return f"WNS-{timestamp}-{random_suffix}"


class OrderService:
    @staticmethod
    async def create(
        db: AsyncSession, user_id: str, data: OrderCreate
    ) -> Order:
        """Create a new order with items."""
        # Import locally to avoid circular imports
        from app.modules.products.model import Product
        from app.modules.variants.model import ProductVariant

        # STEP 1: Validate all items before any write
        resolved = []
        for item in data.items:
            variant_id = item.product_variant_id
            qty = item.quantity

            # Fetch variant
            result = await db.execute(
                select(ProductVariant).where(
                    (ProductVariant.id == variant_id)
                    & (ProductVariant.is_active == True)
                )
            )
            variant = result.scalar_one_or_none()
            if not variant:
                raise ValueError(f"Variant {variant_id} not found or inactive")

            # Check stock
            if variant.stock_quantity < qty:
                raise ValueError(
                    f"Insufficient stock for {variant.sku}. "
                    f"Requested: {qty}, Available: {variant.stock_quantity}"
                )

            # Resolve price
            if variant.price_override:
                price = float(variant.price_override)
            else:
                result = await db.execute(
                    select(Product).where(Product.id == variant.product_id)
                )
                product = result.scalar_one_or_none()
                price = float(product.base_price) if product else 0

            resolved.append(
                {"variant": variant, "product": product, "qty": qty, "price": price}
            )

        # STEP 2: Calculate total
        total = sum(r["qty"] * r["price"] for r in resolved)

        # STEP 3: Create Order (without committing yet)
        order = Order(
            order_number=_generate_order_number(),
            user_id=user_id,
            shipping_address_id=data.shipping_address_id,
            total_amount=total,
            status="pending",
        )
        db.add(order)
        await db.flush()  # Get order.id without committing

        # STEP 4: Create OrderItems and adjust stock
        for r in resolved:
            variant = r["variant"]
            qty = r["qty"]
            price = r["price"]

            # Create order item
            order_item = OrderItem(
                order_id=order.id,
                product_variant_id=variant.id,
                quantity=qty,
                price_at_purchase=price,
            )
            db.add(order_item)

            # Adjust stock
            variant.stock_quantity -= qty

            # Create inventory log
            from app.modules.inventory.model import InventoryLog

            inventory_log = InventoryLog(
                product_variant_id=variant.id,
                change_type="sale",
                quantity_change=-qty,
                reference_id=order.id,
            )
            db.add(inventory_log)

        # STEP 5: Commit
        await db.commit()

        # STEP 6: Refresh with selectinload
        result = await db.execute(
            select(Order).where(Order.id == order.id).options(selectinload(Order.items))
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        db: AsyncSession, skip: int = 0, limit: int = 50
    ) -> list[Order]:
        """Get all orders."""
        query = (
            select(Order)
            .options(selectinload(Order.items))
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_user(db: AsyncSession, user_id: str) -> list[Order]:
        """Get orders for a user."""
        query = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items))
            .order_by(Order.created_at.desc())
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, order_id: str, user_id: str) -> Order:
        """Get order by ID."""
        result = await db.execute(
            select(Order).where(Order.id == order_id).options(selectinload(Order.items))
        )
        order = result.scalar_one_or_none()
        if not order:
            raise ValueError("Order not found")
        if order.user_id != user_id:
            raise ValueError("Order not found")
        return order

    @staticmethod
    async def update_status(db: AsyncSession, order_id: str, status: str) -> Order:
        """Update order status."""
        result = await db.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if not order:
            raise ValueError("Order not found")
        order.status = status
        await db.commit()
        await db.refresh(order)
        return order

    @staticmethod
    async def cancel(db: AsyncSession, order_id: str, user_id: str) -> Order:
        """Cancel an order and restore stock."""
        order = await OrderService.get_by_id(db, order_id, user_id)

        # Check cancelable status
        if order.status not in ("pending", "confirmed"):
            raise ValueError(f"Cannot cancel order with status {order.status}")

        # Restore stock and create return logs
        from app.modules.inventory.model import InventoryLog

        for item in order.items:
            variant = item.variant
            if variant:
                variant.stock_quantity += item.quantity

                # Create return log
                log = InventoryLog(
                    product_variant_id=variant.id,
                    change_type="return",
                    quantity_change=item.quantity,
                    reference_id=order.id,
                )
                db.add(log)

        order.status = "cancelled"
        await db.commit()
        return order
