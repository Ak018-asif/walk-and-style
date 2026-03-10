from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class PaymentCreate(BaseModel):
    """Schema for creating a payment."""

    payment_method: Literal["upi", "card", "cod"]
    transaction_id: Optional[str] = None
    paid_amount: float = Field(gt=0)


class PaymentUpdate(BaseModel):
    """Schema for updating a payment."""

    payment_method: Optional[Literal["upi", "card", "cod"]] = None
    transaction_id: Optional[str] = None
    paid_amount: Optional[float] = Field(None, gt=0)
    payment_status: Optional[Literal["pending", "success", "failed"]] = None


class PaymentResponse(BaseModel):
    """Schema for payment response."""

    id: str
    order_id: str
    payment_method: str
    payment_status: str
    transaction_id: Optional[str]
    paid_amount: float
    paid_at: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}
