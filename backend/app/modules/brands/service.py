from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.brands.model import Brand


class BrandService:
    @staticmethod
    async def create(db: AsyncSession, data: Brand) -> Brand:
        # name uniqueness
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
        query = select(Brand)
        if active_only:
            query = query.where(Brand.is_active == True)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, brand_id: str) -> Brand:
        result = await db.execute(select(Brand).where(Brand.id == brand_id))
        brand = result.scalar_one_or_none()
        if not brand:
            raise ValueError("Brand not found")
        return brand

    @staticmethod
    async def update(db: AsyncSession, brand_id: str, data: dict) -> Brand:
        brand = await BrandService.get_by_id(db, brand_id)
        # if name changing, check uniqueness
        if data.get("name") and data["name"] != brand.name:
            result = await db.execute(select(Brand).where(Brand.name == data["name"]))
            if result.scalar_one_or_none():
                raise ValueError("Brand name already exists")
        for key, value in data.items():
            if value is not None:
                setattr(brand, key, value)
        await db.commit()
        await db.refresh(brand)
        return brand

    @staticmethod
    async def delete(db: AsyncSession, brand_id: str) -> None:
        brand = await BrandService.get_by_id(db, brand_id)
        brand.is_active = False
        await db.commit()
