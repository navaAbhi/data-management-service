import asyncio
from src.core.db import engine
from src.models.base import Base


async def init_models():
    """Util to create all base tables as soon as db connection is established in postgres"""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    print("All tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_models())
