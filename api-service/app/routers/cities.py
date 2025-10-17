from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.weather import CityModel
from app.services.database import DatabaseService

router = APIRouter(prefix="/cities", tags=["cities"])

db_service = DatabaseService()


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
    """Search for cities by name"""
    try:
        cities = await db_service.search_cities(q)
        return cities

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
