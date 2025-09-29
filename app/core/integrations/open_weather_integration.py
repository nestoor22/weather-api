from httpx import AsyncClient, HTTPError, codes

from app.core.config import settings
from app.core.exceptions import (
    CityNotFoundException,
    FailedToGetCoordinatesException,
    FailedToGetWeatherDataException,
)
from app.core.loggers import logger

__all__ = ["OpenWeatherAPIIntegration"]


class OpenWeatherAPIIntegration:
    def __init__(self):
        self.__client = AsyncClient(
            base_url="https://api.openweathermap.org",
            timeout=60.0,
            params={"appid": settings.OPEN_WEATHER_API_KEY},
        )

    async def get_coordinates(self, city: str) -> dict:
        logger.info("Getting city coordinates for %s", city)
        try:
            coordinates_response = await self.__client.get(
                url="/geo/1.0/direct", params={"q": city, "limit": 1}
            )
        except HTTPError as e:
            logger.error(
                "Failed to get coordinates data - %s", e, extra={"city": city}
            )
            raise FailedToGetCoordinatesException

        if codes.is_error(coordinates_response.status_code):
            logger.error(
                "Failed to get coordinates - %s",
                coordinates_response.text,
                extra={
                    "city": city,
                    "status_code": coordinates_response.status_code,
                },
            )
            raise FailedToGetCoordinatesException

        coordinates = coordinates_response.json()
        if not coordinates:
            raise CityNotFoundException(f"{city} not found")

        logger.info("%s City coordinates: %s", city, coordinates[0])
        return coordinates[0]

    async def get_weather_data(self, lat: float, lon: float) -> dict:
        logger.info("Getting weather data for lat=%s and lon=%s", lat, lon)
        try:
            weather_response = await self.__client.get(
                url="/data/2.5/weather", params={"lat": lat, "lon": lon}
            )
        except HTTPError as e:
            logger.error(
                "Failed to get weather data - %s",
                e,
                extra={"lat": lat, "lon": lon},
            )
            raise FailedToGetWeatherDataException

        if codes.is_error(weather_response.status_code):
            logger.error(
                "Failed to get weather data - %s",
                weather_response.text,
                extra={
                    "lat": lat,
                    "lon": lon,
                    "status_code": weather_response.status_code,
                },
            )
            raise FailedToGetWeatherDataException

        logger.info("Returning weather data for lat=%s and lon=%s", lat, lon)
        return weather_response.json()
