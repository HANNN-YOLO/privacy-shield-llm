from app.utils.validator import validate_text
from app.services.detectors.email_detector import redact_email

def redact_text(text: str) -> str:
    text = validate_text(text)
    text = redact_email(text)
    return text