from pydantic import BaseModel


class FileLocalPresignedRequest(BaseModel):
    filename: str
    content_type: str
    size: int
