from app.utils.validator import validate_text
from app.services.detectors.email_detector import redact_email
from app.services.detectors.phone_detector import redact_phone
from app.services.detectors.date_detectors import redact_date
from app.services.detectors.id_detector import redact_id

PIPELINE = [
    redact_email,
    redact_phone,
    redact_date,
    redact_id,
]

def redact_text(text: str) -> str:
    text = validate_text(text)

    for detector in PIPELINE:
        text = detector(text)

    return text