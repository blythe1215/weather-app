from datetime import datetime, timedelta
from openai import AsyncOpenAI
from app.config import settings
from app.services.database import DatabaseService


class AIInsightsService:
    """Service for generating AI-powered weather insights using OpenAI"""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.db_service = DatabaseService()

    async def get_insight(
        self,
        city_id: int,
        city_name: str,
        query: str
    ) -> str:
        """
        Get AI-powered weather insights for a city

        Args:
            city_id: City ID
            city_name: City name for context
            query: User's question or request

        Returns:
            AI-generated insight as a string
        """
        # Fetch weather data
        latest_weather = await self.db_service.get_latest_weather(city_id)

        # Get analytics from last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        analytics = await self.db_service.get_weather_analytics(
            city_id=city_id,
            start_date=start_date,
            end_date=end_date
        )

        # Build context
        current_weather_str = ""
        if latest_weather:
            current_weather_str = f"""Current Weather:
- Temperature: {latest_weather.temperature}°C (feels like {latest_weather.feels_like}°C)
- Conditions: {latest_weather.weather_main} - {latest_weather.weather_description}
- Humidity: {latest_weather.humidity}%
- Wind Speed: {latest_weather.wind_speed} m/s
- Recorded: {latest_weather.recorded_at}"""

        analytics_str = ""
        if analytics:
            analytics_str = f"""7-Day Analytics:
- Average Temperature: {analytics.avg_temperature}°C
- Max Temperature: {analytics.max_temperature}°C
- Min Temperature: {analytics.min_temperature}°C
- Average Humidity: {analytics.avg_humidity}%
- Average Wind Speed: {analytics.avg_wind_speed} m/s
- Most Common Condition: {analytics.most_common_condition}"""

        system_prompt = f"""You are a weather analysis assistant providing insightful and helpful information about weather patterns for {city_name}.

{current_weather_str}

{analytics_str}

Provide clear, concise, and actionable insights. Compare current conditions to weekly averages when relevant."""

        # Call OpenAI API
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content

    async def generate_daily_summary(
        self,
        city_id: int,
        city_name: str
    ) -> str:
        """Generate a daily weather summary for a city"""
        query = f"Provide a comprehensive daily weather summary for {city_name}, including current conditions, how they compare to this week's average, and any notable trends."
        return await self.get_insight(city_id, city_name, query)

    async def get_clothing_recommendation(
        self,
        city_id: int,
        city_name: str
    ) -> str:
        """Get clothing recommendations based on weather"""
        query = f"Based on the current weather conditions in {city_name}, what clothing would you recommend for someone going outside today?"
        return await self.get_insight(city_id, city_name, query)
