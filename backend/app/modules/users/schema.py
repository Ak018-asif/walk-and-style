from typing import Optional
from pydantic import BaseModel


class AddressCreate(BaseModel):
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    pincode: str
    country: str = "India"
    is_default: bool = False


class AddressUpdate(BaseModel):
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    country: Optional[str] = None
    is_default: Optional[bool] = None


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
