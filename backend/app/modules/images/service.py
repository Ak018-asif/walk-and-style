from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.images.model import ProductImage
from app.modules.images.schema import ImageCreate, ImageUpdate


class ImageService:
    @staticmethod
    async def create(
        db: AsyncSession, variant_id: str, data: ImageCreate
    ) -> ProductImage:
        """Create a new image for a variant."""
        # Import locally to avoid circular imports
        from app.modules.variants.model import ProductVariant

        # Verify variant exists
        result = await db.execute(
            select(ProductVariant).where(ProductVariant.id == variant_id)
        )
        if not result.scalar_one_or_none():
            raise ValueError("Variant not found")

        # If setting as primary, unset others
        if data.is_primary:
            images = (
                await db.execute(
                    select(ProductImage).where(
                        ProductImage.product_variant_id == variant_id
                    )
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
    async def get_by_variant(
        db: AsyncSession, variant_id: str
    ) -> list[ProductImage]:
        """Get all images for a variant."""
        result = await db.execute(
            select(ProductImage).where(
                ProductImage.product_variant_id == variant_id
            )
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, image_id: str) -> ProductImage:
        """Get image by ID."""
        result = await db.execute(
            select(ProductImage).where(ProductImage.id == image_id)
        )
        image = result.scalar_one_or_none()
        if not image:
            raise ValueError("Image not found")
        return image

    @staticmethod
    async def update(
        db: AsyncSession, image_id: str, data: ImageUpdate
    ) -> ProductImage:
        """Update an image."""
        image = await ImageService.get_by_id(db, image_id)

        # If setting as primary, unset others
        if data.is_primary:
            images = (
                await db.execute(
                    select(ProductImage).where(
                        ProductImage.product_variant_id == image.product_variant_id
                    )
                )
            ).scalars().all()
            for img in images:
                img.is_primary = False

        for field, value in data.model_dump(exclude_none=True).items():
            setattr(image, field, value)

        await db.commit()
        await db.refresh(image)
        return image

    @staticmethod
    async def delete(db: AsyncSession, image_id: str) -> None:
        """Delete an image."""
        image = await ImageService.get_by_id(db, image_id)
        await db.delete(image)
        await db.commit()
