from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.modules.products.model import Product
from app.modules.variants.model import ProductVariant


class ProductService:
    @staticmethod
    async def create(db: AsyncSession, data: Product) -> Product:
        product = Product(**data.model_dump())
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def get_all(db: AsyncSession, gender: str | None = None,
                      category_id: str | None = None, brand_id: str | None = None,
                      skip: int = 0, limit: int = 20) -> list[Product]:
        query = select(Product).where(Product.is_active == True)
        if gender:
            query = query.where(Product.gender == gender)
        if category_id:
            query = query.where(Product.category_id == category_id)
        if brand_id:
            query = query.where(Product.brand_id == brand_id)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, product_id: str) -> Product:
        query = select(Product).where(Product.id == product_id).options(
            selectinload(Product.variants).selectinload(ProductVariant.images)
        )
        result = await db.execute(query)
        product = result.scalar_one_or_none()
        if not product:
            raise ValueError("Product not found")
        return product

    @staticmethod
    async def update(db: AsyncSession, product_id: str, data: dict) -> Product:
        product = await ProductService.get_by_id(db, product_id)
        for key, value in data.items():
            if value is not None:
                setattr(product, key, value)
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def delete(db: AsyncSession, product_id: str) -> None:
        product = await ProductService.get_by_id(db, product_id)
        product.is_active = False
        await db.commit()
