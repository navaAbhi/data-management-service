from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.models.file import File
from src.models.import_job import ImportJob


class ImportRepository:
    @staticmethod
    async def insert_import_job(job: ImportJob, session: AsyncSession) -> ImportJob:
        """Insert an ImportJob object into the database."""
        session.add(job)
        await session.commit()
        await session.refresh(job)
        return job

    @staticmethod
    async def insert_file(file: File, session: AsyncSession) -> File:
        """Insert a File object into the database."""
        session.add(file)
        await session.commit()
        await session.refresh(file)
        return file

    @staticmethod
    async def get_import_job_by_id(job_id: UUID, session: AsyncSession) -> ImportJob | None:
        result = await session.execute(select(ImportJob).where(ImportJob.id == job_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_import_job(job: ImportJob, session: AsyncSession) -> ImportJob:
        session.add(job)
        await session.commit()
        await session.refresh(job)
        return job
