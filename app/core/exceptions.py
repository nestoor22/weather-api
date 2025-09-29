from fastapi import status


class WeatherAppBaseException(Exception):
    http_status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Exception"

    def __init__(self, message: str = ""):
        if message:
            self.message = message

    def __str__(self):
        return self.message


class FailedToUploadFileToS3Exception(WeatherAppBaseException):
    http_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Failed to upload file to s3"


class CityNotFoundException(WeatherAppBaseException):
    http_status_code = status.HTTP_404_NOT_FOUND
    message = "City not found"


class FailedToGetCoordinatesException(WeatherAppBaseException):
    http_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Failed to get coordinates"


class FailedToGetWeatherDataException(WeatherAppBaseException):
    http_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Failed to get weather data"
