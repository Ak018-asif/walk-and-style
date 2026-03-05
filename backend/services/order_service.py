import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.models import (
    Order,
    OrderItem,
    Payment,
    InventoryLog,
    ProductVariant,
    Product,
)


def _generate_order_number() -> str:
    """Generate unique order number: WNS-YYYYMMDD-XXXX."""
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    random_suffix = str(uuid.uuid4())[:4].upper()
    return f"WNS-{timestamp}-{random_suffix}"


class OrderService:
    """Service for Order operations."""

    @staticmethod
    async def create_order(
        db: AsyncSession,
        user_id: str,
        shipping_address_id: str,
        items: list[dict],
    ) -> Order:
        """Create a new order with validation and inventory management."""
        # STEP 1: Validate ALL items first
        resolved_items = []

        for item in items:
            product_variant_id = item["product_variant_id"]
            quantity = item["quantity"]

            # Fetch variant
            result = await db.execute(
                select(ProductVariant).where(
                    (ProductVariant.id == product_variant_id) & (ProductVariant.is_active == True)
                )
            )
            variant = result.scalar_one_or_none()
            if not variant:
                raise ValueError(f"Variant {product_variant_id} not found or inactive")

            # Check stock
            if variant.stock_quantity < quantity:
                raise ValueError(
                    f"Insufficient stock for SKU {variant.sku}. "
                    f"Requested: {quantity}, Available: {variant.stock_quantity}"
                )

            # Resolve unit price (price_override or product base_price)
            if variant.price_override:
                unit_price = variant.price_override
            else:
                result = await db.execute(select(Product).where(Product.id == variant.product_id))
                product = result.scalar_one_or_none()
                unit_price = float(product.base_price) if product else 0

            resolved_items.append({
                "variant": variant,
                "quantity": quantity,
                "unit_price": unit_price,
            })

        # STEP 2: Create Order after ALL items pass validation
        total_amount = sum(item["quantity"] * item["unit_price"] for item in resolved_items)
        order = Order(
            order_number=_generate_order_number(),
            user_id=user_id,
            shipping_address_id=shipping_address_id,
            status="pending",
            total_amount=total_amount,
        )
        db.add(order)
        await db.flush()  # Get order.id without committing

        # STEP 3: Create OrderItems and update inventory
        for item in resolved_items:
            variant = item["variant"]
            quantity = item["quantity"]
            unit_price = item["unit_price"]

            # Create OrderItem
            order_item = OrderItem(
                order_id=order.id,
                product_variant_id=variant.id,
                quantity=quantity,
                price_at_purchase=unit_price,
            )
            db.add(order_item)

            # Update stock
            variant.stock_quantity -= quantity

            # Create InventoryLog
            inventory_log = InventoryLog(
                product_variant_id=variant.id,
                change_type="sale",
                quantity_change=-quantity,
                reference_id=order.id,
            )
            db.add(inventory_log)

        # STEP 4: Commit all changes
        await db.commit()

        # STEP 5: Re-fetch order with items
        result = await db.execute(
            select(Order).where(Order.id == order.id).options(
                selectinload(Order.items)
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_orders(db: AsyncSession, user_id: str) -> list[Order]:
        """Get all orders for a user."""
        query = select(Order).where(Order.user_id == user_id).options(
            selectinload(Order.items)
        ).order_by(Order.created_at.desc())
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_order_by_id(db: AsyncSession, order_id: str, user_id: str) -> Order:
        """Get a single order with items."""
        result = await db.execute(
            select(Order).where(Order.id == order_id).options(
                selectinload(Order.items)
            )
        )
        order = result.scalar_one_or_none()
        if not order:
            raise ValueError(f"Order {order_id} not found")
        if order.user_id != user_id:
            raise ValueError("Order does not belong to this user")
        return order

    @staticmethod
    async def cancel_order(db: AsyncSession, order_id: str, user_id: str) -> Order:
        """Cancel an order and restore inventory."""
        order = await OrderService.get_order_by_id(db, order_id, user_id)

        # Check if order can be cancelled
        if order.status not in ("pending", "confirmed"):
            raise ValueError(f"Cannot cancel order in {order.status} status")

        # Restore inventory for each item
        for order_item in order.items:
            variant = order_item.variant
            variant.stock_quantity += order_item.quantity

            # Create return InventoryLog
            inventory_log = InventoryLog(
                product_variant_id=variant.id,
                change_type="return",
                quantity_change=order_item.quantity,
                reference_id=order.id,
            )
            db.add(inventory_log)

        # Cancel order
        order.status = "cancelled"
        await db.commit()
        return order


class PaymentService:
    """Service for Payment operations."""

    @staticmethod
    async def record_payment(
        db: AsyncSession,
        order_id: str,
        user_id: str,
        payment_method: str,
        transaction_id: str | None,
        paid_amount: float,
    ) -> Payment:
        """Record a payment for an order."""
        # Verify order exists and belongs to user
        result = await db.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if not order:
            raise ValueError(f"Order {order_id} not found")
        if order.user_id != user_id:
            raise ValueError("Order does not belong to this user")

        # Check if payment already exists
        result = await db.execute(select(Payment).where(Payment.order_id == order_id))
        if result.scalar_one_or_none():
            raise ValueError("Payment already recorded for this order")

        # Create Payment
        payment = Payment(
            order_id=order_id,
            payment_method=payment_method,
            payment_status="success",
            transaction_id=transaction_id,
            paid_amount=paid_amount,
            paid_at=datetime.utcnow(),
        )
        db.add(payment)

        # Update order status
        order.status = "confirmed"
        await db.commit()
        await db.refresh(payment)
        return payment
