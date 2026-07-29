from app.utils.validator import validate_text
from app.services.detectors.email_detector import redact_email
from app.services.detectors.phone_detector import redact_phone

def redact_text(text: str) -> str:
    text = validate_text(text)
    text = redact_email(text)
    text = redact_phone(text)
    return text