import re

DATE_PATTERN = (
    r"\b(?:"
    r"\d{2}[/-]\d{2}[/-]\d{4}"                 # 20/07/2026 atau 20-07-2026
    r"|"
    r"\d{4}-\d{2}-\d{2}"                       # 2026-07-20
    r"|"
    r"\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|"
    r"January|February|March|April|May|June|July|August|"
    r"September|October|November|December)\s\d{4}"
    r")\b"
)

def detect_date(text: str):
    entities = []
    for match in re.finditer(DATE_PATTERN, text):
        entities.append({
            "start": match.start(),
            "end": match.end(),
            "text": match.group(),
            "entity_type": "DATE"
        })
    return entities

def redact_date(text: str):
    return re.sub(DATE_PATTERN, "[DATE]", text)

if __name__ == "__main__":
    print("=" * 50)
    print("Detected Date")
    print("=" * 50)

    print("=" * 50)
    print("Redacted Text")
    print("=" * 50)