from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User


class UserRepository:
    @staticmethod
    async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
        """Fetch a user by user email."""
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(user_id: str, session: AsyncSession) -> User | None:
        """Fetch a user by user ID."""
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
