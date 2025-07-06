from pydantic import BaseModel


class LinkUploadRequest(BaseModel):
    source_url: str
    destination_path: str
