from presidio_analyzer import RecognizerResult

def classify_patient(text: str, entities: list[RecognizerResult]):
    results = []

    for entity in entities:
        if entity.entity_type != "PERSON":
            continue
        before = text[max(0, entity.start - 30):entity.start].lower()
        if "patient" in before:
            results.append(
                RecognizerResult(
                    entity_type="PATIENT",
                    start=entity.start,
                    end=entity.end,
                    score=entity.score
                )
            )
    return results