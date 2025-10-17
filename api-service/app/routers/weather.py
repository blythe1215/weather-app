from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime, timedelta
from app.models.weather import (
    CurrentWeatherResponse,
    ForecastResponse,
    WeatherRecord,
    HistoricalWeatherQuery,
    WeatherAnalytics,
    CityModel
)
from app.services.weather_api import WeatherAPIService
from app.services.database import DatabaseService

router = APIRouter(prefix="/weather", tags=["weather"])

weather_api = WeatherAPIService()
db_service = DatabaseService()


@router.get("/current", response_model=CurrentWeatherResponse)
async def get_current_weather(
    city: Optional[str] = Query(None, description="City name (e.g., 'London' or 'London,UK')"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude")
):
    """
    Get current weather data for a city or coordinates.
    This also stores the data in the database for historical tracking.
    """
    try:
        # Fetch weather from external API
        weather_data = await weather_api.get_current_weather(city=city, lat=lat, lon=lon)

        # Transform and store in database
        weather_record = weather_api.transform_to_weather_record(weather_data)

        # Upsert city information
        city_model = CityModel(
            city_id=weather_data.id,
            name=weather_data.name,
            country=weather_data.sys.country,
            latitude=weather_data.coord.lat,
            longitude=weather_data.coord.lon,
            timezone=weather_data.timezone
        )
        await db_service.upsert_city(city_model)

        # Store weather record
        await db_service.insert_weather_record(weather_record)

        return weather_data

    except HTTPException:
        raise
    except Exception as e:
        # Check if it's an API key error
        error_msg = str(e)
        if "401" in error_msg or "Invalid API key" in error_msg:
            raise HTTPException(
                status_code=401,
                detail="Invalid API key. Please configure a valid OpenWeatherMap API key."
            )
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/forecast", response_model=ForecastResponse)
async def get_forecast(
    city: Optional[str] = Query(None, description="City name"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude")
):
    """Get 5-day weather forecast (3-hour intervals)"""
    try:
        forecast_data = await weather_api.get_forecast(city=city, lat=lat, lon=lon)
        return forecast_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/historical/{city_id}", response_model=List[WeatherRecord])
async def get_historical_weather(
    city_id: int,
    start_date: Optional[datetime] = Query(None, description="Start date for historical data"),
    end_date: Optional[datetime] = Query(None, description="End date for historical data"),
    limit: int = Query(100, le=1000, description="Maximum number of records")
):
    """Get historical weather data for a city"""
    try:
        query = HistoricalWeatherQuery(
            city_id=city_id,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )

        records = await db_service.get_historical_weather(query)
        return records

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/{city_id}", response_model=WeatherAnalytics)
async def get_weather_analytics(
    city_id: int,
    days: int = Query(7, ge=1, le=30, description="Number of days to analyze")
):
    """Get weather analytics and trends for a city"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        analytics = await db_service.get_weather_analytics(
            city_id=city_id,
            start_date=start_date,
            end_date=end_date
        )

        if not analytics:
            raise HTTPException(
                status_code=404,
                detail="No analytics data available for this city"
            )

        return analytics

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/latest/{city_id}", response_model=WeatherRecord)
async def get_latest_weather(city_id: int):
    """Get the most recent weather record for a city from the database"""
    try:
        latest = await db_service.get_latest_weather(city_id)

        if not latest:
            raise HTTPException(
                status_code=404,
                detail="No weather data found for this city"
            )

        return latest

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
