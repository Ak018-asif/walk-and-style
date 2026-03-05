from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.security import hash_password, verify_password, create_access_token
from models.models import User


class AuthService:
    """Service for Authentication operations."""

    @staticmethod
    async def register(db: AsyncSession, full_name: str, email: str, phone: str, password: str) -> User:
        """Register a new user."""
        # Check if email already exists
        result = await db.execute(select(User).where(User.email == email))
        if result.scalar_one_or_none():
            raise ValueError("Email already registered")

        # Check if phone already exists
        result = await db.execute(select(User).where(User.phone == phone))
        if result.scalar_one_or_none():
            raise ValueError("Phone number already registered")

        # Create new user
        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            password_hash=hash_password(password),
            is_active=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def login(db: AsyncSession, email: str, password: str) -> str:
        """Login user and return access token."""
        # Find user by email
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user:
            raise ValueError("Invalid credentials")

        # Verify password
        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        # Check if active
        if not user.is_active:
            raise ValueError("Account deactivated")

        # Return JWT token
        return create_access_token({"sub": user.id})
