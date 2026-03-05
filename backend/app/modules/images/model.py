import uuid
from sqlalchemy import Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class ProductImage(Base):
    __tablename__ = "product_images"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    product_variant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("product_variants.id", ondelete="CASCADE"), index=True)
    image_url: Mapped[str] = mapped_column(Text)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    variant: Mapped["ProductVariant"] = relationship("ProductVariant", back_populates="images", lazy="raise")
