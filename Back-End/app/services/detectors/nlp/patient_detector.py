from presidio_analyzer import RecognizerResult
from app.utils.text import clean_entity

PATIENT_KEYWORDS = {"patient", "pasien"}
DOCTOR_KEYWORDS = {"dr.", "dr", "doctor", "physician", "consultant", "dokter"}

def classify_patient(text: str, entities: list[RecognizerResult]):
    results = []

    for entity in entities:
        if entity.entity_type != "PERSON":
            continue

        # Ambil token/kata TERAKHIR tepat sebelum posisi entitas
        text_before = text[:entity.start].strip()
        tokens = text_before.split()
        last_token = tokens[-1].lower().strip(".,;:!") if tokens else ""

        # Abaikan jika token tepat di sebelahnya adalah keyword Dokter
        if last_token in DOCTOR_KEYWORDS:
            continue

        # Masuk sebagai PATIENT jika:
        # 1. Ada keyword Patient persis di sebelahnya, ATAU
        # 2. Tidak ada keyword Dokter sama sekali (default behavior)
        value, start, end = clean_entity(text, entity.start, entity.end)

        results.append(
            RecognizerResult(
                entity_type="PATIENT",
                start=start,
                end=end,
                score=entity.score
            )
        )

    return results