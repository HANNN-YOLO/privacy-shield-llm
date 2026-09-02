import os
import redis
from dotenv import load_dotenv

load_dotenv()

class RedisProvider:
    _client = None
    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = redis.Redis(
                host=os.getenv("REDIS_HOST", "healtech"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                db=int(os.getenv("REDIS_DB", 0)),
                password=os.getenv("REDIS_PASSWORD") or None,
                decode_responses=True
            )
        return cls._client

def get_redis():
    return RedisProvider.get_client()