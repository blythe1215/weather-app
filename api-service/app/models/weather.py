from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    """Geographic coordinates"""
    lat: float = Field(..., description="Latitude")
    lon: float = Field(..., description="Longitude")


class WeatherCondition(BaseModel):
    """Weather condition details"""
    id: int
    main: str = Field(..., description="Group of weather parameters (Rain, Snow, Clouds etc.)")
    description: str = Field(..., description="Weather condition within the group")
    icon: str = Field(..., description="Weather icon id")


class MainWeatherData(BaseModel):
    """Main weather measurements"""
    temp: float = Field(..., description="Temperature in Celsius")
    feels_like: float = Field(..., description="Feels like temperature")
    temp_min: float = Field(..., description="Minimum temperature")
    temp_max: float = Field(..., description="Maximum temperature")
    pressure: int = Field(..., description="Atmospheric pressure in hPa")
    humidity: int = Field(..., description="Humidity percentage")
    sea_level: Optional[int] = Field(None, description="Sea level pressure")
    grnd_level: Optional[int] = Field(None, description="Ground level pressure")


class Wind(BaseModel):
    """Wind information"""
    speed: float = Field(..., description="Wind speed in m/s")
    deg: int = Field(..., description="Wind direction in degrees")
    gust: Optional[float] = Field(None, description="Wind gust speed")


class Clouds(BaseModel):
    """Cloudiness data"""
    all: int = Field(..., description="Cloudiness percentage")


class Rain(BaseModel):
    """Rain volume"""
    one_hour: Optional[float] = Field(None, alias="1h", description="Rain volume for last hour")
    three_hours: Optional[float] = Field(None, alias="3h", description="Rain volume for last 3 hours")


class Snow(BaseModel):
    """Snow volume"""
    one_hour: Optional[float] = Field(None, alias="1h", description="Snow volume for last hour")
    three_hours: Optional[float] = Field(None, alias="3h", description="Snow volume for last 3 hours")


class Sys(BaseModel):
    """System data"""
    country: str = Field(..., description="Country code")
    sunrise: int = Field(..., description="Sunrise time, unix UTC")
    sunset: int = Field(..., description="Sunset time, unix UTC")


class CurrentWeatherResponse(BaseModel):
    """Complete current weather response from API"""
    coord: Coordinates
    weather: List[WeatherCondition]
    base: str
    main: MainWeatherData
    visibility: int
    wind: Wind
    clouds: Clouds
    rain: Optional[Rain] = None
    snow: Optional[Snow] = None
    dt: int = Field(..., description="Time of data calculation, unix UTC")
    sys: Sys
    timezone: int
    id: int = Field(..., description="City ID")
    name: str = Field(..., description="City name")
    cod: int


class ForecastItem(BaseModel):
    """Single forecast item for 3-hour intervals"""
    dt: int = Field(..., description="Time of forecasted data, unix UTC")
    main: MainWeatherData
    weather: List[WeatherCondition]
    clouds: Clouds
    wind: Wind
    visibility: int
    pop: float = Field(..., description="Probability of precipitation")
    rain: Optional[Rain] = None
    snow: Optional[Snow] = None
    dt_txt: str = Field(..., description="Time of data forecasted, ISO format")


class City(BaseModel):
    """City information in forecast"""
    id: int
    name: str
    coord: Coordinates
    country: str
    population: int
    timezone: int
    sunrise: int
    sunset: int


class ForecastResponse(BaseModel):
    """5-day forecast response"""
    cod: str
    message: int
    cnt: int = Field(..., description="Number of forecast items")
    list: List[ForecastItem]
    city: City


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

    class Config:
        from_attributes = True


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

    class Config:
        from_attributes = True


class HistoricalWeatherQuery(BaseModel):
    """Query parameters for historical weather data"""
    city_id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(default=100, le=1000)


class WeatherAnalytics(BaseModel):
    """Analytics data for weather trends"""
    city_name: str
    country: str
    period_start: datetime
    period_end: datetime
    avg_temperature: float
    max_temperature: float
    min_temperature: float
    avg_humidity: float
    avg_wind_speed: float
    most_common_condition: str
    total_records: int
