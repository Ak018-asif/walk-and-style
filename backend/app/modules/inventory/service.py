from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.inventory.model import InventoryLog


class InventoryService:
    @staticmethod
    async def create_log(
        db: AsyncSession,
        product_variant_id: str,
        change_type: str,
        quantity_change: int,
        reference_id: str | None = None,
    ) -> InventoryLog:
        log = InventoryLog(
            product_variant_id=product_variant_id,
            change_type=change_type,
            quantity_change=quantity_change,
            reference_id=reference_id,
        )
        db.add(log)
        await db.commit()
        await db.refresh(log)
        return log

    @staticmethod
    async def get_for_variant(
        db: AsyncSession, product_variant_id: str, skip: int = 0, limit: int = 20
    ) -> list[InventoryLog]:
        query = (
            select(InventoryLog)
            .where(InventoryLog.product_variant_id == product_variant_id)
            .order_by(InventoryLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 50) -> list[InventoryLog]:
        query = (
            select(InventoryLog)
            .order_by(InventoryLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
