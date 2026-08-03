from app.utils.validator import validate_text

# regex
from app.services.detectors.regex.email_detector import redact_email
from app.services.detectors.regex.phone_detector import redact_phone
from app.services.detectors.regex.date_detector import redact_date
from app.services.detectors.regex.id_detector import redact_id

# presidio
from app.services.detectors.presidio.analyzer import analyze_text
from app.services.detectors.nlp.entitiy_processor import process_entities
from app.services.detectors.presidio.resolver import resolve_entities
from app.services.detectors.presidio.anonymizer import anonymize_text

REGEX_PIPELINE = [
    redact_email,
    redact_phone,
    redact_date,
    redact_id
]


def redact_text(text: str) -> str:
    text = validate_text(text)

    for detector in REGEX_PIPELINE:
        text = detector(text)

    analyzer_results = analyze_text(text)

    custom_entities = process_entities(
        text=text,
        analyzer_results=analyzer_results
    )

    merged_entities = analyzer_results + custom_entities

    final_entities = resolve_entities(
        merged_entities
    )

    redacted_text = anonymize_text(
        text=text,
        entities=final_entities
    )

    return redacted_text