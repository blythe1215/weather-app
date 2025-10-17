import httpx
import asyncio
from datetime import datetime
from typing import List
from supabase import create_client, Client
from config import settings
from models.weather import WeatherRecord, CityModel, WeatherAPIResponse


class WeatherDataCollector:
    """ETL pipeline for collecting and storing weather data"""

    def __init__(self):
        self.api_key = settings.weather_api_key
        self.base_url = settings.weather_api_base_url
        self.supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )

    async def fetch_weather_by_city_id(self, city_id: int) -> WeatherAPIResponse:
        """
        Fetch weather data from OpenWeatherMap API by city ID

        Args:
            city_id: OpenWeatherMap city ID

        Returns:
            WeatherAPIResponse with raw API data
        """
        params = {
            "id": city_id,
            "appid": self.api_key,
            "units": "metric"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/weather",
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

        return WeatherAPIResponse(**data)

    def transform_weather_data(self, api_response: WeatherAPIResponse) -> WeatherRecord:
        """
        Transform API response to database record

        Args:
            api_response: WeatherAPIResponse from API

        Returns:
            WeatherRecord ready for database
        """
        return WeatherRecord(
            city_id=api_response.id,
            city_name=api_response.name,
            country=api_response.sys["country"],
            latitude=api_response.coord["lat"],
            longitude=api_response.coord["lon"],
            temperature=api_response.main["temp"],
            feels_like=api_response.main["feels_like"],
            temp_min=api_response.main["temp_min"],
            temp_max=api_response.main["temp_max"],
            pressure=api_response.main["pressure"],
            humidity=api_response.main["humidity"],
            wind_speed=api_response.wind["speed"],
            wind_direction=api_response.wind["deg"],
            cloudiness=api_response.clouds["all"],
            visibility=api_response.visibility,
            weather_main=api_response.weather[0]["main"],
            weather_description=api_response.weather[0]["description"],
            weather_icon=api_response.weather[0]["icon"],
            recorded_at=datetime.fromtimestamp(api_response.dt)
        )

    def load_weather_record(self, weather_record: WeatherRecord) -> None:
        """
        Load weather record into Supabase

        Args:
            weather_record: WeatherRecord to insert
        """
        record_dict = weather_record.model_dump(exclude={"id", "created_at"})

        # Convert datetime to ISO format
        if isinstance(record_dict.get("recorded_at"), datetime):
            record_dict["recorded_at"] = record_dict["recorded_at"].isoformat()

        self.supabase.table("weather_records").insert(record_dict).execute()
        print(f"✓ Stored weather data for {weather_record.city_name}")

    def upsert_city(self, api_response: WeatherAPIResponse) -> None:
        """
        Insert or update city information

        Args:
            api_response: WeatherAPIResponse containing city data
        """
        city = CityModel(
            city_id=api_response.id,
            name=api_response.name,
            country=api_response.sys["country"],
            latitude=api_response.coord["lat"],
            longitude=api_response.coord["lon"],
            timezone=api_response.timezone
        )

        city_dict = city.model_dump(exclude={"id", "created_at"})

        self.supabase.table("cities")\
            .upsert(city_dict, on_conflict="city_id")\
            .execute()

    async def collect_weather_for_city(self, city_id: int) -> None:
        """
        Complete ETL process for a single city

        Args:
            city_id: OpenWeatherMap city ID
        """
        try:
            # Extract
            api_response = await self.fetch_weather_by_city_id(city_id)

            # Transform
            weather_record = self.transform_weather_data(api_response)

            # Load city info
            self.upsert_city(api_response)

            # Load weather record
            self.load_weather_record(weather_record)

        except Exception as e:
            print(f"✗ Error collecting data for city {city_id}: {str(e)}")

    async def collect_all_cities(self, city_ids: List[int]) -> None:
        """
        Collect weather data for multiple cities concurrently

        Args:
            city_ids: List of OpenWeatherMap city IDs
        """
        print(f"Starting weather data collection for {len(city_ids)} cities...")

        tasks = [self.collect_weather_for_city(city_id) for city_id in city_ids]
        await asyncio.gather(*tasks)

        print("Weather data collection completed!")

    async def run_collection(self) -> None:
        """Run the data collection for all configured cities"""
        await self.collect_all_cities(settings.cities_to_track)


async def main():
    """Main entry point for the data collector"""
    collector = WeatherDataCollector()
    await collector.run_collection()


if __name__ == "__main__":
    asyncio.run(main())
