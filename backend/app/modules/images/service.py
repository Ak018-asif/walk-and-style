from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.images.model import ProductImage
from app.modules.variants.model import ProductVariant


class ImageService:
    @staticmethod
    async def create(db: AsyncSession, variant_id: str, data: ProductImage) -> ProductImage:
        # verify variant exists
        result = await db.execute(select(ProductVariant).where(ProductVariant.id == variant_id))
        if not result.scalar_one_or_none():
            raise ValueError("Variant not found")
        # if primary unset existing
        if data.is_primary:
            images = (
                await db.execute(
                    select(ProductImage).where(ProductImage.product_variant_id == variant_id)
                )
            ).scalars().all()
            for img in images:
                img.is_primary = False
        image = ProductImage(product_variant_id=variant_id, **data.model_dump())
        db.add(image)
        await db.commit()
        await db.refresh(image)
        return image

    @staticmethod
    async def get_by_variant(db: AsyncSession, variant_id: str) -> list[ProductImage]:
        result = await db.execute(
            select(ProductImage).where(ProductImage.product_variant_id == variant_id)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, image_id: str) -> ProductImage:
        result = await db.execute(select(ProductImage).where(ProductImage.id == image_id))
        image = result.scalar_one_or_none()
        if not image:
            raise ValueError("Image not found")
        return image

    @staticmethod
    async def update(db: AsyncSession, image_id: str, data: dict) -> ProductImage:
        image = await ImageService.get_by_id(db, image_id)
        if data.get("is_primary"):
            # unset others
            imgs = (
                await db.execute(
                    select(ProductImage).where(ProductImage.product_variant_id == image.product_variant_id)
                )
            ).scalars().all()
            for img in imgs:
                img.is_primary = False
        for key, value in data.items():
            if value is not None:
                setattr(image, key, value)
        await db.commit()
        await db.refresh(image)
        return image

    @staticmethod
    async def delete(db: AsyncSession, image_id: str) -> None:
        image = await ImageService.get_by_id(db, image_id)
        await db.delete(image)
        await db.commit()
