from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.products.model import Product
from app.modules.products.schema import ProductCreate, ProductUpdate


class ProductService:
    @staticmethod
    async def create(db: AsyncSession, data: ProductCreate) -> Product:
        """Create a new product."""
        product = Product(**data.model_dump())
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def get_all(
        db: AsyncSession,
        gender: str | None = None,
        category_id: str | None = None,
        brand_id: str | None = None,
        active_only: bool = True,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Product]:
        """Get all products with optional filters."""
        query = select(Product)
        if active_only:
            query = query.where(Product.is_active == True)
        if gender:
            query = query.where(Product.gender == gender)
        if category_id:
            query = query.where(Product.category_id == category_id)
        if brand_id:
            query = query.where(Product.brand_id == brand_id)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, product_id: str) -> Product:
        """Get product by ID with variants and images."""
        query = select(Product).where(Product.id == product_id).options(
            selectinload(Product.variants)
        )
        result = await db.execute(query)
        product = result.scalar_one_or_none()
        if not product:
            raise ValueError("Product not found")
        return product

    @staticmethod
    async def update(db: AsyncSession, product_id: str, data: ProductUpdate) -> Product:
        """Update a product."""
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            raise ValueError("Product not found")

        for field, value in data.model_dump(exclude_none=True).items():
            setattr(product, field, value)

        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def delete(db: AsyncSession, product_id: str) -> None:
        """Soft delete a product."""
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            raise ValueError("Product not found")

        product.is_active = False
        await db.commit()
