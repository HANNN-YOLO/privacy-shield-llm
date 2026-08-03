from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer import RecognizerResult

from app.services.detectors.presidio.mapper import (
    get_operator_mapping
)

anonymizer = AnonymizerEngine()


def anonymize_text(
    text: str,
    entities: list[RecognizerResult]
) -> str:

    result = anonymizer.anonymize(
        text=text,
        analyzer_results=entities,
        operators=get_operator_mapping()
    )

    return result.text