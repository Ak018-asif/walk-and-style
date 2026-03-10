from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.model import InventoryLog
from app.modules.inventory.schema import InventoryLogCreate


class InventoryService:
    """Service for inventory log operations (audit-only, no update/delete)."""

    @staticmethod
    async def create(db: AsyncSession, data: InventoryLogCreate) -> InventoryLog:
        """Create a new inventory log entry."""
        # Verify variant exists
        from app.modules.variants.model import ProductVariant

        result = await db.execute(select(ProductVariant).where(ProductVariant.id == data.product_variant_id))
        variant = result.scalar_one_or_none()
        if not variant:
            raise ValueError("Product variant not found")

        # Create log
        log = InventoryLog(
            product_variant_id=data.product_variant_id,
            change_type=data.change_type,
            quantity_change=data.quantity_change,
            reference_id=data.reference_id,
        )
        db.add(log)
        await db.commit()
        await db.refresh(log)
        return log

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 50) -> list[InventoryLog]:
        """Get all inventory logs."""
        result = await db.execute(
            select(InventoryLog).order_by(InventoryLog.created_at.desc()).offset(skip).limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, log_id: str) -> InventoryLog:
        """Get a specific inventory log."""
        result = await db.execute(select(InventoryLog).where(InventoryLog.id == log_id))
        log = result.scalar_one_or_none()
        if not log:
            raise ValueError("Inventory log not found")
        return log

    @staticmethod
    async def get_by_variant(
        db: AsyncSession,
        variant_id: str,
        skip: int = 0,
        limit: int = 50,
    ) -> list[InventoryLog]:
        """Get inventory logs for a specific variant."""
        result = await db.execute(
            select(InventoryLog)
            .where(InventoryLog.product_variant_id == variant_id)
            .order_by(InventoryLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
