import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def _uuid() -> str:
    return str(uuid.uuid4())


GenderEnum = Enum(
    "men", "women", "kids", "unisex", name="gender_type", create_type=False
)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    base_price: Mapped[float] = mapped_column(Numeric(10, 2))
    gender: Mapped[str | None] = mapped_column(GenderEnum, nullable=True, index=True)
    brand_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False), ForeignKey("brands.id", ondelete="SET NULL"), nullable=True, index=True
    )
    category_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()")

    # relationships
    # use a single quoted union string for forward references
    brand: Mapped["Brand | None"] = relationship("Brand", back_populates="products", lazy="raise")
    category: Mapped["Category | None"] = relationship("Category", back_populates="products", lazy="raise")
    variants: Mapped[list["ProductVariant"]] = relationship(
        "ProductVariant", back_populates="product", lazy="raise", cascade="all, delete-orphan"
    )
