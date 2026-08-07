from fastapi import APIRouter
from app.schemas.request import RedactRequest
from app.schemas.response import RedactResponse
from app.services.restore_service import restore_text

router = APIRouter()

@router.get("/")
def home():
    return {
        "message": "Privacy Shield LLM API Running version restore"
    }

@router.post("/restore", response_model=RedactResponse)
def redact(request: RedactRequest):
    result = restore_text(request.text)
    return RedactResponse(
        success=True,
        redacted_text=result
    )