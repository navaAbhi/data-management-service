from pydantic import BaseModel


class LocalUploadCompleteRequest(BaseModel):
    s3_key: str
    original_filename: str
    size: int
