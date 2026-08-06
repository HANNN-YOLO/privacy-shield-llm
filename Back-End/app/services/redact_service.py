from presidio_analyzer import RecognizerResult

from app.utils.validator import validate_text

# ==========================================
# REGEX DETECTOR
# ==========================================

from app.services.detectors.regex.email_detector import detect_email
from app.services.detectors.regex.phone_detector import detect_phone
from app.services.detectors.regex.date_detector import detect_date
from app.services.detectors.regex.id_detector import detect_id

# ==========================================
# PRESIDIO
# ==========================================

from app.services.detectors.presidio.analyzer import analyze_text
from app.services.detectors.nlp.entitiy_processor import process_entities
from app.services.detectors.presidio.resolver import resolve_entities

# ==========================================
# NORMALIZER
# ==========================================

from app.services.normalizer_service import EntityNormalizer

# ==========================================
# PSEUDONYMIZER
# ==========================================

from app.services.pseudonymization.pseudonymizer import Pseudonymizer

REGEX_PIPELINE = [
    detect_email,
    detect_phone,
    detect_date,
    detect_id
]

normalizer = EntityNormalizer()
pseudonymizer = Pseudonymizer()


# ==========================================
# Convert Regex -> RecognizerResult
# ==========================================

def convert_regex_entities(regex_entities):

    presidio_entities = []

    for entity in regex_entities:

        presidio_entities.append(

            RecognizerResult(
                entity_type=entity["entity_type"],
                start=entity["start"],
                end=entity["end"],
                score=1.0
            )

        )

    return presidio_entities


# ==========================================
# Main Pipeline
# ==========================================

def redact_text(text: str):

    text = validate_text(text)

    # Session baru
    pseudonymizer.start_session()

    # =====================================
    # REGEX
    # =====================================

    regex_entities = []

    for detector in REGEX_PIPELINE:

        regex_entities.extend(
            detector(text)
        )

    regex_entities = convert_regex_entities(
        regex_entities
    )

    # =====================================
    # PRESIDIO
    # =====================================

    analyzer_results = analyze_text(
        text
    )

    # =====================================
    # CUSTOM NLP
    # =====================================

    custom_entities = process_entities(

        text=text,

        analyzer_results=analyzer_results

    )

    

    # =====================================
    # MERGE
    # =====================================

    merged_entities = (

        regex_entities

        +

        analyzer_results

        +

        custom_entities

    )
    print("=" * 80)
    print("MERGED")
    print("=" * 80)
    
    for e in merged_entities:
        print(
            e.entity_type,
            repr(text[e.start:e.end]),
            e.start,
            e.end
        )
        
    print("=" * 80)

    # =====================================
    # RESOLVE
    # =====================================

    resolved_entities = resolve_entities(
        merged_entities
    )

    print("=" * 80)
    print("RESOLVED")
    print("=" * 80)

    for e in resolved_entities:
        print(
            e.entity_type,
            text[e.start:e.end],
            e.start,
            e.end
        )

    print("=" * 80)

    # =====================================
    # NORMALIZE
    # =====================================

    normalized_entities = normalizer.normalize(

        text=text,

        entities=resolved_entities

    )

    # =====================================
    # DEBUG NORMALIZER
    # =====================================

    print("\n" + "=" * 80)
    print("NORMALIZED ENTITIES")
    print("=" * 80)

    for entity in normalized_entities:
        print(entity)

    print("=" * 80 + "\n")


    # =====================================
    # PSEUDONYMIZATION
    # =====================================

    redacted_text = pseudonymizer.redact(

        text=text,

        normalized_entities=normalized_entities

    )

    return redacted_text