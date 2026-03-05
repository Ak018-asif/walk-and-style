import uuid
from sqlalchemy import (
    String,
    Integer,
    Numeric,
    Boolean,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    product_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("products.id", ondelete="CASCADE"), index=True)
    sku: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    size: Mapped[str] = mapped_column(String(20))
    color: Mapped[str] = mapped_column(String(50))
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)
    price_override: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    __table_args__ = (CheckConstraint("stock_quantity >= 0", name="ck_stock_qty"),)

    # relationships
    product: Mapped["Product"] = relationship("Product", back_populates="variants", lazy="raise")
    images: Mapped[list["ProductImage"]] = relationship(
        "ProductImage", back_populates="variant", lazy="raise", cascade="all, delete-orphan"
    )
    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="variant", lazy="raise")
    inventory_logs: Mapped[list["InventoryLog"]] = relationship(
        "InventoryLog", back_populates="variant", lazy="raise", cascade="all, delete-orphan"
    )
