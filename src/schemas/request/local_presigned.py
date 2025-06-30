from pydantic import BaseModel

class FileLocalPreesignedRequest(BaseModel):
    url: str
    content_type: str
    size: int