from collections import OrderedDict


class EntityNormalizer:

    def normalize(
        self,
        text: str,
        entities: list
    ):

        normalized = OrderedDict()

        # posisi dari kiri ke kanan
        entities = sorted(
            entities,
            key=lambda e: e.start
        )

        for entity in entities:

            value = text[
                entity.start:entity.end
            ].strip()

            if not value:
                continue

            key = (
                entity.entity_type,
                value.lower()
            )

            occurrence = (
                entity.start,
                entity.end
            )

            if key not in normalized:

                normalized[key] = {
                    "entity_type": entity.entity_type,
                    "value": value,
                    "occurrences": [
                        occurrence
                    ]
                }

            else:

                normalized[key][
                    "occurrences"
                ].append(
                    occurrence
                )

        return list(
            normalized.values()
        )