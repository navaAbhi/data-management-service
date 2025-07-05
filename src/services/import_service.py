import uuid
from datetime import datetime, timezone
from src.models.file import File
from src.models.import_job import ImportJob
from src.repository.import_repository import ImportRepository
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
        # create ImportJob
        import_job = ImportJob(
            id=uuid.uuid4(),
            user_id=user_id,
            status="COMPLETED",
            source_type="local",
            source_path=data["original_filename"],
            destination_path=data["s3_key"],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        await self.import_repository.insert_import_job(import_job, self.db)

        # create File tied to ImportJob
        file = File(
            id=uuid.uuid4(),
            import_job_id=import_job.id,
            original_filename=data["original_filename"],
            s3_key=data["s3_key"],
            size=data["size"],
            uploaded_at=datetime.now(timezone.utc)
        )
        await self.import_repository.insert_file(file, self.db)

        return import_job
