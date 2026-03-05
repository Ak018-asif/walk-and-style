from datetime import datetime
from pydantic import BaseModel


class InventoryLogSchema(BaseModel):
    id: str
    product_variant_id: str
    change_type: str
    quantity_change: int
    reference_id: str | None
    created_at: datetime

    class Config:
        orm_mode = True


class InventoryLogCreateSchema(BaseModel):
    product_variant_id: str
    change_type: str
    quantity_change: int
    reference_id: str | None = None
