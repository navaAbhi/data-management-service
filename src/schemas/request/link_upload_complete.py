from pydantic import BaseModel


class LinkUploadCompleteRequest(BaseModel):
    s3_key: str
    original_filename: str
    size: int
    job_id: str
