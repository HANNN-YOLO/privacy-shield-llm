import spacy
from spacy.language import Language

_MODEL_NAME = "en_core_web_sm"

_nlp: Language | None = None

def get_nlp() -> Language:
    global _nlp

    if _nlp is None:
        _nlp = spacy.load(_MODEL_NAME)

    return _nlp