from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from core.dependencies import get_current_user
from models.models import User, Address
from schemas.schemas import AddressCreate, AddressResponse

router = APIRouter(tags=["User"])


@router.post("/users/me/addresses", response_model=AddressResponse, status_code=201)
async def create_address(
    body: AddressCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new address for the current user."""
    address = Address(
        user_id=current_user.id,
        address_line1=body.address_line1,
        address_line2=body.address_line2,
        city=body.city,
        state=body.state,
        pincode=body.pincode,
        country=body.country,
        is_default=body.is_default,
    )
    db.add(address)
    await db.commit()
    await db.refresh(address)
    return address


@router.get("/users/me/addresses", response_model=list[AddressResponse])
async def get_user_addresses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all addresses for the current user."""
    result = await db.execute(
        select(Address).where(Address.user_id == current_user.id)
    )
    return result.scalars().all()


@router.delete("/users/me/addresses/{address_id}", status_code=204)
async def delete_address(
    address_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete an address."""
    result = await db.execute(
        select(Address).where(
            (Address.id == address_id) & (Address.user_id == current_user.id)
        )
    )
    address = result.scalar_one_or_none()
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    await db.delete(address)
    await db.commit()
