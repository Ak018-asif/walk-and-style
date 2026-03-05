from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from core.dependencies import get_current_user
from app.modules.users.schema import (
    AddressCreate,
    AddressUpdate,
    AddressResponse,
)
from app.modules.users.model import Address
from app.modules.users.service import AddressService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/me/addresses", response_model=AddressResponse, status_code=201)
async def create_address(
    body: AddressCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        address = await AddressService.create(db, current_user.id, Address(**body.model_dump()))
        return address
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/me/addresses", response_model=list[AddressResponse])
async def get_addresses(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await AddressService.get_by_user(db, current_user.id)


@router.get("/me/addresses/{address_id}", response_model=AddressResponse)
async def get_address(
    address_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return await AddressService.get_by_id(db, address_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/me/addresses/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: str,
    body: AddressUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        data = body.model_dump(exclude_none=True)
        return await AddressService.update(db, address_id, current_user.id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/me/addresses/{address_id}", status_code=204)
async def delete_address(
    address_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        await AddressService.delete(db, address_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
