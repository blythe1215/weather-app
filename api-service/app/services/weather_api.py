import httpx
from datetime import datetime
from typing import Optional
from app.config import settings
from app.models.weather import (
    CurrentWeatherResponse,
    ForecastResponse,
    WeatherRecord
)


class WeatherAPIService:
    """Service for fetching weather data from OpenWeatherMap API"""

    def __init__(self):
        self.base_url = settings.weather_api_base_url
        self.api_key = settings.weather_api_key

    async def get_current_weather(
        self,
        city: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> CurrentWeatherResponse:
        """
        Fetch current weather data by city name or coordinates

        Args:
            city: City name (e.g., "London" or "London,UK")
            lat: Latitude
            lon: Longitude

        Returns:
            CurrentWeatherResponse with weather data
        """
        params = {
            "appid": self.api_key,
            "units": "metric"  # Use Celsius
        }

        if city:
            params["q"] = city
        elif lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        else:
            raise ValueError("Must provide either city name or coordinates")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/weather",
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

        return CurrentWeatherResponse(**data)

    async def get_forecast(
        self,
        city: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> ForecastResponse:
        """
        Fetch 5-day weather forecast (3-hour intervals)

        Args:
            city: City name
            lat: Latitude
            lon: Longitude

        Returns:
            ForecastResponse with forecast data
        """
        params = {
            "appid": self.api_key,
            "units": "metric"
        }

        if city:
            params["q"] = city
        elif lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        else:
            raise ValueError("Must provide either city name or coordinates")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/forecast",
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

        return ForecastResponse(**data)

    @staticmethod
    def transform_to_weather_record(
        weather_response: CurrentWeatherResponse
    ) -> WeatherRecord:
        """
        Transform API response to database record format

        Args:
            weather_response: CurrentWeatherResponse from API

        Returns:
            WeatherRecord ready for database insertion
        """
        return WeatherRecord(
            city_id=weather_response.id,
            city_name=weather_response.name,
            country=weather_response.sys.country,
            latitude=weather_response.coord.lat,
            longitude=weather_response.coord.lon,
            temperature=weather_response.main.temp,
            feels_like=weather_response.main.feels_like,
            temp_min=weather_response.main.temp_min,
            temp_max=weather_response.main.temp_max,
            pressure=weather_response.main.pressure,
            humidity=weather_response.main.humidity,
            wind_speed=weather_response.wind.speed,
            wind_direction=weather_response.wind.deg,
            cloudiness=weather_response.clouds.all,
            visibility=weather_response.visibility,
            weather_main=weather_response.weather[0].main,
            weather_description=weather_response.weather[0].description,
            weather_icon=weather_response.weather[0].icon,
            recorded_at=datetime.fromtimestamp(weather_response.dt)
        )
