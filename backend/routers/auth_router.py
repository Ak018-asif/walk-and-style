from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.schemas import UserCreate, LoginRequest, TokenResponse, UserResponse
from services.auth_service import AuthService
from core.dependencies import get_current_user
from models.models import User

router = APIRouter(tags=["Auth"])


@router.post("/auth/register", response_model=UserResponse, status_code=201)
async def register(body: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user."""
    try:
        user = await AuthService.register(
            db=db,
            full_name=body.full_name,
            email=body.email,
            phone=body.phone,
            password=body.password,
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/auth/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Login and get access token."""
    try:
        token = await AuthService.login(db=db, email=body.email, password=body.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        )


@router.get("/auth/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current authenticated user profile."""
    return current_user
