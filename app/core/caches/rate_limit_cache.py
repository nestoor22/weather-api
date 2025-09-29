from .base_redis_cache import BaseRedisCache

__all__ = ["RateLimitCache"]


class RateLimitCache(BaseRedisCache):
    async def increase_usage(self, ip: str) -> int:
        return await self._client.incr(self.get_cache_key(ip))

    async def get_current_usage(self, ip: str) -> int | None:
        value = await self._client.get(self.get_cache_key(ip))
        return int(value) if value is not None else None

    async def get_ttl(self, ip: str) -> int:
        return await self._client.ttl(self.get_cache_key(ip))

    async def set_expiry(self, ip: str, seconds: int):
        await self._client.expire(self.get_cache_key(ip), seconds)

    @staticmethod
    def get_cache_key(ip: str) -> str:
        return f"rate-{ip}"
