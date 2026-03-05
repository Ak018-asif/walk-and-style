import uuid
from datetime import datetime

from sqlalchemy import String, Enum, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    product_variant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("product_variants.id"), nullable=False, index=True)
    change_type: Mapped[str] = mapped_column(String(50))  # e.g. "stock_adjustment", "sale", "return"
    quantity_change: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # relationships
    variant: Mapped["ProductVariant"] = relationship("ProductVariant", back_populates="inventory_logs", lazy="raise")
