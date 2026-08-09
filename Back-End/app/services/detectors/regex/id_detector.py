import re

ID_PATTERNS = [

    # ==========================================
    # PATIENT IDENTIFIERS
    # ==========================================

    # Patient ID
    r"\b(?:PAT|PID)[- ]?\d{3,10}\b",

    # Medical Record Number
    r"\bMRN[- ]?\d{3,12}\b",

    # Unit Record
    r"\bUR[- ]?\d{3,12}\b",

    # Medical ID
    r"\bMED[- ]?\d{3,12}\b",

    # Patient IHS / SATUSEHAT
    r"\bP\d{11}\b",


    # ==========================================
    # INDONESIA IDENTIFIERS
    # ==========================================

    # NIK
    r"\bNIK[:\s-]*\d{16}\b",

    # KK
    r"\b(?:KK|Kartu\s+Keluarga)[:\s-]*\d{16}\b",

    # Passport
    r"\b(?:PASPOR|PASSPORT)[\s]*(?:NO|NUMBER|ID)?[:\s-]*[A-Z0-9]{6,15}\b",

    # KITAS / KITAP
    r"\b(?:KITAS|KITAP)[:\s-]*[A-Z0-9./-]{5,20}\b",


    # ==========================================
    # INSURANCE
    # ==========================================

    # Insurance ID
    r"\b(?:INS|INSURANCE)[- ]?(?:ID)?[:\s-]*[A-Z0-9]{4,20}\b",

    # Member ID
    r"\b(?:MEMBER|MEM)[- ]?(?:ID|NO|NUMBER)?[:\s-]*[A-Z0-9]{4,20}\b",

    # Subscriber ID
    r"\b(?:SUB|SUBSCRIBER)[- ]?(?:ID|NO|NUMBER)?[:\s-]*[A-Z0-9]{4,20}\b",

    # Policy Number
    r"\b(?:POL|POLICY)[- ]?(?:ID|NO|NUMBER)?[:\s-]*[A-Z0-9]{4,20}\b",


    # ==========================================
    # PROFESSIONAL IDENTIFIERS
    # ==========================================

    # Provider ID
    r"\b(?:PRV|PROVIDER)[- ]?(?:ID|NO|NUMBER)?[:\s-]*[A-Z0-9]{4,20}\b",

    # Practitioner ID
    r"\b(?:PRA|PRACTITIONER)[- ]?(?:ID|NO|NUMBER)?[:\s-]*[A-Z0-9]{4,20}\b",

    # STR Indonesia
    r"\b(?:STR|S\.T\.R\.)[:\s-]*[A-Z0-9./-]{6,30}\b",


    # ==========================================
    # CLINICAL IDENTIFIERS
    # ==========================================

    # Accession ID
    r"\b(?:ACC|ACCN|ACCESSION)[- ]?(?:ID|NO|NUMBER)?[:\s-]*[A-Z0-9-]{4,20}\b",

    # Specimen ID
    r"\b(?:SPEC|SPECIMEN)[- ]?(?:ID|NO|NUMBER)?[:\s-]*[A-Z0-9-]{4,20}\b",

    # Order ID
    r"\b(?:ORD|ORDER)[- ]?(?:ID|NO|NUMBER)?[:\s-]*[A-Z0-9-]{4,20}\b",

    # Encounter ID
    r"\b(?:ENC|ENCOUNTER)[- ]?(?:ID|NO|NUMBER)?[:\s-]*[A-Z0-9-]{4,20}\b",

    # Visit ID
    r"\b(?:VIS|VISIT)[- ]?(?:ID|NO|NUMBER)?[:\s-]*[A-Z0-9-]{4,20}\b",

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