from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class WeatherRecord(BaseModel):
    """Database model for storing weather records"""
    id: Optional[int] = None
    city_id: int
    city_name: str
    country: str
    latitude: float
    longitude: float
    temperature: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    wind_speed: float
    wind_direction: int
    cloudiness: int
    visibility: int
    weather_main: str
    weather_description: str
    weather_icon: str
    recorded_at: datetime
    created_at: Optional[datetime] = None


class CityModel(BaseModel):
    """Database model for cities"""
    id: Optional[int] = None
    city_id: int
    name: str
    country: str
    latitude: float
    longitude: float
    timezone: int
    created_at: Optional[datetime] = None


class WeatherAPIResponse(BaseModel):
    """Raw weather API response"""
    coord: dict
    weather: list[dict]
    base: str
    main: dict
    visibility: int
    wind: dict
    clouds: dict
    rain: Optional[dict] = None
    snow: Optional[dict] = None
    dt: int
    sys: dict
    timezone: int
    id: int
    name: str
    cod: int
