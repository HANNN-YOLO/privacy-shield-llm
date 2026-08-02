from app.providers.presidio_provider import get_analyzer

def detect_pii(text: str):

    analyzer = get_analyzer()

    results = analyzer.analyze(
        text=text,
        language="en"
    )

    entities = []

    for result in results:

        entities.append({
            "entity": result.entity_type,
            "text": text[result.start:result.end],
            "start": result.start,
            "end": result.end,
            "score": result.score
        })

    return results