from presidio_analyzer import RecognizerResult


# ======================================================
# ENTITY GROUPS
# ======================================================

# ------------------------------------------------------
# REGEX ENTITY
# ------------------------------------------------------

REGEX_ENTITIES = {
    "EMAIL",
    "PHONE",
    "DATE",
    "ID",
}


# ------------------------------------------------------
# CUSTOM NLP ENTITY
# ------------------------------------------------------

CUSTOM_ENTITIES = {
    "PATIENT",
    "DOCTOR",
    "ADDRESS",
}


# ------------------------------------------------------
# PRESIDIO GENERIC ENTITY
# ------------------------------------------------------

PRESIDIO_PERSON = {
    "PERSON",
}


PRESIDIO_ADDRESS = {
    "LOCATION",
    "LOC",
    "GPE",
    "FAC",
}


PRESIDIO_EMAIL = {
    "EMAIL_ADDRESS",
}


PRESIDIO_PHONE = {
    "PHONE_NUMBER",
    "PHON_NUMBER",
}


PRESIDIO_DATE = {
    "DATE_TIME",
}


# ======================================================
# SOURCE PRIORITY
# ======================================================

def source_priority(
    entity_type: str
) -> int:

    entity_type = entity_type.upper()

    # ==================================================
    # PRIORITY 4
    # REGEX
    #
    # Regex lebih spesifik daripada Presidio generic
    # ==================================================

    if entity_type in REGEX_ENTITIES:
        return 4

    # ==================================================
    # PRIORITY 3
    # CUSTOM NLP
    #
    # PATIENT
    # DOCTOR
    # ADDRESS
    # ==================================================

    if entity_type in CUSTOM_ENTITIES:
        return 3

    # ==================================================
    # PRIORITY 1
    # PRESIDIO GENERIC
    # ==================================================

    if entity_type in PRESIDIO_PERSON:
        return 1

    if entity_type in PRESIDIO_ADDRESS:
        return 1

    if entity_type in PRESIDIO_EMAIL:
        return 1

    if entity_type in PRESIDIO_PHONE:
        return 1

    if entity_type in PRESIDIO_DATE:
        return 1

    # ==================================================
    # UNKNOWN ENTITY
    # ==================================================

    return 1


# ======================================================
# ENTITY FAMILY
# ======================================================

def get_entity_family(
    entity_type: str
) -> str:

    entity_type = entity_type.upper()

    # --------------------------------------------------
    # PERSON FAMILY
    # --------------------------------------------------

    if entity_type in {
        "PATIENT",
        "DOCTOR",
        "PERSON",
    }:
        return "PERSON"

    # --------------------------------------------------
    # ADDRESS FAMILY
    # --------------------------------------------------

    if entity_type in {
        "ADDRESS",
        "LOCATION",
        "LOC",
        "GPE",
        "FAC",
    }:
        return "ADDRESS"

    # --------------------------------------------------
    # EMAIL FAMILY
    # --------------------------------------------------

    if entity_type in {
        "EMAIL",
        "EMAIL_ADDRESS",
    }:
        return "EMAIL"

    # --------------------------------------------------
    # PHONE FAMILY
    # --------------------------------------------------

    if entity_type in {
        "PHONE",
        "PHONE_NUMBER",
        "PHON_NUMBER",
    }:
        return "PHONE"

    # --------------------------------------------------
    # DATE FAMILY
    # --------------------------------------------------

    if entity_type in {
        "DATE",
        "DATE_TIME",
    }:
        return "DATE"

    # --------------------------------------------------
    # ID FAMILY
    # --------------------------------------------------

    if entity_type == "ID":
        return "ID"

    # --------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------

    return entity_type


# ======================================================
# CHECK OVERLAP
# ======================================================

def is_overlapping(
    current: RecognizerResult,
    existing: RecognizerResult
) -> bool:

    return (
        current.start < existing.end
        and
        current.end > existing.start
    )


# ======================================================
# RESOLVE ENTITIES
# ======================================================

def resolve_entities(
    entities: list[RecognizerResult]
) -> list[RecognizerResult]:

    # ==================================================
    # SORT BY:
    #
    # 1. Priority tinggi
    # 2. Entity lebih panjang
    # 3. Score lebih tinggi
    # ==================================================

    sorted_entities = sorted(
        entities,
        key=lambda entity: (
            source_priority(
                entity.entity_type
            ),

            entity.end - entity.start,

            entity.score
        ),
        reverse=True
    )

    resolved = []

    # ==================================================
    # PROCESS ENTITY
    # ==================================================

    for entity in sorted_entities:

        current_type = (
            entity.entity_type.upper()
        )

        current_family = get_entity_family(
            current_type
        )

        entity_accepted = True

        # ==================================================
        # COMPARE WITH ACCEPTED ENTITIES
        # ==================================================

        for existing in resolved:

            existing_type = (
                existing.entity_type.upper()
            )

            existing_family = get_entity_family(
                existing_type
            )

            # --------------------------------------------------
            # Tidak overlap
            # --------------------------------------------------

            if not is_overlapping(
                entity,
                existing
            ):
                continue

            # ==================================================
            # SPECIAL CASE
            #
            # Entity berada pada family yang sama
            # ==================================================

            if current_family == existing_family:

                current_priority = source_priority(
                    current_type
                )

                existing_priority = source_priority(
                    existing_type
                )

                # --------------------------------------------------
                # Current lebih tinggi
                # --------------------------------------------------

                if current_priority > existing_priority:

                    resolved.remove(
                        existing
                    )

                    break

                # --------------------------------------------------
                # Existing lebih tinggi
                # --------------------------------------------------

                elif current_priority < existing_priority:

                    entity_accepted = False

                    break

                # --------------------------------------------------
                # Priority sama
                # Gunakan entity lebih panjang
                # --------------------------------------------------

                current_length = (
                    entity.end - entity.start
                )

                existing_length = (
                    existing.end - existing.start
                )

                if current_length > existing_length:

                    resolved.remove(
                        existing
                    )

                    break

                elif current_length < existing_length:

                    entity_accepted = False

                    break

                # --------------------------------------------------
                # Length sama
                # Gunakan score
                # --------------------------------------------------

                elif entity.score > existing.score:

                    resolved.remove(
                        existing
                    )

                    break

                else:

                    entity_accepted = False

                    break

            # ==================================================
            # SPECIAL CASE
            #
            # Berbeda family tetapi overlap
            # ==================================================

            else:

                current_priority = source_priority(
                    current_type
                )

                existing_priority = source_priority(
                    existing_type
                )

                # --------------------------------------------------
                # Current priority lebih tinggi
                # --------------------------------------------------

                if current_priority > existing_priority:

                    resolved.remove(
                        existing
                    )

                    break

                # --------------------------------------------------
                # Existing priority lebih tinggi
                # --------------------------------------------------

                else:

                    entity_accepted = False

                    break

        # ==================================================
        # ACCEPT ENTITY
        # ==================================================

        if entity_accepted:

            resolved.append(
                entity
            )

    # ==================================================
    # FINAL SORT
    # Berdasarkan posisi dalam text
    # ==================================================

    return sorted(
        resolved,
        key=lambda entity: entity.start
    )