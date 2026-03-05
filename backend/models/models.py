import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    String,
    Text,
    Numeric,
    Integer,
    ForeignKey,
    Enum,
    CheckConstraint,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database import Base


def _uuid() -> str:
    """Generate UUID as string."""
    return str(uuid.uuid4())


# Reference existing PostgreSQL ENUMs
GenderEnum = Enum(
    "men", "women", "kids", "unisex", name="gender_type", create_type=False
)
OrderStatusEnum = Enum(
    "pending",
    "confirmed",
    "shipped",
    "delivered",
    "cancelled",
    name="order_status",
    create_type=False,
)
PaymentStatusEnum = Enum(
    "pending", "success", "failed", name="payment_status", create_type=False
)
PaymentMethodEnum = Enum(
    "upi", "card", "cod", name="payment_method", create_type=False
)
InventoryChangeEnum = Enum(
    "purchase",
    "sale",
    "return",
    "manual_adjustment",
    name="inventory_change_type",
    create_type=False,
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    full_name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    addresses: Mapped[list["Address"]] = relationship(
        back_populates="user", lazy="raise", cascade="all, delete-orphan"
    )
    orders: Mapped[list["Order"]] = relationship(
        back_populates="user", lazy="raise", cascade="all, delete-orphan"
    )


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    address_line1: Mapped[str] = mapped_column(String(255))
    address_line2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(100))
    pincode: Mapped[str] = mapped_column(String(20))
    country: Mapped[str] = mapped_column(String(100), default="India")
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    user: Mapped[User] = relationship(back_populates="addresses", lazy="raise")
    orders: Mapped[list["Order"]] = relationship(
        back_populates="shipping_address", lazy="raise"
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    parent_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False), ForeignKey("categories.id"), nullable=True, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Self-referential relationships
    parent: Mapped["Category | None"] = relationship(
        "Category",
        remote_side=[id],
        back_populates="children",
        lazy="raise",
        foreign_keys=[parent_id],
    )
    children: Mapped[list["Category"]] = relationship(
        back_populates="parent", lazy="raise", cascade="all, delete-orphan"
    )
    products: Mapped[list["Product"]] = relationship(
        back_populates="category", lazy="raise"
    )


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    products: Mapped[list["Product"]] = relationship(
        back_populates="brand", lazy="raise"
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    name: Mapped[str] = mapped_column(String(150), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    base_price: Mapped[float] = mapped_column(Numeric(10, 2))
    gender: Mapped[str | None] = mapped_column(GenderEnum, nullable=True, index=True)
    brand_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("brands.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    category_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    brand: Mapped[Brand | None] = relationship(back_populates="products", lazy="raise")
    category: Mapped[Category | None] = relationship(
        back_populates="products", lazy="raise"
    )
    variants: Mapped[list["ProductVariant"]] = relationship(
        back_populates="product", lazy="raise", cascade="all, delete-orphan"
    )


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    product_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("products.id", ondelete="CASCADE"),
        index=True,
    )
    sku: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    size: Mapped[str] = mapped_column(String(20))
    color: Mapped[str] = mapped_column(String(50))
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)
    price_override: Mapped[float | None] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

    __table_args__ = (CheckConstraint("stock_quantity >= 0", name="ck_stock_qty"),)

    # Relationships
    product: Mapped[Product] = relationship(back_populates="variants", lazy="raise")
    images: Mapped[list["ProductImage"]] = relationship(
        back_populates="variant", lazy="raise", cascade="all, delete-orphan"
    )
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="variant", lazy="raise"
    )
    inventory_logs: Mapped[list["InventoryLog"]] = relationship(
        back_populates="variant", lazy="raise", cascade="all, delete-orphan"
    )


class ProductImage(Base):
    __tablename__ = "product_images"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    product_variant_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("product_variants.id", ondelete="CASCADE"),
        index=True,
    )
    image_url: Mapped[str] = mapped_column(Text)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    variant: Mapped[ProductVariant] = relationship(back_populates="images", lazy="raise")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    order_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    user_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    shipping_address_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("addresses.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(OrderStatusEnum, default="pending", index=True)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    user: Mapped[User | None] = relationship(back_populates="orders", lazy="raise")
    shipping_address: Mapped[Address | None] = relationship(
        back_populates="orders", lazy="raise"
    )
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", lazy="raise", cascade="all, delete-orphan"
    )
    payment: Mapped["Payment | None"] = relationship(
        back_populates="order", lazy="raise", uselist=False, cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    order_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("orders.id", ondelete="CASCADE"), index=True
    )
    product_variant_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("product_variants.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    quantity: Mapped[int] = mapped_column(Integer)
    price_at_purchase: Mapped[float] = mapped_column(Numeric(10, 2))

    __table_args__ = (CheckConstraint("quantity > 0", name="ck_order_item_qty"),)

    # Relationships
    order: Mapped[Order] = relationship(back_populates="items", lazy="raise")
    variant: Mapped[ProductVariant | None] = relationship(
        back_populates="order_items", lazy="raise"
    )


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    order_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("orders.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )
    payment_method: Mapped[str] = mapped_column(PaymentMethodEnum)
    payment_status: Mapped[str] = mapped_column(PaymentStatusEnum, default="pending")
    transaction_id: Mapped[str | None] = mapped_column(String(150), nullable=True)
    paid_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    order: Mapped[Order] = relationship(back_populates="payment", lazy="raise")


class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    product_variant_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("product_variants.id", ondelete="CASCADE"),
        index=True,
    )
    change_type: Mapped[str] = mapped_column(InventoryChangeEnum)
    quantity_change: Mapped[int] = mapped_column(Integer)
    reference_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    variant: Mapped[ProductVariant] = relationship(
        back_populates="inventory_logs", lazy="raise"
    )
