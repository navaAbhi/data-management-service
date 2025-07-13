from pydantic import BaseModel


class LinkUploadRequest(BaseModel):
    source_url: str
