class RedisKeys:

    @staticmethod
    def mapping(token: str) -> str:
        return token

    @staticmethod
    def counter(entity_type: str) -> str:
        return f"counter:{entity_type.upper()}"