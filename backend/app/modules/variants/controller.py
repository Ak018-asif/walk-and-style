from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.modules.auth.model import User
from app.modules.variants.schema import (
    StockAdjust,
    VariantCreate,
    VariantResponse,
    VariantUpdate,
)
from app.modules.variants.service import VariantService

router = APIRouter(tags=["Variants"])


@router.post(
    "/products/{product_id}/variants",
    response_model=VariantResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_variant(
    product_id: str,
    data: VariantCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Create a new variant for a product (auth required)."""
    try:
        return await VariantService.create(db, product_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/products/{product_id}/variants", response_model=list[VariantResponse])
async def get_variants(product_id: str, db: AsyncSession = Depends(get_db)):
    """Get all variants for a product."""
    return await VariantService.get_by_product(db, product_id)


# IMPORTANT: This route MUST come BEFORE /variants/{variant_id}
@router.get("/variants/low-stock", response_model=list[VariantResponse])
async def get_low_stock(
    threshold: int = Query(5, ge=0),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Get variants with low stock (auth required)."""
    return await VariantService.get_low_stock(db, threshold)


@router.get("/{variant_id}", response_model=VariantResponse)
async def get_variant(variant_id: str, db: AsyncSession = Depends(get_db)):
    """Get a variant by ID."""
    try:
        return await VariantService.get_by_id(db, variant_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{variant_id}", response_model=VariantResponse)
async def update_variant(
    variant_id: str,
    data: VariantUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Update a variant (auth required)."""
    try:
        return await VariantService.update(db, variant_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{variant_id}/adjust-stock", response_model=VariantResponse)
async def adjust_stock(
    variant_id: str,
    body: StockAdjust,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Adjust stock for a variant (auth required)."""
    try:
        return await VariantService.adjust_stock(db, variant_id, body.quantity_change)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{variant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_variant(
    variant_id: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Delete a variant (auth required)."""
    try:
        await VariantService.delete(db, variant_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
