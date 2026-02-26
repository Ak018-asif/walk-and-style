from sqlalchemy import Column, Integer, String, Boolean, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("category.id"), nullable=True)

    # Relationships
    parent = relationship("Category", remote_side=[id], backref="children")
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    base_price = Column(Numeric(10, 2), nullable=False)

    # Relationships
    category = relationship("Category", back_populates="products")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")


class ProductVariant(Base):
    __tablename__ = "product_variant"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    size = Column(String, nullable=False)
    color = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    stock_quantity = Column(Integer, default=0)

    # Relationships
    product = relationship("Product", back_populates="variants")


class ProductImage(Base):
    __tablename__ = "product_image"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    image_url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)

    # Relationships
    product = relationship("Product", back_populates="images")
