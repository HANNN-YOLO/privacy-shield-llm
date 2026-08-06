from presidio_analyzer import RecognizerResult
from app.utils.text import clean_entity

PATIENT_KEYWORDS = [
    "patient",
    "mr.",
    "mrs.",
    "miss",
    "name",
    "admitted"
]

DOCTOR_KEYWORDS = [
    "doctor",
    "dr.",
    "dr ",
    "physician",
    "consultant"
]

MEDICAL_TERMS = [
    "disease",
    "syndrome",
    "disorder",
    "infection",
    "cancer",
    "diabetes",
    "hypertension",
    "parkinson",
    "alzheimer"
]


def detect_context(
    text: str,
    results: list[RecognizerResult]
):

    context_entities = []

    for entity in results:

        if entity.entity_type != "PERSON":
            continue

        before = text[
            max(0, entity.start - 40):entity.start
        ].lower()

        after = text[
            entity.end:min(len(text), entity.end + 40)
        ].lower()

        context = before + " " + after

        # Ignore medical terms
        if any(term in context for term in MEDICAL_TERMS):
            continue

        # Bersihkan entity sekali saja
        value, start, end = clean_entity(
            text,
            entity.start,
            entity.end
        )

        # ===========================
        # Doctor
        # ===========================

        if any(keyword in context for keyword in DOCTOR_KEYWORDS):

            context_entities.append(
                RecognizerResult(
                    entity_type="DOCTOR",
                    start=start,
                    end=end,
                    score=entity.score
                )
            )

            continue

        # ===========================
        # Patient
        # ===========================

        if any(keyword in context for keyword in PATIENT_KEYWORDS):

            context_entities.append(
                RecognizerResult(
                    entity_type="PATIENT",
                    start=start,
                    end=end,
                    score=entity.score
                )
            )

            continue

    return context_entities