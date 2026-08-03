from presidio_analyzer import RecognizerResult

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


# ===========================
# Context Detector
# ===========================

def detect_context(
    text: str,
    results: list[RecognizerResult]
):

    context_entities = []
    for entity in results:

        # Day 6 hanya fokus PERSON
        if entity.entity_type != "PERSON":
            continue

        # Ambil context sekitar entity
        before = text[
            max(0, entity.start - 40):entity.start
        ].lower()

        after = text[
            entity.end:min(len(text), entity.end + 40)
        ].lower()

        context = before + " " + after

        # ===========================
        # Ignore Medical Term
        # ===========================

        if any(term in context for term in MEDICAL_TERMS):
            continue

        # ===========================
        # Doctor
        # ===========================

        if any(keyword in context for keyword in DOCTOR_KEYWORDS):
            context_entities.append(
                RecognizerResult(
                    entity_type="DOCTOR",
                    start=entity.start,
                    end=entity.end,
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
                    start=entity.start,
                    end=entity.end,
                    score=entity.score
                )
            )
            continue
    return context_entities