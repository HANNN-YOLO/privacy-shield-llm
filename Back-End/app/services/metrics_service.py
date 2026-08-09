from typing import Iterable


# ==========================================
# ENTITY TYPE MAPPING
# ==========================================

ENTITY_GROUPS = {
    "PATIENT": "person",
    "DOCTOR": "person",
    "PERSON": "person",

    "EMAIL": "email",
    "PHONE": "phone",
    "ID": "id",
    "ADDRESS": "address",
    "DATE": "date",
}


# ==========================================
# EMPTY COUNTER
# ==========================================

def empty_entity_counts() -> dict:
    return {
        "person": 0,
        "email": 0,
        "phone": 0,
        "id": 0,
        "address": 0,
        "date": 0,
    }


# ==========================================
# COUNT FINAL ENTITIES
# ==========================================

def count_entities(
    entities: Iterable[dict],
) -> dict:

    counts = empty_entity_counts()

    for entity in entities:

        entity_type = entity.get(
            "entity_type",
            ""
        ).upper()

        group = ENTITY_GROUPS.get(
            entity_type
        )

        if group is None:
            continue

        counts[group] += 1

    return counts


# ==========================================
# TOTAL ENTITY
# ==========================================

def calculate_total(
    counts: dict,
) -> int:

    return sum(
        counts.values()
    )


# ==========================================
# REDACT METRICS
# ==========================================

def build_redact_metrics(
    entities: Iterable[dict],
    processing_time_ms: float,
) -> dict:

    counts = count_entities(
        entities
    )

    total = calculate_total(
        counts
    )

    return {
        "entity_counts": counts,

        "total_entities": total,

        "processing_time_ms": round(
            processing_time_ms,
            2
        ),
    }


# ==========================================
# RESTORE METRICS
# ==========================================

def build_restore_metrics(
    restored_entities: Iterable[str],
    processing_time_ms: float,
) -> dict:

    counts = empty_entity_counts()

    for entity_type in restored_entities:

        entity_type = entity_type.upper()

        group = ENTITY_GROUPS.get(
            entity_type
        )

        if group is None:
            continue

        counts[group] += 1

    total = calculate_total(
        counts
    )

    return {
        "entity_counts": counts,

        "total_entities": total,

        "processing_time_ms": round(
            processing_time_ms,
            2
        ),
    }