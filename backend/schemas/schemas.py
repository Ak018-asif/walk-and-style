from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal

# --- Image Schemas ---
class ProductImageBase(BaseModel):
    image_url: str
    is_primary: bool = False

class ProductImageCreate(ProductImageBase):
    pass

class ProductImage(ProductImageBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True

# --- Variant Schemas ---
class ProductVariantBase(BaseModel):
    size: str
    color: str
    sku: str
    stock_quantity: int = 0

class ProductVariantCreate(ProductVariantBase):
    pass

class ProductVariant(ProductVariantBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True

# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    base_price: Decimal
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    images: List[ProductImage] = []
    variants: List[ProductVariant] = []

    class Config:
        from_attributes = True

# --- Category Schemas ---
class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    # children: List['Category'] = [] # Self-referencing can be tricky, keeping simple for now

    class Config:
        from_attributes = True
