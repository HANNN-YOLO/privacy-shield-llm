from presidio_analyzer import RecognizerResult

PRIORITY = {
    "PATIENT": 100,
    "DOCTOR": 100,
    "ADDRESS": 100,

    "PERSON": 50,
    "LOCATION": 50,
    "GPE": 50,

    "EMAIL_ADDRESS": 80,
    "PHONE_NUMBER": 80,
    "DATE_TIME": 80,
    "URL": 80
}


def resolve_entities(
    entities: list[RecognizerResult]
) -> list[RecognizerResult]:

    resolved = []

    # urutkan berdasarkan posisi
    entities = sorted(
        entities,
        key=lambda x: (x.start, x.end)
    )

    for entity in entities:
        duplicated = False
        for i, existing in enumerate(resolved):
            same_span = (
                entity.start == existing.start
                and
                entity.end == existing.end
            )

            if not same_span:
                continue

            duplicated = True

            current_priority = PRIORITY.get(
                entity.entity_type,
                0
            )

            existing_priority = PRIORITY.get(
                existing.entity_type,
                0
            )

            if current_priority > existing_priority:
                resolved[i] = entity

            break

        if not duplicated:
            resolved.append(entity)

    return resolved