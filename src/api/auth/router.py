from fastapi import APIRouter, Response, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.request.login import LoginRequest
from src.services.auth_service import AuthService
from src.core.db import get_db

router = APIRouter(
    prefix="",
    tags=["auth"],
)


@router.post("/login")
async def login(request: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    """Authenticate user and set access_token as an httpOnly cookie"""
    service = AuthService(response, db)
    return await service.authenticate_user_service(request)


@router.post("/verify-token")
async def very_access_token(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    service = AuthService(response, db)
    return await service.verify_access_token_service(request)


@router.post("/logout")
async def logout_user(response: Response, db: AsyncSession = Depends(get_db)):
    """Clear the user access_token cookie."""
    service = AuthService(response, db)
    return await service.logout_user_service()
