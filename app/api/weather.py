from fastapi import APIRouter, Query, status

from app.core.decorators import custom_exceptions_to_http_error
from app.core.exceptions import (
    CityNotFoundException,
    FailedToGetCoordinatesException,
    FailedToGetWeatherDataException,
    FailedToUploadFileToS3Exception,
)
from app.schemas import WeatherResponse
from app.services import WeatherService

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("", status_code=status.HTTP_200_OK, response_model=WeatherResponse)
@custom_exceptions_to_http_error(
    exceptions_to_handle=[
        CityNotFoundException,
        FailedToUploadFileToS3Exception,
        FailedToGetCoordinatesException,
        FailedToGetWeatherDataException,
    ]
)
async def get_weather(city: str = Query(...)):
    return await WeatherService().get_weather(city)
