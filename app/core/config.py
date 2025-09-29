import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    BASE_DIR: str = os.path.abspath(Path(__file__).parent.parent)
    DOCS_URL: str = "/docs"
    USE_JSON_LOGGING: bool = False
    LOG_LEVEL: str = "INFO"

    OPEN_WEATHER_API_KEY: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USE_SSL: bool = True

    AWS_ENDPOINT_URL_CUSTOM: str | None = "http://localhost:4566"
    WEATHER_DATA_BUCKET_NAME: str = "weather"


settings = Settings()
