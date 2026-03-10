from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.modules.auth.model import User
from app.modules.inventory.schema import (
    InventoryLogCreate,
    InventoryLogResponse,
)
from app.modules.inventory.service import InventoryService

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.post("/log", response_model=InventoryLogResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory_log(
    data: InventoryLogCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Create a new inventory log entry (auth required)."""
    try:
        return await InventoryService.create(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/log", response_model=list[InventoryLogResponse])
async def get_all_inventory_logs(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Get all inventory logs (auth required)."""
    return await InventoryService.get_all(db, skip, limit)


@router.get("/log/{log_id}", response_model=InventoryLogResponse)
async def get_inventory_log(
    log_id: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Get a specific inventory log (auth required)."""
    try:
        return await InventoryService.get_by_id(db, log_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/variant/{variant_id}", response_model=list[InventoryLogResponse])
async def get_variant_inventory_logs(
    variant_id: str,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Get inventory logs for a specific variant (auth required)."""
    return await InventoryService.get_by_variant(db, variant_id, skip, limit)
