from presidio_analyzer import AnalyzerEngine, RecognizerResult

analyzer = AnalyzerEngine()

def analyze_text(text: str) -> list[RecognizerResult]:
    results = analyzer.analyze(
        text=text,
        language="en"
    )

    # Urutkan berdasarkan posisi dalam text
    results.sort(key=lambda x: x.start)

    return results