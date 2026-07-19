from app.utils.validator import validate_text
def redact_text(text: str) -> str:
    text = validate_text(text)
    return text