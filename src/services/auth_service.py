from fastapi import HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.user_repository import UserRepository
from src.schemas.request.login import LoginRequest
from src.utils.user_tokens import FAKE_USER_TOKENS


class AuthService:
    """Service class for authentication and authorization operations."""

    def __init__(self, response: Response, db: AsyncSession):
        self.response = response
        self.db = db

    async def authenticate_user_service(self, data: LoginRequest):
        user = await UserRepository.get_user_by_email(data.email, self.db)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email")

        # Find matching fake token
        # string casting because user.name is a Column in model but after fetching from db it is string so explicitly casting is better
        token = FAKE_USER_TOKENS.get(str(user.name))

        if not token:
            raise HTTPException(
                500, detail="No fake token mapped for this user")

        self.response.set_cookie(
            key="Authorization",
            value=token,
            httponly=True,
            secure=False
        )
        return {"message": "Logged in successfully"}

    async def logout_user_service(self):
        self.response.delete_cookie("Authorization")
        return {"message": "Logged out successfully"}
