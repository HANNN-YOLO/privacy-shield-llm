from app.providers.presidio_provider import get_analyzer

def detect_pii(text: str):

    analyzer = get_analyzer()

    results = analyzer.analyze(
        text=text,
        language="en"
    )

    return results