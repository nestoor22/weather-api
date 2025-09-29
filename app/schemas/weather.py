from pydantic import BaseModel

__all__ = ["WeatherResponse"]


class Coord(BaseModel):
    lon: float
    lat: float


class Weather(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class Main(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: int | None = None
    grnd_level: int | None = None


class Wind(BaseModel):
    speed: float
    deg: int
    gust: float | None = None


class Rain(BaseModel):
    _1h: float  # pylint: disable=invalid-name

    class Config:
        fields = {"_1h": "1h"}


class Clouds(BaseModel):
    all: int


class Sys(BaseModel):
    type: int | None = None
    id: int | None = None
    country: str
    sunrise: int
    sunset: int


class WeatherResponse(BaseModel):
    coord: Coord
    weather: list[Weather]
    base: str
    main: Main
    visibility: int
    wind: Wind
    rain: Rain | None = None
    clouds: Clouds
    dt: int
    sys: Sys
    timezone: int
    id: int
    name: str
    cod: int
