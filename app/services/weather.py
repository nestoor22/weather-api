import io
import json
from datetime import UTC, datetime

from app.core.caches import WeatherAPICache
from app.core.config import settings
from app.core.integrations import OpenWeatherAPIIntegration, S3Client

__all__ = ["WeatherService"]


class WeatherService:
    def __init__(self):
        self.__s3_client = S3Client()
        self.__open_weather_api_integration = OpenWeatherAPIIntegration()
        self.__weather_api_cache = WeatherAPICache()

    async def get_weather(self, city: str) -> dict:
        if cached_data := await self.__weather_api_cache.get_weather_data(
            city
        ):
            return cached_data

        city_coordinates = (
            await self.__open_weather_api_integration.get_coordinates(city)
        )

        weather_data = (
            await self.__open_weather_api_integration.get_weather_data(
                lat=city_coordinates["lat"],
                lon=city_coordinates["lon"],
            )
        )
        await self.__weather_api_cache.store_weather(city, weather_data)
        await self.__s3_client.upload_file(
            file=io.BytesIO(json.dumps(weather_data).encode("utf-8")),
            file_path=f"weather/{city}/{datetime.now(UTC).isoformat()}.json",
            bucket_name=settings.WEATHER_DATA_BUCKET_NAME,
        )
        return weather_data
