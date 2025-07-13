import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from src.enum.source_type_enum import SourceType
from src.enum.status_enum import ImportJobStatus
from src.models.file import File
from src.models.import_job import ImportJob
from src.repository.import_repository import ImportRepository
from src.tasks import copy_from_s3_link, process_local_upload
from src.utils.aws_util import AwsUtil
from src.utils.constants import PRESIGNED_URL_EXPIRY_SECONDS, SERVICE_FILES_BUCKET_NAME
from sqlalchemy.ext.asyncio import AsyncSession


class ImportService:
    """Service class for all import operations"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.import_repository = ImportRepository()
        self.aws_util = AwsUtil()

    async def generate_presigned_post(self, filename, content_type, size, user_id):
        s3_key = f"user-uploads/{user_id}/{uuid.uuid4()}_{filename}"
        presigned_post = self.aws_util.get_presigned_post(
            bucket_name=SERVICE_FILES_BUCKET_NAME,
            object_name=s3_key,
            content_type=content_type,
            expires_in=PRESIGNED_URL_EXPIRY_SECONDS,
            acl="private"
        )
        return {"presigned_post": presigned_post, "s3_key": s3_key}

    async def complete_local_upload(self, user_id, data: dict):
        # Create job as QUEUED
        import_job = ImportJob(
            id=uuid.uuid4(),
            user_id=user_id,
            status=ImportJobStatus.QUEUED,
            progress_percentage=0,
            source_type=SourceType.LOCAL,
            source_details={
                "original_filename": data["original_filename"],
                "s3_key": data["s3_key"]
            },
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        await self.import_repository.insert_import_job(import_job, self.db)

        # Enqueue celery task to process uploaded file
        process_local_upload.delay(  # type: ignore
            str(import_job.id),
            data["s3_key"],
            data["original_filename"],
            data["size"]
        )

        return import_job

    async def start_link_import(self, user_id, source_url):
        import_job = ImportJob(
            id=uuid.uuid4(),
            user_id=user_id,
            status=ImportJobStatus.QUEUED,
            source_type=SourceType.LINK,
            source_details={"source_url": source_url},
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        await self.import_repository.insert_import_job(import_job, self.db)

        # enqueue celery task
        copy_from_s3_link.delay(str(import_job.id), source_url)  # type: ignore

        return import_job

    async def complete_link_upload(self, user_id, data: dict):
        # fetch the job by ID
        job = await self.import_repository.get_import_job_by_id(data["job_id"], self.db)
        if not job or job.user_id != user_id:
            raise HTTPException(status_code=404, detail="Import job not found")

        # pylance issue, not runtime error
        job.status = ImportJobStatus.COMPLETED  # type: ignore
        job.updated_at = datetime.now(timezone.utc)  # type: ignore
        await self.import_repository.update_import_job(job, self.db)

        # add File entry
        file = File(
            id=uuid.uuid4(),
            import_job_id=job.id,
            original_filename=data["original_filename"],
            s3_key=data["s3_key"],
            size=data["size"],
            uploaded_at=datetime.now(timezone.utc)
        )
        await self.import_repository.insert_file(file, self.db)

        return job

    async def get_import_job_status(self, job_id, user_id):
        job = await self.import_repository.get_import_job_by_id(job_id, self.db)
        if not job or job.user_id != user_id:
            raise HTTPException(status_code=404, detail="Import job not found")

        try:
            status = ImportJobStatus(job.status).value
        except ValueError:
            status = ImportJobStatus.IN_PROGRESS.value

        files_processed = len(job.files) if job.files else 0
        total_files = getattr(job, "total_files", files_processed)

        return {
            "job_id": str(job.id),
            "status": status,
            "progress_percentage": job.progress_percentage or 0,
            "details": {
                "files_processed": files_processed,
                "total_files": total_files,
                "error_message": None
            },
            "created_at": job.created_at.isoformat() if isinstance(job.created_at, datetime) else None,
            "updated_at": job.updated_at.isoformat() if isinstance(job.updated_at, datetime) else None
        }
