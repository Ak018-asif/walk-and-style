from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class InventoryLogCreate(BaseModel):
    """Schema for creating an inventory log."""

    product_variant_id: str
    change_type: Literal["purchase", "sale", "return", "manual_adjustment"]
    quantity_change: int
    reference_id: Optional[str] = None


class InventoryLogResponse(BaseModel):
    """Schema for inventory log response."""

    id: str
    product_variant_id: str
    change_type: str
    quantity_change: int
    reference_id: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
