from typing import Optional
from pydantic import BaseModel, Field


class BrandCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    is_active: bool = True


class BrandUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class BrandResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    is_active: bool

    model_config = {"from_attributes": True}
