from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class InventoryLog(Base):
    """Audit log for inventory changes."""

    __tablename__ = "inventory_logs"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    product_variant_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("product_variants.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
        nullable=False,
    )
    change_type: Mapped[str] = mapped_column(nullable=False)  # purchase, sale, return, manual_adjustment
    quantity_change: Mapped[int] = mapped_column(nullable=False)  # Can be negative
    reference_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<InventoryLog(id={self.id}, variant_id={self.product_variant_id}, change_type={self.change_type}, qty={self.quantity_change})>"
