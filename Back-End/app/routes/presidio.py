from fastapi import APIRouter
from app.schemas.request import RedactRequest
from app.services.detectors.nlp.presidio_detector import detect_pii
from app.services.detectors.nlp.patient_detector import classify_patient
from app.services.detectors.nlp.doctor_detector import classify_doctor
from app.services.detectors.nlp.address_detector import detect_address
from app.services.detectors.nlp.context_detector import detect_context

router = APIRouter()

@router.post("/presidio-test")
def presidio_test(request: RedactRequest):

    results = detect_pii(request.text)

    patient = classify_patient(
        request.text,
        results
    )

    doctor = classify_doctor(
        request.text,
        results
    )

    address = detect_address(
        request.text,
        results
    )

    context = detect_context(
        request.text,
        results
    )

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
        "entities": response,
        "patient" : patient,
        "doctor" : doctor,
        "address": address,
        "context": context
    }