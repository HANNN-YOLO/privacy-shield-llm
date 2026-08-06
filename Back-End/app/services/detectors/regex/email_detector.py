import re

EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

def detect_email(text: str):
    entities = []
    for match in re.finditer(EMAIL_PATTERN, text):
        entities.append({
            "start": match.start(),
            "end": match.end(),
            "text": match.group(),
            "entity_type": "EMAIL"
        })
    return entities


def redact_email(text: str):
    return re.sub(EMAIL_PATTERN, "[EMAIL]", text)

if __name__ == "__main__":

    print("=" * 50)
    print("Detected Email")
    print("=" * 50)

    print("\n")

    print("=" * 50)
    print("Redacted Text")
    print("=" * 50)