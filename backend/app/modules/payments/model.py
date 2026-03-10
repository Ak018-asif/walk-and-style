from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Payment(Base):
    """Payment table for orders."""

    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    order_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("orders.id", ondelete="CASCADE", onupdate="CASCADE"),
        unique=True,
        index=True,
        nullable=False,
    )
    payment_method: Mapped[str] = mapped_column(nullable=False)  # upi, card, cod
    payment_status: Mapped[str] = mapped_column(nullable=False, default="pending")  # pending, success, failed
    transaction_id: Mapped[Optional[str]] = mapped_column(nullable=True, unique=True)
    paid_amount: Mapped[float] = mapped_column(nullable=False)
    paid_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False, index=True)

    # Relationships
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="payment",
        lazy="selectin",
        foreign_keys=[order_id],
    )

    def __repr__(self) -> str:
        return f"<Payment(id={self.id}, order_id={self.order_id}, status={self.payment_status})>"
