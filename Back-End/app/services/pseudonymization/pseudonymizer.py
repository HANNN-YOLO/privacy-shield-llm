from app.services.pseudonymization.token_generator import TokenGenerator
from app.services.redis.mapping_service import MappingService

class Pseudonymizer:

    def __init__(self):
        self.generator = TokenGenerator()
        self.mapping_service = MappingService()

    # ==========================================
    # Session
    # ==========================================

    def start_session(self):
        self.generator.reset()
        self.mapping_service.clear()

    # ==========================================
    # Generate Token
    # ==========================================

    def generate_tokens(
        self,
        normalized_entities: list
    ):

        tokenized = []

        for entity in normalized_entities:

            entity_type = entity["entity_type"].upper()
            value = entity["value"]

            token = self.generator.generate(
                entity_type
            )

            self.mapping_service.save_mapping(
                original=value,
                token=token
            )

            tokenized.append({

                "token": token,

                "value": value,

                "entity_type": entity_type,

                "occurrences": entity["occurrences"]

            })

        return tokenized

    # ==========================================
    # Replace
    # ==========================================

    def replace_text(
        self,
        text: str,
        tokenized_entities: list
    ):

        replacements = []

        for entity in tokenized_entities:

            for start, end in entity["occurrences"]:

                replacements.append({

                    "start": start,

                    "end": end,

                    "token": entity["token"]

                })

        replacements.sort(
            key=lambda item: item["start"],
            reverse=True
        )

        redacted = text

        for item in replacements:

            redacted = (

                redacted[:item["start"]]

                + f"[{item['token']}]"

                + redacted[item["end"]:]

            )

        return redacted

    # ==========================================
    # Wrapper
    # ==========================================

    def redact(
        self,
        text: str,
        normalized_entities: list
    ):

        self.start_session()

        tokenized = self.generate_tokens(
            normalized_entities
        )

        return self.replace_text(
            text,
            tokenized
        )

    # ==========================================
    # Restore
    # ==========================================

    def restore(
        self,
        text: str
    ):

        import re

        pattern = r"\[([A-Z_]+\d{3})\]"

        tokens = re.findall(
            pattern,
            text
        )

        restored = text

        for token in tokens:

            value = self.mapping_service.get_original(
                token
            )

            if value:

                restored = restored.replace(
                    f"[{token}]",
                    value
                )

        return restored