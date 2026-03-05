from typing import Optional
from pydantic import BaseModel


class ImageCreate(BaseModel):
    image_url: str
    is_primary: bool = False


class ImageUpdate(BaseModel):
    image_url: Optional[str] = None
    is_primary: Optional[bool] = None


class ImageResponse(BaseModel):
    id: str
    product_variant_id: str
    image_url: str
    is_primary: bool

    model_config = {"from_attributes": True}
