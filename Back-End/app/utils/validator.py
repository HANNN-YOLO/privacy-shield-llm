def validate_text(text: str) -> str:
    if not text:
        raise ValueError("Text cannot be empty.")
    text = text.strip()
    if len(text) == 0:
        raise ValueError("Text cannot contain only whitespace.")
    return text