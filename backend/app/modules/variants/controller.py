from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from core.dependencies import get_current_user
from app.modules.variants.schema import (
    VariantCreate,
    VariantUpdate,
    VariantResponse,
    StockAdjust,
)
from app.modules.variants.model import ProductVariant
from app.modules.variants.service import VariantService

router = APIRouter(tags=["Variants"])


@router.post("/products/{product_id}/variants", response_model=VariantResponse, status_code=201)
async def create_variant(
    product_id: str,
    body: VariantCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        variant = await VariantService.create(db, product_id, ProductVariant(**body.model_dump()))
        return variant
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/products/{product_id}/variants", response_model=list[VariantResponse])
async def get_variants(product_id: str, db: AsyncSession = Depends(get_db)):
    return await VariantService.get_by_product(db, product_id)


@router.get("/variants/{variant_id}", response_model=VariantResponse)
async def get_variant(variant_id: str, db: AsyncSession = Depends(get_db)):
    try:
        return await VariantService.get_by_id(db, variant_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/variants/low-stock", response_model=list[VariantResponse])
async def low_stock(threshold: int = Query(5, ge=0), db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await VariantService.get_low_stock(db, threshold)


@router.patch("/variants/{variant_id}", response_model=VariantResponse)
async def update_variant(
    variant_id: str,
    body: VariantUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        data = body.model_dump(exclude_none=True)
        return await VariantService.update(db, variant_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/variants/{variant_id}/adjust-stock", response_model=VariantResponse)
async def adjust_stock(
    variant_id: str,
    body: StockAdjust,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return await VariantService.adjust_stock(db, variant_id, body.quantity_change)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/variants/{variant_id}", status_code=204)
async def delete_variant(
    variant_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        await VariantService.delete(db, variant_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
