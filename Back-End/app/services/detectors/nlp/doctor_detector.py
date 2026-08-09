from presidio_analyzer import RecognizerResult
from app.utils.text import clean_entity

DOCTOR_KEYWORDS = {"dr.", "dr", "doctor", "physician", "consultant", "dokter"}

def classify_doctor(text: str, entities: list[RecognizerResult]):
    results = []

    for entity in entities:
        if entity.entity_type != "PERSON":
            continue

        # Ambil token/kata TERAKHIR tepat sebelum posisi entitas
        text_before = text[:entity.start].strip()
        tokens = text_before.split()
        last_token = tokens[-1].lower().strip(".,;:!") if tokens else ""

        # HANYA tetapkan sebagai DOCTOR jika kata tepat di sebelahnya adalah keyword dokter
        if last_token in DOCTOR_KEYWORDS:
            value, start, end = clean_entity(text, entity.start, entity.end)

            results.append(
                RecognizerResult(
                    entity_type="DOCTOR",
                    start=start,
                    end=end,
                    score=entity.score
                )
            )

    return results