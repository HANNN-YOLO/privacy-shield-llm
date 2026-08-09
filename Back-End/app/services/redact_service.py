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
# PSEUDONYMIZATION
# ==========================================

from app.services.pseudonymization.pseudonymizer import Pseudonymizer


# ==========================================
# METRICS
# ==========================================

from time import perf_counter

from app.services.metrics_service import (
    build_redact_metrics
)


# ==========================================
# PIPELINE CONFIGURATION
# ==========================================

REGEX_PIPELINE = [
    detect_email,
    detect_phone,
    detect_date,
    detect_id
]


# ==========================================
# SERVICE INSTANCE
# ==========================================

normalizer = EntityNormalizer()

pseudonymizer = Pseudonymizer()


# ==========================================
# CONVERT REGEX → RECOGNIZER RESULT
# ==========================================

def convert_regex_entities(
    regex_entities
):

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
# MAIN REDACTION PIPELINE
# ==========================================

def redact_text(text: str):

    # ======================================
    # START PROCESSING TIMER
    # ======================================

    start_time = perf_counter()


    # ======================================
    # VALIDATE INPUT
    # ======================================

    text = validate_text(text)


    # ======================================
    # START NEW PSEUDONYMIZATION SESSION
    # ======================================

    pseudonymizer.start_session()


    # ======================================
    # REGEX DETECTION
    # ======================================

    regex_entities = []

    for detector in REGEX_PIPELINE:

        detected = detector(text)

        regex_entities.extend(
            detected
        )


    # ======================================
    # CONVERT REGEX → RECOGNIZER RESULT
    # ======================================

    regex_entities = convert_regex_entities(
        regex_entities
    )


    # ======================================
    # PRESIDIO ANALYSIS
    # ======================================

    analyzer_results = analyze_text(
        text
    )


    # ======================================
    # CUSTOM NLP
    # ======================================

    custom_entities = process_entities(

        text=text,

        analyzer_results=analyzer_results

    )


    # ======================================
    # MERGE ALL ENTITIES
    # ======================================

    merged_entities = (

        regex_entities

        + analyzer_results

        + custom_entities

    )


    # ======================================
    # RESOLVE OVERLAPPING ENTITIES
    # ======================================

    resolved_entities = resolve_entities(

        merged_entities

    )


    # ======================================
    # NORMALIZE ENTITIES
    # ======================================

    normalized_entities = normalizer.normalize(

        text=text,

        entities=resolved_entities

    )


    # ======================================
    # PSEUDONYMIZATION
    # ======================================
    #
    # Pseudonymizer melakukan:
    #
    # 1. Generate token
    # 2. Save mapping ke Redis
    # 3. Replace original text
    #
    # Tidak perlu mapping_service
    # dipanggil lagi di sini.
    # ======================================

    redacted_text = pseudonymizer.redact(

        text=text,

        normalized_entities=normalized_entities

    )


    # ======================================
    # STOP PROCESSING TIMER
    # ======================================

    processing_time_ms = (

        perf_counter() - start_time

    ) * 1000


    # ======================================
    # BUILD METRICS
    # ======================================
    #
    # normalized_entities adalah FINAL
    # ENTITY setelah:
    #
    # Regex
    # Presidio
    # Custom NLP
    # Resolver
    # Normalizer
    #
    # Jadi metrics menghitung entity
    # berdasarkan hasil final tersebut.
    # ======================================

    metrics = build_redact_metrics(

        normalized_entities,

        processing_time_ms

    )


    # ======================================
    # RETURN FINAL RESULT
    # ======================================

    return {

        "redacted_text": redacted_text,

        "entity_counts": metrics[
            "entity_counts"
        ],

        "total_entities": metrics[
            "total_entities"
        ],

        "processing_time_ms": metrics[
            "processing_time_ms"
        ],

    }