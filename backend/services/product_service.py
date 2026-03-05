from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.models import (
    Category,
    Brand,
    Product,
    ProductVariant,
    ProductImage,
)


class CategoryService:
    """Service for Category operations."""

    @staticmethod
    async def create(db: AsyncSession, name: str, slug: str, parent_id: str | None = None, is_active: bool = True) -> Category:
        """Create a new category."""
        # Check slug uniqueness
        result = await db.execute(select(Category).where(Category.slug == slug))
        if result.scalar_one_or_none():
            raise ValueError("Slug already exists")

        category = Category(
            name=name,
            slug=slug,
            parent_id=parent_id,
            is_active=is_active,
        )
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Category]:
        """Get all active categories."""
        result = await db.execute(select(Category).where(Category.is_active == True))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, category_id: str) -> Category:
        """Get a category by ID."""
        result = await db.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()
        if not category:
            raise ValueError(f"Category {category_id} not found")
        return category


class BrandService:
    """Service for Brand operations."""

    @staticmethod
    async def create(db: AsyncSession, name: str, description: str | None = None, is_active: bool = True) -> Brand:
        """Create a new brand."""
        # Check name uniqueness
        result = await db.execute(select(Brand).where(Brand.name == name))
        if result.scalar_one_or_none():
            raise ValueError("Brand name already exists")

        brand = Brand(
            name=name,
            description=description,
            is_active=is_active,
        )
        db.add(brand)
        await db.commit()
        await db.refresh(brand)
        return brand

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Brand]:
        """Get all active brands."""
        result = await db.execute(select(Brand).where(Brand.is_active == True))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, brand_id: str) -> Brand:
        """Get a brand by ID."""
        result = await db.execute(select(Brand).where(Brand.id == brand_id))
        brand = result.scalar_one_or_none()
        if not brand:
            raise ValueError(f"Brand {brand_id} not found")
        return brand


class ProductService:
    """Service for Product operations."""

    @staticmethod
    async def create(db: AsyncSession, name: str, base_price: float, description: str | None = None,
                     gender: str | None = None, brand_id: str | None = None, 
                     category_id: str | None = None, is_active: bool = True) -> Product:
        """Create a new product."""
        product = Product(
            name=name,
            description=description,
            base_price=base_price,
            gender=gender,
            brand_id=brand_id,
            category_id=category_id,
            is_active=is_active,
        )
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def get_all(db: AsyncSession, gender: str | None = None, category_id: str | None = None,
                      brand_id: str | None = None, skip: int = 0, limit: int = 10) -> list[Product]:
        """Get all active products with optional filters."""
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
        """Get a product by ID with variants and images."""
        query = select(Product).where(Product.id == product_id).options(
            selectinload(Product.variants).selectinload(ProductVariant.images)
        )
        result = await db.execute(query)
        product = result.scalar_one_or_none()
        if not product:
            raise ValueError(f"Product {product_id} not found")
        return product

    @staticmethod
    async def update(db: AsyncSession, product_id: str, data: dict) -> Product:
        """Partially update a product."""
        product = await ProductService.get_by_id(db, product_id)

        for key, value in data.items():
            if value is not None:
                setattr(product, key, value)

        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def delete(db: AsyncSession, product_id: str) -> None:
        """Soft delete a product."""
        product = await ProductService.get_by_id(db, product_id)
        product.is_active = False
        await db.commit()


class VariantService:
    """Service for ProductVariant operations."""

    @staticmethod
    async def create(db: AsyncSession, product_id: str, sku: str, size: str, color: str,
                     stock_quantity: int = 0, price_override: float | None = None,
                     is_active: bool = True) -> ProductVariant:
        """Create a new product variant."""
        # Verify product exists
        result = await db.execute(select(Product).where(Product.id == product_id))
        if not result.scalar_one_or_none():
            raise ValueError(f"Product {product_id} not found")

        # Check SKU uniqueness
        result = await db.execute(select(ProductVariant).where(ProductVariant.sku == sku))
        if result.scalar_one_or_none():
            raise ValueError("SKU already exists")

        variant = ProductVariant(
            product_id=product_id,
            sku=sku,
            size=size,
            color=color,
            stock_quantity=stock_quantity,
            price_override=price_override,
            is_active=is_active,
        )
        db.add(variant)
        await db.commit()
        await db.refresh(variant)
        return variant

    @staticmethod
    async def get_by_product(db: AsyncSession, product_id: str) -> list[ProductVariant]:
        """Get all variants for a product with images."""
        query = select(ProductVariant).where(ProductVariant.product_id == product_id).options(
            selectinload(ProductVariant.images)
        )
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, variant_id: str) -> ProductVariant:
        """Get a variant by ID."""
        result = await db.execute(select(ProductVariant).where(ProductVariant.id == variant_id))
        variant = result.scalar_one_or_none()
        if not variant:
            raise ValueError(f"Variant {variant_id} not found")
        return variant

    @staticmethod
    async def update(db: AsyncSession, variant_id: str, data: dict) -> ProductVariant:
        """Partially update a variant."""
        variant = await VariantService.get_by_id(db, variant_id)

        for key, value in data.items():
            if value is not None:
                setattr(variant, key, value)

        await db.commit()
        await db.refresh(variant)
        return variant


class ImageService:
    """Service for ProductImage operations."""

    @staticmethod
    async def add_image(db: AsyncSession, product_variant_id: str, image_url: str, is_primary: bool = False) -> ProductImage:
        """Add an image to a product variant."""
        # Verify variant exists
        result = await db.execute(select(ProductVariant).where(ProductVariant.id == product_variant_id))
        if not result.scalar_one_or_none():
            raise ValueError(f"Variant {product_variant_id} not found")

        # If this is primary, set all others to non-primary
        if is_primary:
            images = (await db.execute(
                select(ProductImage).where(ProductImage.product_variant_id == product_variant_id)
            )).scalars().all()
            for img in images:
                img.is_primary = False

        image = ProductImage(
            product_variant_id=product_variant_id,
            image_url=image_url,
            is_primary=is_primary,
        )
        db.add(image)
        await db.commit()
        await db.refresh(image)
        return image

    @staticmethod
    async def get_by_variant(db: AsyncSession, product_variant_id: str) -> list[ProductImage]:
        """Get all images for a variant."""
        result = await db.execute(
            select(ProductImage).where(ProductImage.product_variant_id == product_variant_id)
        )
        return result.scalars().all()

    @staticmethod
    async def delete(db: AsyncSession, image_id: str) -> None:
        """Delete an image."""
        result = await db.execute(select(ProductImage).where(ProductImage.id == image_id))
        image = result.scalar_one_or_none()
        if not image:
            raise ValueError(f"Image {image_id} not found")
        await db.delete(image)
        await db.commit()
