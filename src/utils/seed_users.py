import asyncio
from sqlalchemy import select
from src.core.db import AsyncSessionLocal
from src.models.user import User


async def seed_users():
    """Util to seed sample users in the database"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        if users:
            print("Users already seeded.")
            return

        # sample users
        user1 = User(email="abhinav@panaroma.ai", name="Abhinav")
        user2 = User(email="admin@panaroma.ai", name="Admin")

        session.add_all([user1, user2])
        await session.commit()
        print("Seeded sample users!")

if __name__ == "__main__":
    asyncio.run(seed_users())
