from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.schemas.request.link_upload import LinkUploadRequest
from src.schemas.request.link_upload_complete import LinkUploadCompleteRequest
from src.schemas.request.local_presigned import FileLocalPresignedRequest
from src.schemas.request.local_upload_complete import LocalUploadCompleteRequest
from src.services.import_service import ImportService
from src.utils.get_current_user import get_current_user

router = APIRouter(
    prefix="/import",
    tags=["imports"],
)


@router.get("/{job_id}")
async def get_import_job_status(job_id: str, response: Response, user=Depends(get_current_user)):
    """Retrieves the current status and progress of a specific import job."""
    return None


@router.get("")
async def list_import_jobs(response: Response, user=Depends(get_current_user)):
    """Lists recent import jobs initiated by the current user, with pagination."""
    return None


@router.post("/local/presigned-url")
async def upload_local_large_file(request: FileLocalPresignedRequest, response: Response, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    """Generates a presigned URL for uploading a large local file directly to S3."""
    service = ImportService(db)
    presigned_data = await service.generate_presigned_post(
        filename=request.filename,
        content_type=request.content_type,
        size=request.size,
        user_id=user.id
    )
    return {"presigned": presigned_data}


@router.post("/local/complete")
async def complete_upload(request: LocalUploadCompleteRequest, response: Response, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    """Marks the local file upload as complete and stores metadata."""
    service = ImportService(db)
    job = await service.complete_local_upload(
        user_id=user.id,
        data=request.dict()
    )
    return {
        "job_id": str(job.id),
        "status": job.status
    }


@router.post("/cloud")
async def cloud_upload(response: Response, user=Depends(get_current_user)):
    """Initiates an import from a connected cloud storage provider (like GDrive or Dropbox)."""
    return None


@router.post("/cloud/complete")
async def complete_cloud_upload(response: Response, user=Depends(get_current_user)):
    """Finalizes the cloud import process and stores metadata."""
    return None


@router.post("/link")
async def link_upload(request_data: LinkUploadRequest, response: Response, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    """Accepts a direct file URL to import from (via HTTP or S3 link)."""
    service = ImportService(db)
    job = await service.start_link_import(
        user_id=user.id,
        source_url=request_data.source_url,
        destination_path=request_data.destination_path
    )
    return {
        "job_id": str(job.id),
        "status": job.status
    }


@router.post("/link/complete")
async def complete_link_upload(request_data: LinkUploadCompleteRequest, response: Response, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    """Marks the link-based import as complete and stores metadata."""
    service = ImportService(db)
    job = await service.complete_link_upload(
        user_id=user.id,
        data=request_data.dict()
    )
    return {
        "job_id": str(job.id),
        "status": job.status
    }


@router.post("/metadata")
async def store_import_metadata(response: Response, user=Depends(get_current_user)):
    """Stores metadata for the uploaded data by the user."""
    return None
