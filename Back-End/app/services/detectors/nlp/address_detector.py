from presidio_analyzer import RecognizerResult

ADDRESS_KEYWORDS = [
        "street ",
        "road",
        "avenu",
        "district",
        "city",
        "jalan",
        "jl ",
        "jl .",
        "no",
        "rt",
        "rw",
        "kelurahan",
        "kecamatan",
        "kota", 
        "province"
]

def detect_address(
    text: str,
    results: list[RecognizerResult]
):
    addresses = []

    for entity in results:
        # Hanya proses LOCATION
        if entity.entity_type != "LOCATION":
            continue

        # Ambil konteks sebelum entity
        before = text[
            max(0, entity.start - 40):entity.start
        ].lower()

        # Ambil konteks sesudah entity
        after = text[
            entity.end:min(len(text), entity.end + 40)
        ].lower()

        context = before + " " + after

        # Cek apakah ada keyword alamat
        if any(keyword in context for keyword in ADDRESS_KEYWORDS):
            addresses.append(
                RecognizerResult(
                    entity_type="ADDRESS",
                    start=entity.start,
                    end=entity.end,
                    score=entity.score
                )
            )
    return addresses