from datetime import datetime, timezone
from fastapi import Security, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_db
from src.repository.user_repository import UserRepository
from src.utils.user_tokens import FAKE_USER_TOKENS

security = HTTPBearer()


async def get_current_user(
    request: Request,
    # credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Security(get_db)
):
    # token = credentials.credentials  # extracts from Authorization: Bearer <token>
    token = request.cookies.get("Authorization")

    # if token not in FAKE_USER_TOKENS:
    #     raise HTTPException(status_code=401, detail="Invalid user token")

    # user_id = FAKE_USER_TOKENS[token]

    user_record = None
    for username, data in FAKE_USER_TOKENS.items():
        if data["token"] == token:
            user_record = data
            user_record["username"] = username
            break

    if not user_record:
        raise HTTPException(status_code=401, detail="Invalid token")

    if user_record["expires_at"] < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Token expired")

    user_id = user_record["token"]
    user = await UserRepository.get_user_by_id(str(user_id), db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
