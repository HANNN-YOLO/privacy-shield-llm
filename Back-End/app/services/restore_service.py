import re

from time import perf_counter

from app.services.redis.mapping_service import (
    MappingService
)

from app.services.metrics_service import (
    build_restore_metrics
)


# ======================================================
# SERVICE INSTANCE
# ======================================================

mapping_service = MappingService()


# ======================================================
# TOKEN → ENTITY TYPE
# ======================================================

def get_entity_type(
    token: str
) -> str | None:

    """
    Extract entity type from token.

    Example:

    PATIENT_001 → PATIENT
    DOCTOR_002  → DOCTOR
    EMAIL_001   → EMAIL
    PHONE_001   → PHONE
    ADDRESS_001 → ADDRESS
    DATE_001    → DATE
    ID_001      → ID
    """

    match = re.match(
        r"^([A-Z]+)_\d+$",
        token
    )

    if not match:
        return None

    return match.group(1)


# ======================================================
# FIND TOKENS
# ======================================================

def extract_tokens(
    text: str
) -> list[str]:

    """
    Find all pseudonymization tokens
    inside the text.

    Example:

    [PATIENT_001]
    [EMAIL_001]
    [PHONE_001]

    Returns unique tokens while
    preserving first appearance.
    """

    tokens = re.findall(
        r"\[([A-Z]+_\d+)\]",
        text
    )

    return list(
        dict.fromkeys(tokens)
    )


# ======================================================
# RESTORE TEXT
# ======================================================

def restore_text(
    text: str
) -> dict:

    """
    Restore pseudonymized text
    using mappings stored in Redis.
    """

    # ==============================================
    # START TIMER
    # ==============================================

    start_time = perf_counter()


    # ==============================================
    # EXTRACT TOKENS
    # ==============================================

    tokens = extract_tokens(
        text
    )


    # ==============================================
    # NO TOKEN
    # ==============================================

    if not tokens:

        processing_time_ms = (
            perf_counter() - start_time
        ) * 1000

        metrics = build_restore_metrics(
            [],
            processing_time_ms
        )

        return {

            "restored_text": text,

            "entity_counts": metrics[
                "entity_counts"
            ],

            "total_entities": metrics[
                "total_entities"
            ],

            "processing_time_ms": metrics[
                "processing_time_ms"
            ],

        }


    # ==============================================
    # MAPPING SERVICE
    # ==============================================

    mappings = mapping_service.restore_tokens(
        tokens
    )


    # ==============================================
    # RESTORE TEXT
    # ==============================================

    restored_text = text


    # ==============================================
    # COLLECT RESTORED ENTITIES
    # ==============================================

    restored_entities = []


    # ==============================================
    # REPLACE TOKEN
    # ==============================================

    for token in tokens:

        original = mappings.get(
            token
        )


        # ==========================================
        # TOKEN NOT FOUND
        # ==========================================

        if original is None:
            continue


        # ==========================================
        # GET ENTITY TYPE
        # ==========================================

        entity_type = get_entity_type(
            token
        )


        if entity_type is not None:

            restored_entities.append(
                entity_type
            )


        # ==========================================
        # RESTORE TOKEN
        # ==========================================

        restored_text = restored_text.replace(

            f"[{token}]",

            original

        )


    # ==============================================
    # PROCESSING TIME
    # ==============================================

    processing_time_ms = (

        perf_counter() - start_time

    ) * 1000


    # ==============================================
    # METRICS SERVICE
    # ==============================================

    metrics = build_restore_metrics(

        restored_entities,

        processing_time_ms

    )


    # ==============================================
    # RETURN RESULT
    # ==============================================

    return {

        "restored_text": restored_text,

        "entity_counts": metrics[
            "entity_counts"
        ],

        "total_entities": metrics[
            "total_entities"
        ],

        "processing_time_ms": metrics[
            "processing_time_ms"
        ],

    }