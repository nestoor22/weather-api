import json

from app.core.loggers import logger

from .base_redis_cache import BaseRedisCache

__all__ = ["WeatherAPICache"]


class WeatherAPICache(BaseRedisCache):
    async def store_weather(self, city: str, weather_data: dict, ttl=5 * 60):
        logger.info("Storing weather data for %s to cache", city)
        await self._client.set(
            value=json.dumps(weather_data),
            name=self.get_cache_key(city),
            ex=ttl,
        )

    async def get_weather_data(self, city: str) -> dict | None:
        value = await self._client.get(
            name=self.get_cache_key(city),
        )
        if not value:
            return None
        logger.info("Retrieved weather data for %s from cache", city)
        return json.loads(value)

    @staticmethod
    def get_cache_key(city: str):
        return f"{city}-weather-api"
