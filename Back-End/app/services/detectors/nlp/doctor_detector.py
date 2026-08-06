from presidio_analyzer import RecognizerResult
from app.utils.text import clean_entity

DOCTOR_KEYWORDS = [
    "dr.",
    "dr ",
    "doctor ",
    "Doctor ",
    "physician",
    "consultant"
]

def classify_doctor(text: str, entities: list[RecognizerResult]):
    results = []
    for entity in entities:
        if entity.entity_type != "PERSON":
            continue
        before = text[max(0, entity.start - 30):entity.start].lower()

        if not any(keyword in before for keyword in DOCTOR_KEYWORDS):
                continue
        
                
        value, start, end = clean_entity(
        text,
        entity.start,
        entity.end
        )

        results.append(
            RecognizerResult(
                entity_type="DOCTOR",
                start=start,
                end=end,
                score=entity.score
            )
        )
    return results