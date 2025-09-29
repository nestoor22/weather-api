from redis.asyncio import Redis

from app.core.config import settings
from app.core.singleton import SingletonMeta


class BaseRedisCache(metaclass=SingletonMeta):
    def __init__(self):
        self._client = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True,
            ssl=settings.REDIS_USE_SSL,
        )
