from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.core.config import DATABASE_URI

"""Register SQLAlchemy models into the engine"""
import src.models.user
import src.models.credential
import src.models.import_job
import src.models.file
import src.models.file_metadata

engine = create_async_engine(str(DATABASE_URI), echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
