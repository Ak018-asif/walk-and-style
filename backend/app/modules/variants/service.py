from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.variants.model import ProductVariant
from app.modules.products.model import Product


class VariantService:
    @staticmethod
    async def create(db: AsyncSession, product_id: str, data: ProductVariant) -> ProductVariant:
        # verify product exists
        result = await db.execute(select(Product).where(Product.id == product_id))
        if not result.scalar_one_or_none():
            raise ValueError("Product not found")
        # check SKU uniqueness
        result = await db.execute(select(ProductVariant).where(ProductVariant.sku == data.sku))
        if result.scalar_one_or_none():
            raise ValueError("SKU already exists")
        variant = ProductVariant(product_id=product_id, **data.model_dump())
        db.add(variant)
        await db.commit()
        await db.refresh(variant)
        return variant

    @staticmethod
    async def get_by_product(db: AsyncSession, product_id: str) -> list[ProductVariant]:
        query = select(ProductVariant).where(ProductVariant.product_id == product_id)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, variant_id: str) -> ProductVariant:
        result = await db.execute(select(ProductVariant).where(ProductVariant.id == variant_id))
        variant = result.scalar_one_or_none()
        if not variant:
            raise ValueError("Variant not found")
        return variant

    @staticmethod
    async def get_low_stock(db: AsyncSession, threshold: int = 5) -> list[ProductVariant]:
        query = select(ProductVariant).where(ProductVariant.stock_quantity <= threshold)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update(db: AsyncSession, variant_id: str, data: dict) -> ProductVariant:
        variant = await VariantService.get_by_id(db, variant_id)
        for key, value in data.items():
            if value is not None:
                setattr(variant, key, value)
        await db.commit()
        await db.refresh(variant)
        return variant

    @staticmethod
    async def adjust_stock(db: AsyncSession, variant_id: str, quantity_change: int) -> ProductVariant:
        variant = await VariantService.get_by_id(db, variant_id)
        new_stock = variant.stock_quantity + quantity_change
        if new_stock < 0:
            raise ValueError("Insufficient stock")
        variant.stock_quantity = new_stock
        await db.commit()
        await db.refresh(variant)
        return variant

    @staticmethod
    async def delete(db: AsyncSession, variant_id: str) -> None:
        variant = await VariantService.get_by_id(db, variant_id)
        variant.is_active = False
        await db.commit()
