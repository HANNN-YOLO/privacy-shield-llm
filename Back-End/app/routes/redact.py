from fastapi import APIRouter
from app.schemas.request import RedactRequest
from app.schemas.response import RedactResponse
from app.services.redact_service import redact_text

router = APIRouter()

@router.get("/")
def home():
    return {
        "message": "Privacy Shield LLM API Running"
    }

@router.post("/redact", response_model=RedactResponse)

def redact(request: RedactRequest):
    result = redact_text(request.text)
    return RedactResponse(
        success=True,
        redacted_text=result
    )