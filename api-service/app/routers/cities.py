from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.weather import CityModel
from app.services.database import DatabaseService
from app.services.weather_api import WeatherAPIService

router = APIRouter(prefix="/cities", tags=["cities"])

db_service = DatabaseService()
weather_api = WeatherAPIService()


@router.get("/", response_model=List[CityModel])
async def get_all_cities():
    """Get all cities from the database"""
    try:
        cities = await db_service.get_all_cities()
        return cities

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search", response_model=List[CityModel])
async def search_cities(
    q: str = Query(..., min_length=1, description="Search term for city name")
):
    """
    Search for cities by name.
    First checks local database, then queries OpenWeatherMap API for any city worldwide.
    """
    try:
        # First, search in local database
        db_cities = await db_service.search_cities(q)

        # If we found cities in DB, return them
        if db_cities and len(db_cities) > 0:
            return db_cities

        # If not found in DB, try to fetch from OpenWeatherMap API
        try:
            weather_data = await weather_api.get_current_weather(city=q)

            # Create city model from the API response
            city = CityModel(
                city_id=weather_data.id,
                name=weather_data.name,
                country=weather_data.sys.country,
                latitude=weather_data.coord.lat,
                longitude=weather_data.coord.lon,
                timezone=weather_data.timezone
            )

            # Store the city in database for future searches
            try:
                await db_service.upsert_city(city)
            except Exception as upsert_error:
                # If upsert fails, just log it and continue (city might already exist)
                print(f"Failed to upsert city: {upsert_error}")

            return [city]

        except Exception as api_error:
            # If API call fails, return empty list (city not found)
            print(f"API search failed: {api_error}")
            return []

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
