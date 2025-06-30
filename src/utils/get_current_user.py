from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_db
from src.repository.user_repository import UserRepository
from src.utils.user_tokens import FAKE_USER_TOKENS

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Security(get_db)
):
    token = credentials.credentials  # extracts from Authorization: Bearer <token>

    if token not in FAKE_USER_TOKENS:
        raise HTTPException(status_code=401, detail="Invalid user token")

    user_id = FAKE_USER_TOKENS[token]
    user = await UserRepository.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
