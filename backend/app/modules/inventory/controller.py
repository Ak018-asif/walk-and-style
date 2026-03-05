from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.schema import InventoryLogCreateSchema, InventoryLogSchema
from app.modules.inventory.service import InventoryService
from core.dependencies import get_db, get_current_user
from models.models import User

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.post("/log", response_model=InventoryLogSchema)
async def log_inventory(
    log_data: InventoryLogCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Only admins should normally perform inventory adjustments
    try:
        log = await InventoryService.create_log(
            db,
            product_variant_id=log_data.product_variant_id,
            change_type=log_data.change_type,
            quantity_change=log_data.quantity_change,
            reference_id=log_data.reference_id,
        )
        return log
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/variant/{variant_id}", response_model=list[InventoryLogSchema])
async def get_variant_logs(
    variant_id: str,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    logs = await InventoryService.get_for_variant(db, variant_id, skip, limit)
    return logs


@router.get("/", response_model=list[InventoryLogSchema])
async def get_all_logs(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    return await InventoryService.get_all(db, skip, limit)
