from datetime import datetime, timezone
from src.celery_app import celery_app
from src.core.db import AsyncSessionLocal, get_db  # your DB session maker
from src.models.file import File
from src.models.import_job import ImportJob
from src.enum.status_enum import ImportJobStatus
from sqlalchemy.future import select
import asyncio
import uuid


@celery_app.task(bind=True)
def copy_from_s3_link(self, import_job_id, source_url):
    """
    This runs OUTSIDE the FastAPI process in a separate worker.
    """
    # switch to asyncio event loop
    asyncio.run(process_import_job(import_job_id, source_url))


async def process_import_job(import_job_id, source_url):
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(ImportJob).where(ImportJob.id == uuid.UUID(import_job_id)))
        job = result.scalars().first()

        if not job:
            print(f"No job found for ID {import_job_id}")
            return

        for progress in range(0, 101, 20):
            job.progress_percentage = progress  # type: ignore
            job.updated_at = datetime.now(timezone.utc)  # type: ignore
            await db.commit()
            print(f"Updated progress to {progress}%")
            await asyncio.sleep(2)

        job.status = ImportJobStatus.IN_PROGRESS  # type: ignore
        await db.commit()
        print("Job set to IN_PROGRESS")


@celery_app.task(bind=True)
def process_local_upload(self, job_id, s3_key, original_filename, size):
    asyncio.run(_process_local_upload(job_id, s3_key, original_filename, size))


async def _process_local_upload(job_id, s3_key, original_filename, size):
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(ImportJob).where(ImportJob.id == uuid.UUID(job_id)))
        job = result.scalars().first()

        if not job:
            print(f"Job not found for id: {job_id}")
            return

        # simulate processing, e.g. verifying file, scanning, extracting metadata etc
        for progress in range(0, 101, 25):
            job.progress_percentage = progress  # type: ignore
            job.status = ImportJobStatus.IN_PROGRESS  # type: ignore
            job.updated_at = datetime.now(timezone.utc)  # type: ignore
            await db.commit()
            print(f"Local upload job {job_id}: {progress}% complete")
            await asyncio.sleep(2)

        # finally mark COMPLETED and create File record
        job.progress_percentage = 100  # type: ignore
        job.status = ImportJobStatus.COMPLETED  # type: ignore
        job.updated_at = datetime.now(timezone.utc)  # type: ignore
        await db.commit()

        file = File(
            id=uuid.uuid4(),
            import_job_id=job.id,
            original_filename=original_filename,
            s3_key=s3_key,
            size=size,
            uploaded_at=datetime.now(timezone.utc)
        )
        db.add(file)
        await db.commit()
        print(f"Local upload job {job_id} completed.")
