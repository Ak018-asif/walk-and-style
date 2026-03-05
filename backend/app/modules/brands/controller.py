from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.brands.schema import (
    BrandCreate,
    BrandUpdate,
    BrandResponse,
)
from app.modules.brands.model import Brand
from app.modules.brands.service import BrandService
from core.dependencies import get_current_user

router = APIRouter(prefix="/brands", tags=["Brands"])


@router.post("/", response_model=BrandResponse, status_code=201)
async def create_brand(
    body: BrandCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        brand = await BrandService.create(db, Brand(**body.model_dump()))
        return brand
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=list[BrandResponse])
async def get_brands(db: AsyncSession = Depends(get_db)):
    return await BrandService.get_all(db)


@router.get("/{brand_id}", response_model=BrandResponse)
async def get_brand(brand_id: str, db: AsyncSession = Depends(get_db)):
    try:
        return await BrandService.get_by_id(db, brand_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{brand_id}", response_model=BrandResponse)
async def update_brand(
    brand_id: str,
    body: BrandUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        data = body.model_dump(exclude_none=True)
        return await BrandService.update(db, brand_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{brand_id}", status_code=204)
async def delete_brand(
    brand_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        await BrandService.delete(db, brand_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
