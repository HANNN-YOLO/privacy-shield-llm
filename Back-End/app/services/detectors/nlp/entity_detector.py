from app.providers.spacy_provider import get_nlp

ENTITY_MAPPING = {
    "PERSON": "[PERSON]",
    "ORG": "[ORG]",
    "GPE": "[ADDRESS]",
    "LOC": "[ADDRESS]",
    "DATE": "[DATE]"
}


def redact_entities(text: str) -> str:
    nlp = get_nlp()

    doc = nlp(text)

    entities = sorted(
        doc.ents,
        key=lambda entity: entity.start_char,
        reverse=True
    )

    redacted_text = text

    for entity in entities:
        replacement = ENTITY_MAPPING.get(entity.label_)
        if replacement:
            redacted_text = (
                redacted_text[:entity.start_char]
                + replacement
                + redacted_text[entity.end_char:]
            )
    return redacted_text