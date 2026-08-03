from presidio_analyzer import RecognizerResult
from app.services.detectors.nlp.patient_detector import classify_patient
from app.services.detectors.nlp.doctor_detector import classify_doctor
from app.services.detectors.nlp.address_detector import detect_address
from app.services.detectors.nlp.context_detector import detect_context


def process_entities(
    text: str,
    analyzer_results: list[RecognizerResult]
) -> list[RecognizerResult]:

    custom_entities = []

    custom_entities.extend(
        classify_patient(
            text,
            analyzer_results
        )
    )

    custom_entities.extend(
        classify_doctor(
            text,
            analyzer_results
        )
    )

    custom_entities.extend(
        detect_address(
            text,
            analyzer_results
        )
    )

    custom_entities.extend(
        detect_context(
            text,
            analyzer_results
        )
    )

    return custom_entities