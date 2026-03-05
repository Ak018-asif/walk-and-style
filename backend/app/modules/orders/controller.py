from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.orders.schema import (
    OrderCreate,
    OrderResponse,
    OrderListResponse,
    OrderStatusUpdate,
)
from app.modules.orders.service import OrderService
# from app.modules.users.schema import AddressSchema  # unused
from core.dependencies import get_db, get_current_user
from models.models import User

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        order = await OrderService.create(
            db,
            user_id=current_user.id,
            shipping_address_id=order_data.shipping_address_id,
            items=[item.dict() for item in order_data.items],
        )
        return order
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/", response_model=OrderListResponse)
async def list_orders(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    orders = await OrderService.get_all(db, skip, limit)
    return {"orders": orders}


@router.get("/my", response_model=OrderListResponse)
async def my_orders(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = await OrderService.get_by_user(db, current_user.id)
    return {"orders": orders}


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        order = await OrderService.get_by_id(db, order_id, current_user.id)
        return order
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: str,
    status_update: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # in a real app, we'd check admin rights for status change
    try:
        order = await OrderService.update_status(db, order_id, status_update.status)
        return order
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(
    order_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        order = await OrderService.cancel(db, order_id, current_user.id)
        return order
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
