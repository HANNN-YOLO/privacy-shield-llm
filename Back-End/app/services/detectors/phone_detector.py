import re

PHONE_PATTERN = (
    r"\b(?:\+62|62|0)"
    r"(?:[\s-]?\d){8,13}\b"
)

def detect_phone(text: str):
    return re.findall(PHONE_PATTERN, text)

def redact_phone(text: str):
    return re.sub(PHONE_PATTERN, "[PHONE]", text)

if __name__ == "__main__":
    print("=" * 50)
    print("Detected Phone")
    print("=" * 50)

    print("=" * 50)
    print("Redacted Text")
    print("=" * 50)