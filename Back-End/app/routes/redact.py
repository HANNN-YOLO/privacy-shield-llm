from fastapi import APIRouter

from app.schemas.request import RedactRequest
from app.schemas.response import (
    RedactResponse,
    EntityCounts,
)

from app.services.redact_service import redact_text


router = APIRouter()


@router.post(
    "/redact",
    response_model=RedactResponse
)
def redact(
    request: RedactRequest
):

    result = redact_text(
        request.text
    )

    return RedactResponse(
        success=True,

        redacted_text=result[
            "redacted_text"
        ],

        entity_counts=EntityCounts(
            **result["entity_counts"]
        ),

        total_entities=result[
            "total_entities"
        ],

        processing_time_ms=result[
            "processing_time_ms"
        ],
    )