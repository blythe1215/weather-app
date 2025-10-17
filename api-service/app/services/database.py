from datetime import datetime
from typing import Optional, List
from supabase import create_client, Client
from app.config import settings
from app.models.weather import (
    WeatherRecord,
    CityModel,
    WeatherAnalytics,
    HistoricalWeatherQuery
)


class DatabaseService:
    """Service for interacting with Supabase database"""

    def __init__(self):
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )

    async def insert_weather_record(
        self,
        weather_record: WeatherRecord
    ) -> WeatherRecord:
        """
        Insert a new weather record into the database

        Args:
            weather_record: WeatherRecord to insert

        Returns:
            Inserted WeatherRecord with id
        """
        record_dict = weather_record.model_dump(exclude={"id", "created_at"})

        # Convert datetime to ISO format string
        if isinstance(record_dict.get("recorded_at"), datetime):
            record_dict["recorded_at"] = record_dict["recorded_at"].isoformat()

        response = self.client.table("weather_records").insert(record_dict).execute()

        if response.data and len(response.data) > 0:
            return WeatherRecord(**response.data[0])

        raise Exception("Failed to insert weather record")

    async def get_latest_weather(self, city_id: int) -> Optional[WeatherRecord]:
        """
        Get the most recent weather record for a city

        Args:
            city_id: City ID

        Returns:
            Latest WeatherRecord or None
        """
        response = self.client.table("weather_records")\
            .select("*")\
            .eq("city_id", city_id)\
            .order("recorded_at", desc=True)\
            .limit(1)\
            .execute()

        if response.data and len(response.data) > 0:
            return WeatherRecord(**response.data[0])

        return None

    async def get_historical_weather(
        self,
        query: HistoricalWeatherQuery
    ) -> List[WeatherRecord]:
        """
        Get historical weather records for a city

        Args:
            query: HistoricalWeatherQuery with filters

        Returns:
            List of WeatherRecord objects
        """
        db_query = self.client.table("weather_records")\
            .select("*")\
            .eq("city_id", query.city_id)\
            .order("recorded_at", desc=True)\
            .limit(query.limit)

        if query.start_date:
            db_query = db_query.gte("recorded_at", query.start_date.isoformat())

        if query.end_date:
            db_query = db_query.lte("recorded_at", query.end_date.isoformat())

        response = db_query.execute()

        if response.data:
            return [WeatherRecord(**record) for record in response.data]

        return []

    async def get_weather_analytics(
        self,
        city_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Optional[WeatherAnalytics]:
        """
        Get weather analytics for a city using the database function

        Args:
            city_id: City ID
            start_date: Start of period
            end_date: End of period

        Returns:
            WeatherAnalytics object or None
        """
        params = {"p_city_id": city_id}

        if start_date:
            params["p_start_date"] = start_date.isoformat()
        if end_date:
            params["p_end_date"] = end_date.isoformat()

        response = self.client.rpc("get_weather_analytics", params).execute()

        if response.data and len(response.data) > 0:
            data = response.data[0]
            return WeatherAnalytics(**data)

        return None

    async def upsert_city(self, city: CityModel) -> CityModel:
        """
        Insert or update a city record

        Args:
            city: CityModel to upsert

        Returns:
            Upserted CityModel
        """
        city_dict = city.model_dump(exclude={"id", "created_at"})

        response = self.client.table("cities")\
            .upsert(city_dict, on_conflict="city_id")\
            .execute()

        if response.data and len(response.data) > 0:
            return CityModel(**response.data[0])

        raise Exception("Failed to upsert city")

    async def get_all_cities(self) -> List[CityModel]:
        """
        Get all cities from the database

        Returns:
            List of CityModel objects
        """
        response = self.client.table("cities")\
            .select("*")\
            .order("name")\
            .execute()

        if response.data:
            return [CityModel(**city) for city in response.data]

        return []

    async def search_cities(self, search_term: str) -> List[CityModel]:
        """
        Search for cities by name

        Args:
            search_term: Search string

        Returns:
            List of matching CityModel objects
        """
        response = self.client.table("cities")\
            .select("*")\
            .ilike("name", f"%{search_term}%")\
            .order("name")\
            .limit(10)\
            .execute()

        if response.data:
            return [CityModel(**city) for city in response.data]

        return []
