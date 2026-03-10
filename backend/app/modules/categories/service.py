from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.categories.model import Category
from app.modules.categories.schema import CategoryCreate, CategoryUpdate


class CategoryService:
    @staticmethod
    async def create(db: AsyncSession, data: CategoryCreate) -> Category:
        """Create a new category."""
        # Check if slug already exists
        result = await db.execute(select(Category).where(Category.slug == data.slug))
        if result.scalar_one_or_none():
            raise ValueError(f"Slug '{data.slug}' is already taken")

        category = Category(**data.model_dump())
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def get_all(db: AsyncSession, active_only: bool = True) -> list[Category]:
        """Get all categories."""
        query = select(Category)
        if active_only:
            query = query.where(Category.is_active == True)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, category_id: str) -> Category:
        """Get category by ID."""
        result = await db.execute(select(Category).where(Category.id == category_id))
        cat = result.scalar_one_or_none()
        if not cat:
            raise ValueError("Category not found")
        return cat

    @staticmethod
    async def update(
        db: AsyncSession, category_id: str, data: CategoryUpdate
    ) -> Category:
        """Update a category."""
        result = await db.execute(select(Category).where(Category.id == category_id))
        cat = result.scalar_one_or_none()
        if not cat:
            raise ValueError("Category not found")

        # Check slug uniqueness if changing
        if data.slug and data.slug != cat.slug:
            existing = await db.execute(
                select(Category).where(Category.slug == data.slug)
            )
            if existing.scalar_one_or_none():
                raise ValueError(f"Slug '{data.slug}' is already taken")

        for field, value in data.model_dump(exclude_none=True).items():
            setattr(cat, field, value)

        await db.commit()
        await db.refresh(cat)
        return cat

    @staticmethod
    async def delete(db: AsyncSession, category_id: str) -> None:
        """Soft delete a category."""
        result = await db.execute(select(Category).where(Category.id == category_id))
        cat = result.scalar_one_or_none()
        if not cat:
            raise ValueError("Category not found")

        cat.is_active = False
        await db.commit()
