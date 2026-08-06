from presidio_analyzer import RecognizerResult

CUSTOM = {
    "PATIENT",
    "DOCTOR",
    "ADDRESS"
}

REGEX = {
    "EMAIL",
    "PHONE",
    "DATE",
    "ID"
}

def source_priority(entity_type: str):

    if entity_type in CUSTOM:
        return 3

    if entity_type in REGEX:
        return 2

    return 1


def resolve_entities(
    entities: list[RecognizerResult]
):

    entities = sorted(
        entities,
        key=lambda e: (
            e.start,
            e.end
        )
    )

    resolved = []

    for entity in entities:

        replaced = False

        for i, existing in enumerate(resolved):

            overlap = (
                entity.start < existing.end
                and
                entity.end > existing.start
            )

            if not overlap:
                continue

            current_source = source_priority(
                entity.entity_type
            )

            existing_source = source_priority(
                existing.entity_type
            )

            # =====================================
            # CASE 1
            # Span sama
            # =====================================

            if (
                entity.start == existing.start
                and
                entity.end == existing.end
            ):

                if current_source > existing_source:

                    resolved[i] = entity

                elif current_source == existing_source:

                    # entity terakhir menang
                    resolved[i] = entity

                replaced = True
                break

            # =====================================
            # CASE 2
            # Span berbeda
            # =====================================

            if current_source > existing_source:

                resolved[i] = entity

            elif current_source == existing_source:

                current_len = (
                    entity.end - entity.start
                )

                existing_len = (
                    existing.end - existing.start
                )

                if current_len > existing_len:

                    resolved[i] = entity

            replaced = True
            break

        if not replaced:

            resolved.append(entity)

    return sorted(
        resolved,
        key=lambda e: e.start
    )