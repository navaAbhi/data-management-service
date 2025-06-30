from fastapi import APIRouter, Depends, Request, Response

from src.schemas.request.local_presigned import FileLocalPreesignedRequest
from src.utils.get_current_user import get_current_user

router = APIRouter(
    prefix="/import",
    tags=["core"],
)

@router.post("/import/local/presigned-url")
async def upload_local_large_file(request: FileLocalPreesignedRequest, response: Response, user=Depends(get_current_user)):
    return