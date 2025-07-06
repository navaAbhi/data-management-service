from datetime import datetime, timezone
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
        token_data = FAKE_USER_TOKENS.get(str(user.name))

        if not token_data:
            raise HTTPException(
                500, detail="No fake token mapped for this user")

        self.response.set_cookie(
            key="Authorization",
            value=token_data["token"],
            max_age=60*60,
            httponly=True,
            # samesite="lax",
            secure=False
        )
        return {"message": "Logged in successfully"}

    async def verify_access_token_service(self, request):
        """Verify the user's access token from the request cookie."""
        token = self.get_token_from_cookie(request)

        if not token:
            await self.logout_user_service()
            raise HTTPException(
                status_code=401, detail="Missing or expired token. Logged out.")

        user = self.get_user_from_token(token)

        if not user:
            await self.logout_user_service()
            raise HTTPException(
                status_code=401, detail="Invalid or expired token. Logged out.")

        return {"status": "valid token", "user": user}

    def get_token_from_cookie(self, request):
        """Validate the token against the FAKE_USER_TOKENS store and check expiration."""
        return request.cookies.get("Authorization")

    def get_user_from_token(self, token):
        """Validate the token against the FAKE_USER_TOKENS store and check expiration."""
        for username, data in FAKE_USER_TOKENS.items():
            if data["token"] == token:
                if datetime.now(timezone.utc) < data["expires_at"]:
                    return username
                else:
                    return None
        return None

    async def logout_user_service(self):
        """Logout user by deleting the Authorization cookie in the header"""
        self.response.delete_cookie("Authorization")
        return {"message": "Logged out successfully"}
