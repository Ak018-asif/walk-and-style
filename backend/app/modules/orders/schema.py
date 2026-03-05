from typing import Optional
from pydantic import BaseModel, Field
from typing_extensions import Literal


class OrderItemCreate(BaseModel):
    product_variant_id: str
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    shipping_address_id: str
    items: list[OrderItemCreate] = Field(..., min_length=1)


class OrderStatusUpdate(BaseModel):
    status: Literal["pending", "confirmed", "shipped", "delivered", "cancelled"]


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
    created_at: str
    items: list[OrderItemResponse] = []

    model_config = {"from_attributes": True}


class OrderListResponse(BaseModel):
    orders: list[OrderResponse]

    model_config = {"from_attributes": True}
