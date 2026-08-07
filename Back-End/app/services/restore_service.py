import re

from app.services.redis.mapping_service import MappingService


mapping_service = MappingService()


# ======================================================
# Restore Text
# ======================================================

def restore_text(
    text: str
) -> str:

    # ---------------------------------------
    # Cari seluruh token
    # ---------------------------------------

    tokens = set(
        re.findall(
            r"\[[A-Z]+_\d+\]",
            text
        )
    )

    # ---------------------------------------
    # Tidak ada token
    # ---------------------------------------

    if not tokens:
        return text

    # ---------------------------------------
    # Loop semua token
    # ---------------------------------------

    for token in tokens:

        clean_token = token.strip("[]")

        original = mapping_service.get_original(
            clean_token
        )

        if original is None:
            continue

        text = text.replace(
            token,
            original
        )

    return text