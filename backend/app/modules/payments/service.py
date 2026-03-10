from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.payments.model import Payment
from app.modules.payments.schema import PaymentCreate, PaymentUpdate


class PaymentService:
    """Service for payment operations."""

    @staticmethod
    async def create(
        db: AsyncSession,
        user_id: str,
        order_id: str,
        data: PaymentCreate,
    ) -> Payment:
        """Create a new payment for an order."""
        # Local import to avoid circular dependencies
        from app.modules.orders.model import Order

        # Fetch order and verify
        result = await db.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if not order:
            raise ValueError("Order not found")

        # Verify user owns the order
        if order.user_id != user_id:
            raise ValueError("User does not own this order")

        # Check if payment already exists
        result = await db.execute(select(Payment).where(Payment.order_id == order_id))
        existing = result.scalar_one_or_none()
        if existing:
            raise ValueError("Payment already exists for this order")

        # Create payment
        payment = Payment(
            order_id=order_id,
            payment_method=data.payment_method,
            transaction_id=data.transaction_id,
            paid_amount=data.paid_amount,
            payment_status="success",
            paid_at=datetime.utcnow(),
        )
        db.add(payment)

        # Update order status
        order.status = "confirmed"

        # Commit
        await db.commit()

        # Refresh
        result = await db.execute(
            select(Payment).where(Payment.id == payment.id).options(selectinload(Payment.order))
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 50) -> list[Payment]:
        """Get all payments."""
        result = await db.execute(
            select(Payment)
            .options(selectinload(Payment.order))
            .order_by(Payment.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().unique().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, payment_id: str) -> Payment:
        """Get a payment by ID."""
        result = await db.execute(
            select(Payment).where(Payment.id == payment_id).options(selectinload(Payment.order))
        )
        payment = result.scalar_one_or_none()
        if not payment:
            raise ValueError("Payment not found")
        return payment

    @staticmethod
    async def get_by_order(db: AsyncSession, order_id: str) -> Optional[Payment]:
        """Get payment for an order."""
        result = await db.execute(
            select(Payment).where(Payment.order_id == order_id).options(selectinload(Payment.order))
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, payment_id: str, data: PaymentUpdate) -> Payment:
        """Update a payment."""
        result = await db.execute(select(Payment).where(Payment.id == payment_id))
        payment = result.scalar_one_or_none()
        if not payment:
            raise ValueError("Payment not found")

        # Update fields
        if data.payment_method is not None:
            payment.payment_method = data.payment_method
        if data.transaction_id is not None:
            payment.transaction_id = data.transaction_id
        if data.paid_amount is not None:
            payment.paid_amount = data.paid_amount
        if data.payment_status is not None:
            payment.payment_status = data.payment_status

        await db.commit()

        # Refresh
        result = await db.execute(
            select(Payment).where(Payment.id == payment.id).options(selectinload(Payment.order))
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def delete(db: AsyncSession, payment_id: str) -> None:
        """Delete a payment (cannot delete if success)."""
        result = await db.execute(select(Payment).where(Payment.id == payment_id))
        payment = result.scalar_one_or_none()
        if not payment:
            raise ValueError("Payment not found")

        if payment.payment_status == "success":
            raise ValueError("Cannot delete a successful payment")

        await db.delete(payment)
        await db.commit()
