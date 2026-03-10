from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.variants.model import ProductVariant
from app.modules.variants.schema import VariantCreate, VariantUpdate


class VariantService:
    @staticmethod
    async def create(
        db: AsyncSession, product_id: str, data: VariantCreate
    ) -> ProductVariant:
        """Create a new variant."""
        # Import locally to avoid circular imports
        from app.modules.products.model import Product

        # Verify product exists
        result = await db.execute(select(Product).where(Product.id == product_id))
        if not result.scalar_one_or_none():
            raise ValueError("Product not found")

        # Check SKU uniqueness
        result = await db.execute(
            select(ProductVariant).where(ProductVariant.sku == data.sku)
        )
        if result.scalar_one_or_none():
            raise ValueError("SKU already exists")

        variant = ProductVariant(product_id=product_id, **data.model_dump())
        db.add(variant)
        await db.commit()
        await db.refresh(variant)
        return variant

    @staticmethod
    async def get_by_product(db: AsyncSession, product_id: str) -> list[ProductVariant]:
        """Get all variants for a product."""
        query = select(ProductVariant).where(ProductVariant.product_id == product_id)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, variant_id: str) -> ProductVariant:
        """Get variant by ID."""
        result = await db.execute(
            select(ProductVariant).where(ProductVariant.id == variant_id)
        )
        variant = result.scalar_one_or_none()
        if not variant:
            raise ValueError("Variant not found")
        return variant

    @staticmethod
    async def get_low_stock(
        db: AsyncSession, threshold: int = 5
    ) -> list[ProductVariant]:
        """Get variants with low stock."""
        query = (
            select(ProductVariant)
            .where(ProductVariant.stock_quantity <= threshold)
            .where(ProductVariant.is_active == True)
            .order_by(ProductVariant.stock_quantity.asc())
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def update(
        db: AsyncSession, variant_id: str, data: VariantUpdate
    ) -> ProductVariant:
        """Update a variant."""
        result = await db.execute(
            select(ProductVariant).where(ProductVariant.id == variant_id)
        )
        variant = result.scalar_one_or_none()
        if not variant:
            raise ValueError("Variant not found")

        for field, value in data.model_dump(exclude_none=True).items():
            setattr(variant, field, value)

        await db.commit()
        await db.refresh(variant)
        return variant

    @staticmethod
    async def adjust_stock(
        db: AsyncSession, variant_id: str, quantity_change: int
    ) -> ProductVariant:
        """Adjust stock quantity."""
        variant = await VariantService.get_by_id(db, variant_id)
        new_stock = variant.stock_quantity + quantity_change
        if new_stock < 0:
            raise ValueError(
                f"Insufficient stock. Available: {variant.stock_quantity}"
            )
        variant.stock_quantity = new_stock
        await db.commit()
        await db.refresh(variant)
        return variant

    @staticmethod
    async def delete(db: AsyncSession, variant_id: str) -> None:
        """Soft delete a variant."""
        variant = await VariantService.get_by_id(db, variant_id)
        variant.is_active = False
        await db.commit()
