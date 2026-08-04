class TokenGenerator:
    def __init__(self):
        self.counters = {
            "PATIENT": 0,
            "DOCTOR": 0,
            "PERSON": 0,
            "EMAIL": 0,
            "PHONE": 0,
            "ADDRESS": 0,
            "DATE": 0,
            "ID": 0,
            "ORG": 0
        }

    def generate(self, entity_type: str) -> str:

        entity_type = entity_type.upper()

        # Tambahkan counter jika entity baru
        if entity_type not in self.counters:
            self.counters[entity_type] = 0

        # Naikkan counter
        self.counters[entity_type] += 1

        token = f"{entity_type}_{self.counters[entity_type]:03d}"

        return token

    def get_counter(self, entity_type: str) -> int:
        return self.counters.get(entity_type.upper(), 0)

    def reset(self):
        for key in self.counters:
            self.counters[key] = 0

    def show_counters(self):
        return self.counters.copy()