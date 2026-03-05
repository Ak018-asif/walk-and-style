import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Numeric,
    DateTime,
    ForeignKey,
    Enum,
    CheckConstraint,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

# import related models for type hints only (optional)
from models.models import User, Address, Payment
from app.modules.variants.model import ProductVariant


def _uuid() -> str:
    return str(uuid.uuid4())


OrderStatusEnum = Enum(
    "pending",
    "confirmed",
    "shipped",
    "delivered",
    "cancelled",
    name="order_status",
    create_type=False,
)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    order_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    shipping_address_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("addresses.id", ondelete="SET NULL"), nullable=True, index=True)
    status: Mapped[str] = mapped_column(OrderStatusEnum, default="pending", index=True)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()")

    # forward refs must wrap the entire union in quotes
    user: Mapped["User | None"] = relationship("User", lazy="raise")
    shipping_address: Mapped["Address | None"] = relationship("Address", lazy="raise")
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", lazy="raise", cascade="all, delete-orphan"
    )
    payment: Mapped["Payment | None"] = relationship(
        "Payment", back_populates="order", lazy="raise", uselist=False, cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    order_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    product_variant_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("product_variants.id", ondelete="SET NULL"), nullable=True, index=True)
    quantity: Mapped[int] = mapped_column(Integer)
    price_at_purchase: Mapped[float] = mapped_column(Numeric(10, 2))

    __table_args__ = (CheckConstraint("quantity > 0", name="ck_order_item_qty"),)

    order: Mapped[Order] = relationship("Order", back_populates="items", lazy="raise")
    variant: Mapped["ProductVariant | None"] = relationship("ProductVariant", lazy="raise")
