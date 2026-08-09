from fastapi import APIRouter

from app.schemas.request import RestoreRequest

from app.schemas.response import (
    RestoreResponse,
    EntityCounts,
)

from app.services.restore_service import restore_text


# ==========================================
# ROUTER
# ==========================================

router = APIRouter()


# ==========================================
# HOME
# ==========================================

@router.get("/")
def home():

    return {
        "message": "Privacy Shield LLM API Running version restore"
    }


# ==========================================
# RESTORE
# ==========================================

@router.post(
    "/restore",
    response_model=RestoreResponse
)
def restore(
    request: RestoreRequest
):

    result = restore_text(
        request.text
    )

    return RestoreResponse(

        success=True,

        restored_text=result[
            "restored_text"
        ],

        entity_counts=EntityCounts(
            **result[
                "entity_counts"
            ]
        ),

        total_entities=result[
            "total_entities"
        ],

        processing_time_ms=result[
            "processing_time_ms"
        ],
    )