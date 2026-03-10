from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.brands.model import Brand
from app.modules.brands.schema import BrandCreate, BrandUpdate


class BrandService:
    @staticmethod
    async def create(db: AsyncSession, data: BrandCreate) -> Brand:
        """Create a new brand."""
        # Check name uniqueness
        result = await db.execute(select(Brand).where(Brand.name == data.name))
        if result.scalar_one_or_none():
            raise ValueError("Brand name already exists")

        brand = Brand(**data.model_dump())
        db.add(brand)
        await db.commit()
        await db.refresh(brand)
        return brand

    @staticmethod
    async def get_all(db: AsyncSession, active_only: bool = True) -> list[Brand]:
        """Get all brands."""
        query = select(Brand)
        if active_only:
            query = query.where(Brand.is_active == True)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, brand_id: str) -> Brand:
        """Get brand by ID."""
        result = await db.execute(select(Brand).where(Brand.id == brand_id))
        brand = result.scalar_one_or_none()
        if not brand:
            raise ValueError("Brand not found")
        return brand

    @staticmethod
    async def update(db: AsyncSession, brand_id: str, data: BrandUpdate) -> Brand:
        """Update a brand."""
        brand = await BrandService.get_by_id(db, brand_id)

        # If name changing, check uniqueness
        if data.name and data.name != brand.name:
            result = await db.execute(select(Brand).where(Brand.name == data.name))
            if result.scalar_one_or_none():
                raise ValueError("Brand name already exists")

        for field, value in data.model_dump(exclude_none=True).items():
            setattr(brand, field, value)

        await db.commit()
        await db.refresh(brand)
        return brand

    @staticmethod
    async def delete(db: AsyncSession, brand_id: str) -> None:
        """Soft delete a brand."""
        brand = await BrandService.get_by_id(db, brand_id)
        brand.is_active = False
        await db.commit()
