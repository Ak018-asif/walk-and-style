from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.modules.auth.model import User
from app.modules.images.schema import (
    ImageCreate,
    ImageResponse,
    ImageUpdate,
)
from app.modules.images.service import ImageService

router = APIRouter(tags=["Images"])


@router.post(
    "/variants/{variant_id}/images",
    response_model=ImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_image(
    variant_id: str,
    data: ImageCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Create a new image for a variant (auth required)."""
    try:
        return await ImageService.create(db, variant_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/variants/{variant_id}/images", response_model=list[ImageResponse])
async def get_images(variant_id: str, db: AsyncSession = Depends(get_db)):
    """Get all images for a variant."""
    return await ImageService.get_by_variant(db, variant_id)


@router.get("/images/{image_id}", response_model=ImageResponse)
async def get_image(image_id: str, db: AsyncSession = Depends(get_db)):
    """Get an image by ID."""
    try:
        return await ImageService.get_by_id(db, image_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/images/{image_id}", response_model=ImageResponse)
async def update_image(
    image_id: str,
    data: ImageUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Update an image (auth required)."""
    try:
        return await ImageService.update(db, image_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    image_id: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Delete an image (auth required)."""
    try:
        await ImageService.delete(db, image_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
