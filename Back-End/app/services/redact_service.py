from app.utils.validator import validate_text
from app.services.detectors.regex.email_detector import redact_email
from app.services.detectors.regex.phone_detector import redact_phone
from app.services.detectors.regex.date_detector import redact_date
from app.services.detectors.regex.id_detector import redact_id
from app.services.detectors.nlp.entity_detector import redact_entities

PIPELINE = [
    redact_email,
    redact_phone,
    redact_date,
    redact_id,
    redact_entities
]

def redact_text(text: str) -> str:
    text = validate_text(text)

    for detector in PIPELINE:
        text = detector(text)

    return text