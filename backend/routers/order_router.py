from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from core.dependencies import get_current_user
from models.models import User
from schemas.schemas import (
    OrderCreate,
    OrderResponse,
    PaymentCreate,
    PaymentResponse,
)
from services.order_service import OrderService, PaymentService

router = APIRouter(tags=["Orders"])


@router.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(
    body: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new order."""
    try:
        order_items = [
            {
                "product_variant_id": item.product_variant_id,
                "quantity": item.quantity,
            }
            for item in body.items
        ]
        order = await OrderService.create_order(
            db=db,
            user_id=current_user.id,
            shipping_address_id=body.shipping_address_id,
            items=order_items,
        )
        return order
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/orders", response_model=list[OrderResponse])
async def get_user_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all orders for the current user."""
    orders = await OrderService.get_user_orders(db=db, user_id=current_user.id)
    return orders


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific order."""
    try:
        order = await OrderService.get_order_by_id(
            db=db, order_id=order_id, user_id=current_user.id
        )
        return order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "not found" in str(e) else status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.post("/orders/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Cancel an order."""
    try:
        order = await OrderService.cancel_order(
            db=db, order_id=order_id, user_id=current_user.id
        )
        return order
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/orders/{order_id}/payment", response_model=PaymentResponse, status_code=201)
async def record_payment(
    order_id: str,
    body: PaymentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Record a payment for an order."""
    try:
        payment = await PaymentService.record_payment(
            db=db,
            order_id=order_id,
            user_id=current_user.id,
            payment_method=body.payment_method,
            transaction_id=body.transaction_id,
            paid_amount=body.paid_amount,
        )
        return payment
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
