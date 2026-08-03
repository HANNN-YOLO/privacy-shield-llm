from presidio_anonymizer.entities import OperatorConfig

ENTITY_MAPPING = {

    # =============================
    # Custom NLP (Day 4 - Day 6)
    # =============================

    "PATIENT": "[PATIENT]",
    "DOCTOR": "[DOCTOR]",
    "ADDRESS": "[ADDRESS]",

    # =============================
    # Presidio Built-in
    # =============================

    "EMAIL_ADDRESS": "[EMAIL]",
    "PHONE_NUMBER": "[PHONE]",
    "DATE_TIME": "[DATE]",
    "URL": "[URL]",

    # =============================
    # Fallback
    # =============================

    "PERSON": "[PERSON]",
    "LOCATION": "[ADDRESS]",
    "GPE": "[ADDRESS]",
    "LOC": "[ADDRESS]"
}


def get_operator_mapping() -> dict[str, OperatorConfig]:
    operators = {}
    for entity, replacement in ENTITY_MAPPING.items():
        operators[entity] = OperatorConfig(
            operator_name="replace",
            params={
                "new_value": replacement
            }
        )
    return operators