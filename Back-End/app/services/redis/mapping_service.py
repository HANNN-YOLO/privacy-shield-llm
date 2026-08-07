from app.providers.redis_provider import get_redis
from app.services.redis.redis_keys import RedisKeys


class MappingService:

    TTL = 600

    def __init__(self):
        self.redis = get_redis()

    # =====================================
    # Save
    # =====================================

    def save_mapping(
        self,
        original: str,
        token: str
    ):

        key = RedisKeys.mapping(token)

        self.redis.set(
            key,
            original,
            ex=self.TTL
        )

    # =====================================
    # Restore
    # =====================================

    def get_original(
        self,
        token: str
    ):

        key = RedisKeys.mapping(token)

        return self.redis.get(key)

    # =====================================
    # Delete
    # =====================================

    def delete_mapping(
        self,
        token: str
    ):

        key = RedisKeys.mapping(token)

        self.redis.delete(key)

    # =====================================
    # Clear Session
    # =====================================

    def clear(self):

        pattern = RedisKeys.mapping("*")

        for key in self.redis.scan_iter(match=pattern):

            self.redis.delete(key)

    # =====================================
    # Restore Multiple Tokens
    # =====================================

    def restore_tokens(
        self,
        tokens: list[str]
    ):

        restored = {}

        for token in tokens:

            original = self.get_original(token)

            if original is not None:

                restored[token] = original

        return restored