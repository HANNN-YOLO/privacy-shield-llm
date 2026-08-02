from fastapi import APIRouter
from app.schemas.request import RedactRequest
from app.services.detectors.nlp.presidio_detector import detect_pii

router = APIRouter()

@router.post("/presidio-test")
def presidio_test(request: RedactRequest):

    results = detect_pii(request.text)

    response = []

    for result in results:
        response.append({
            "entity": result.entity_type,
            "start": result.start,
            "end": result.end,
            "score": round(result.score, 3)
        })

    return {
        "success": True,
        "entities": response
    }