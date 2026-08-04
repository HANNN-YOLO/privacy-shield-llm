from app.services.pseudonymization.token_generator import TokenGenerator

class Pseudonymizer:

    def __init__(self):
        self.mapping = {}

        self.generator = TokenGenerator()

    def pseudonymize(self, value: str, entity_type: str) -> str:
        if not value:
            return value

        value = value.strip()

        # jika sudah pernah dibuat token
        if value in self.mapping:
            return self.mapping[value]

        # buat token baru
        token = self.generator.generate(entity_type)

        # simpan mapping
        self.mapping[value] = token

        return token

    def get_token(self, value: str):
        return self.mapping.get(value)

    def has_value(self, value: str):
        return value in self.mapping

    def get_mapping(self):
        return self.mapping.copy()

    def reset(self):
        self.mapping.clear()
        self.generator.reset()

    def total_mapping(self):
        return len(self.mapping)