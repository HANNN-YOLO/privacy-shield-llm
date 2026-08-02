from presidio_analyzer import RecognizerResult

DOCTOR_KEYWORDS = [
    "dr.",
    "dr ",
    "doctor ",
    "Doctor "
]

def classify_doctor(text: str, entities: list[RecognizerResult]):
    results = []
    for entity in entities:
        if entity.entity_type != "PERSON":
            continue
        before = text[max(0, entity.start - 30):entity.start].lower()

        if any(keyword in before for keyword in DOCTOR_KEYWORDS):
            results.append({
                "entity": "DOCTOR",
                "text": text[entity.start:entity.end],
                "start": entity.start,
                "end": entity.end,
                "score": entity.score
            })
    return results