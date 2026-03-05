from typing import Optional
from pydantic import BaseModel, Field
from typing_extensions import Literal


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    base_price: float = Field(..., gt=0)
    gender: Optional[Literal["men", "women", "kids", "unisex"]]
    brand_id: Optional[str] = None
    category_id: Optional[str] = None
    is_active: bool = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[float] = Field(None, gt=0)
    gender: Optional[Literal["men", "women", "kids", "unisex"]]
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
    created_at: str

    model_config = {"from_attributes": True}
