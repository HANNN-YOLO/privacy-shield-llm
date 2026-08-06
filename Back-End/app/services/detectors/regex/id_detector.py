import re

ID_PATTERNS = [
    # Patient ID
    r"\bPAT[- ]?\d{3,10}\b",

    # Medical Record Number
    r"\bMRN[- ]?\d{3,10}\b",

    # Medical ID
    r"\bMED[- ]?\d{3,10}\b",

    # Employee ID
    r"\bEMP[- ]?\d{3,10}\b",

    # Insurance ID
    r"\bINS[- ]?\d{3,10}\b",

    # Generic ID
    r"\bID[- ]?\d{3,10}\b"

    # Numeric Identifier
    # r"\b\d{8,16}\b"
]

def detect_id(text: str):
    entities = []
    for pattern in ID_PATTERNS:
        for match in re.finditer(pattern, text):
            entities.append({
                "start": match.start(),
                "end": match.end(),
                "text": match.group(),
                "entity_type": "ID"
            })
    return entities

def redact_id(text: str):
    for pattern in ID_PATTERNS:
        text = re.sub(pattern, "[ID]", text)
    return text

if __name__ == "__main__":
    print("="*50)
    print("Detected ID")
    print("="*50)

    print("="*50)
    print("Redacted")
    print("="*50)