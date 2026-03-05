from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from core.dependencies import get_current_user
from models.models import User
from schemas.schemas import (
    CategoryCreate,
    CategoryResponse,
    BrandCreate,
    BrandResponse,
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    VariantCreate,
    VariantUpdate,
    VariantResponse,
    ImageCreate,
    ImageResponse,
)
from services.product_service import (
    CategoryService,
    BrandService,
    ProductService,
    VariantService,
    ImageService,
)

router = APIRouter(tags=["Products"])


# ============ CATEGORY ENDPOINTS ============
@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category(
    body: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new category (admin only)."""
    try:
        category = await CategoryService.create(
            db=db,
            name=body.name,
            slug=body.slug,
            parent_id=body.parent_id,
            is_active=body.is_active,
        )
        return category
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/categories", response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    """Get all active categories."""
    categories = await CategoryService.get_all(db=db)
    return categories


@router.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific category."""
    try:
        category = await CategoryService.get_by_id(db=db, category_id=category_id)
        return category
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============ BRAND ENDPOINTS ============
@router.post("/brands", response_model=BrandResponse, status_code=201)
async def create_brand(
    body: BrandCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new brand (admin only)."""
    try:
        brand = await BrandService.create(
            db=db,
            name=body.name,
            description=body.description,
            is_active=body.is_active,
        )
        return brand
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/brands", response_model=list[BrandResponse])
async def get_brands(db: AsyncSession = Depends(get_db)):
    """Get all active brands."""
    brands = await BrandService.get_all(db=db)
    return brands


@router.get("/brands/{brand_id}", response_model=BrandResponse)
async def get_brand(brand_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific brand."""
    try:
        brand = await BrandService.get_by_id(db=db, brand_id=brand_id)
        return brand
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============ PRODUCT ENDPOINTS ============
@router.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(
    body: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new product (admin only)."""
    try:
        product = await ProductService.create(
            db=db,
            name=body.name,
            base_price=body.base_price,
            description=body.description,
            gender=body.gender,
            brand_id=body.brand_id,
            category_id=body.category_id,
            is_active=body.is_active,
        )
        return product
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/products", response_model=list[ProductResponse])
async def get_products(
    gender: str = Query(None),
    category_id: str = Query(None),
    brand_id: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get all active products with optional filters."""
    products = await ProductService.get_all(
        db=db,
        gender=gender,
        category_id=category_id,
        brand_id=brand_id,
        skip=skip,
        limit=limit,
    )
    return products


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific product with variants and images."""
    try:
        product = await ProductService.get_by_id(db=db, product_id=product_id)
        return product
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    body: ProductUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a product (admin only)."""
    try:
        data = body.model_dump(exclude_none=True)
        product = await ProductService.update(db=db, product_id=product_id, data=data)
        return product
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/products/{product_id}", status_code=204)
async def delete_product(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a product (soft delete, admin only)."""
    try:
        await ProductService.delete(db=db, product_id=product_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============ VARIANT ENDPOINTS ============
@router.post("/products/{product_id}/variants", response_model=VariantResponse, status_code=201)
async def create_variant(
    product_id: str,
    body: VariantCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a product variant (admin only)."""
    try:
        variant = await VariantService.create(
            db=db,
            product_id=product_id,
            sku=body.sku,
            size=body.size,
            color=body.color,
            stock_quantity=body.stock_quantity,
            price_override=body.price_override,
            is_active=body.is_active,
        )
        return variant
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/products/{product_id}/variants", response_model=list[VariantResponse])
async def get_product_variants(product_id: str, db: AsyncSession = Depends(get_db)):
    """Get all variants for a product."""
    variants = await VariantService.get_by_product(db=db, product_id=product_id)
    return variants


@router.patch("/variants/{variant_id}", response_model=VariantResponse)
async def update_variant(
    variant_id: str,
    body: VariantUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a variant (admin only)."""
    try:
        data = body.model_dump(exclude_none=True)
        variant = await VariantService.update(db=db, variant_id=variant_id, data=data)
        return variant
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============ IMAGE ENDPOINTS ============
@router.post("/variants/{variant_id}/images", response_model=ImageResponse, status_code=201)
async def add_image(
    variant_id: str,
    body: ImageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add an image to a variant (admin only)."""
    try:
        image = await ImageService.add_image(
            db=db,
            product_variant_id=variant_id,
            image_url=body.image_url,
            is_primary=body.is_primary,
        )
        return image
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/variants/{variant_id}/images", response_model=list[ImageResponse])
async def get_variant_images(variant_id: str, db: AsyncSession = Depends(get_db)):
    """Get all images for a variant."""
    images = await ImageService.get_by_variant(db=db, product_variant_id=variant_id)
    return images


@router.delete("/images/{image_id}", status_code=204)
async def delete_image(
    image_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete an image (admin only)."""
    try:
        await ImageService.delete(db=db, image_id=image_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
