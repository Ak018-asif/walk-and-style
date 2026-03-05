import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.modules.orders.model import Order, OrderItem
from app.modules.variants.model import ProductVariant
from app.modules.products.model import Product
from app.modules.inventory.model import InventoryLog


def _generate_order_number() -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    random_suffix = str(uuid.uuid4())[:4].upper()
    return f"WNS-{timestamp}-{random_suffix}"


class OrderService:
    @staticmethod
    async def create(db: AsyncSession, user_id: str, shipping_address_id: str, items: list[dict]) -> Order:
        resolved = []
        for item in items:
            variant_id = item["product_variant_id"]
            qty = item["quantity"]
            result = await db.execute(
                select(ProductVariant).where(
                    (ProductVariant.id == variant_id) & (ProductVariant.is_active == True)
                )
            )
            variant = result.scalar_one_or_none()
            if not variant:
                raise ValueError(f"Variant {variant_id} not found")
            if variant.stock_quantity < qty:
                raise ValueError(
                    f"Insufficient stock for SKU {variant.sku}. Requested: {qty}, Available: {variant.stock_quantity}"
                )
            if variant.price_override:
                price = variant.price_override
            else:
                prod = (await db.execute(select(Product).where(Product.id == variant.product_id))).scalar_one_or_none()
                price = float(prod.base_price) if prod else 0
            resolved.append({"variant": variant, "qty": qty, "price": price})
        total = sum(r["qty"] * r["price"] for r in resolved)
        order = Order(
            order_number=_generate_order_number(),
            user_id=user_id,
            shipping_address_id=shipping_address_id,
            total_amount=total,
        )
        db.add(order)
        await db.flush()
        for r in resolved:
            var = r["variant"]
            qty = r["qty"]
            price = r["price"]
            item_obj = OrderItem(
                order_id=order.id,
                product_variant_id=var.id,
                quantity=qty,
                price_at_purchase=price,
            )
            db.add(item_obj)
            var.stock_quantity -= qty
            log = InventoryLog(
                product_variant_id=var.id,
                change_type="sale",
                quantity_change=-qty,
                reference_id=order.id,
            )
            db.add(log)
        await db.commit()
        result = await db.execute(
            select(Order).where(Order.id == order.id).options(selectinload(Order.items))
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 20) -> list[Order]:
        query = select(Order).options(selectinload(Order.items)).order_by(Order.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_user(db: AsyncSession, user_id: str) -> list[Order]:
        query = select(Order).where(Order.user_id == user_id).options(selectinload(Order.items)).order_by(Order.created_at.desc())
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, order_id: str, user_id: str) -> Order:
        result = await db.execute(
            select(Order).where(Order.id == order_id).options(selectinload(Order.items))
        )
        order = result.scalar_one_or_none()
        if not order:
            raise ValueError("Order not found")
        if order.user_id != user_id:
            raise ValueError("Order does not belong to user")
        return order

    @staticmethod
    async def update_status(db: AsyncSession, order_id: str, status: str) -> Order:
        order = (await db.execute(select(Order).where(Order.id == order_id))).scalar_one_or_none()
        if not order:
            raise ValueError("Order not found")
        order.status = status
        await db.commit()
        await db.refresh(order)
        return order

    @staticmethod
    async def cancel(db: AsyncSession, order_id: str, user_id: str) -> Order:
        order = await OrderService.get_by_id(db, order_id, user_id)
        if order.status not in ("pending", "confirmed"):
            raise ValueError(f"Cannot cancel order in {order.status} status")
        for item in order.items:
            var = item.variant
            var.stock_quantity += item.quantity
            log = InventoryLog(
                product_variant_id=var.id,
                change_type="return",
                quantity_change=item.quantity,
                reference_id=order.id,
            )
            db.add(log)
        order.status = "cancelled"
        await db.commit()
        return order
