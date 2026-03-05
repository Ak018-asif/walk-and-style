from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from core.dependencies import get_current_user
from app.modules.images.schema import (
    ImageCreate,
    ImageUpdate,
    ImageResponse,
)
from app.modules.images.model import ProductImage
from app.modules.images.service import ImageService

router = APIRouter(tags=["Images"])


@router.post("/variants/{variant_id}/images", response_model=ImageResponse, status_code=201)
async def create_image(
    variant_id: str,
    body: ImageCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        image = await ImageService.create(db, variant_id, ProductImage(**body.model_dump()))
        return image
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/variants/{variant_id}/images", response_model=list[ImageResponse])
async def get_images(variant_id: str, db: AsyncSession = Depends(get_db)):
    return await ImageService.get_by_variant(db, variant_id)


@router.get("/images/{image_id}", response_model=ImageResponse)
async def get_image(image_id: str, db: AsyncSession = Depends(get_db)):
    try:
        return await ImageService.get_by_id(db, image_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/images/{image_id}", response_model=ImageResponse)
async def update_image(
    image_id: str,
    body: ImageUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        data = body.model_dump(exclude_none=True)
        return await ImageService.update(db, image_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/images/{image_id}", status_code=204)
async def delete_image(
    image_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        await ImageService.delete(db, image_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
