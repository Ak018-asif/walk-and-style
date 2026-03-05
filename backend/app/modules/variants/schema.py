from typing import Optional
from pydantic import BaseModel, Field


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


class StockAdjust(BaseModel):
    quantity_change: int


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
