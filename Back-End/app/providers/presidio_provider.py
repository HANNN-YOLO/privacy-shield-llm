from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

_analyzer = None


def get_analyzer():

    global _analyzer

    if _analyzer is None:

        configuration = {
            "nlp_engine_name": "spacy",
            "models": [
                {
                    "lang_code": "en",
                    "model_name": "en_core_web_lg"
                }
            ]
        }

        provider = NlpEngineProvider(
            nlp_configuration=configuration
        )

        nlp_engine = provider.create_engine()

        _analyzer = AnalyzerEngine(
            nlp_engine=nlp_engine,
            supported_languages=["en"]
        )

    return _analyzer