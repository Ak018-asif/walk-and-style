from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# ============ AUTH SCHEMAS ============
class UserCreate(BaseModel):
    full_name: str = Field(..., max_length=150)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    password: str = Field(..., min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    phone: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ============ ADDRESS SCHEMAS ============
class AddressCreate(BaseModel):
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    pincode: str
    country: str = "India"
    is_default: bool = False


class AddressResponse(BaseModel):
    id: str
    user_id: str
    address_line1: str
    address_line2: Optional[str]
    city: str
    state: str
    pincode: str
    country: str
    is_default: bool

    model_config = {"from_attributes": True}


# ============ CATEGORY SCHEMAS ============
class CategoryCreate(BaseModel):
    name: str
    slug: str
    parent_id: Optional[str] = None
    is_active: bool = True


class CategoryResponse(BaseModel):
    id: str
    name: str
    slug: str
    parent_id: Optional[str]
    is_active: bool

    model_config = {"from_attributes": True}


# ============ BRAND SCHEMAS ============
class BrandCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True


class BrandResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    is_active: bool

    model_config = {"from_attributes": True}


# ============ PRODUCT SCHEMAS ============
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    base_price: float = Field(..., gt=0)
    gender: Optional[str] = None  # men, women, kids, unisex
    brand_id: Optional[str] = None
    category_id: Optional[str] = None
    is_active: bool = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[float] = Field(None, gt=0)
    gender: Optional[str] = None
    brand_id: Optional[str] = None
    category_id: Optional[str] = None
    is_active: Optional[bool] = None


class ProductResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    base_price: float
    gender: Optional[str]
    brand_id: Optional[str]
    category_id: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ============ VARIANT SCHEMAS ============
class VariantCreate(BaseModel):
    sku: str = Field(..., max_length=100)
    size: str = Field(..., max_length=20)
    color: str = Field(..., max_length=50)
    stock_quantity: int = Field(0, ge=0)
    price_override: Optional[float] = Field(None, gt=0)
    is_active: bool = True


class VariantUpdate(BaseModel):
    sku: Optional[str] = Field(None, max_length=100)
    size: Optional[str] = Field(None, max_length=20)
    color: Optional[str] = Field(None, max_length=50)
    stock_quantity: Optional[int] = Field(None, ge=0)
    price_override: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None


class VariantResponse(BaseModel):
    id: str
    product_id: str
    sku: str
    size: str
    color: str
    stock_quantity: int
    price_override: Optional[float]
    is_active: bool

    model_config = {"from_attributes": True}


# ============ IMAGE SCHEMAS ============
class ImageCreate(BaseModel):
    image_url: str
    is_primary: bool = False


class ImageResponse(BaseModel):
    id: str
    product_variant_id: str
    image_url: str
    is_primary: bool

    model_config = {"from_attributes": True}


# ============ ORDER SCHEMAS ============
class OrderItemCreate(BaseModel):
    product_variant_id: str
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    shipping_address_id: str
    items: list[OrderItemCreate] = Field(..., min_length=1)


class OrderItemResponse(BaseModel):
    id: str
    product_variant_id: Optional[str]
    quantity: int
    price_at_purchase: float

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: str
    order_number: str
    user_id: Optional[str]
    shipping_address_id: Optional[str]
    status: str
    total_amount: float
    created_at: datetime
    items: list[OrderItemResponse] = []

    model_config = {"from_attributes": True}


# ============ PAYMENT SCHEMAS ============
class PaymentCreate(BaseModel):
    payment_method: str  # upi, card, cod
    transaction_id: Optional[str] = None
    paid_amount: float = Field(..., gt=0)


class PaymentResponse(BaseModel):
    id: str
    order_id: str
    payment_method: str
    payment_status: str
    transaction_id: Optional[str]
    paid_amount: float
    paid_at: Optional[datetime]

    model_config = {"from_attributes": True}

