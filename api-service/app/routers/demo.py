from fastapi import APIRouter
from app.models.weather import CurrentWeatherResponse, Coordinates, WeatherCondition, MainWeatherData, Wind, Clouds, Sys
from datetime import datetime

router = APIRouter(prefix="/demo", tags=["demo"])

@router.get("/weather/current")
async def get_demo_weather(city: str = "London"):
    """Get demo weather data for testing"""

    demo_data = {
        "London": {
            "coord": Coordinates(lat=51.5085, lon=-0.1257),
            "weather": [WeatherCondition(id=800, main="Clear", description="clear sky", icon="01d")],
            "base": "stations",
            "main": MainWeatherData(
                temp=15.5,
                feels_like=14.2,
                temp_min=13.0,
                temp_max=17.0,
                pressure=1013,
                humidity=72
            ),
            "visibility": 10000,
            "wind": Wind(speed=3.5, deg=230),
            "clouds": Clouds(all=0),
            "dt": int(datetime.now().timestamp()),
            "sys": Sys(
                country="GB",
                sunrise=int(datetime.now().replace(hour=6, minute=30).timestamp()),
                sunset=int(datetime.now().replace(hour=18, minute=45).timestamp())
            ),
            "timezone": 0,
            "id": 2643743,
            "name": "London",
            "cod": 200
        },
        "Paris": {
            "coord": Coordinates(lat=48.8534, lon=2.3488),
            "weather": [WeatherCondition(id=801, main="Clouds", description="few clouds", icon="02d")],
            "base": "stations",
            "main": MainWeatherData(
                temp=16.8,
                feels_like=15.9,
                temp_min=14.5,
                temp_max=18.2,
                pressure=1015,
                humidity=68
            ),
            "visibility": 10000,
            "wind": Wind(speed=2.8, deg=180),
            "clouds": Clouds(all=20),
            "dt": int(datetime.now().timestamp()),
            "sys": Sys(
                country="FR",
                sunrise=int(datetime.now().replace(hour=6, minute=45).timestamp()),
                sunset=int(datetime.now().replace(hour=18, minute=30).timestamp())
            ),
            "timezone": 3600,
            "id": 2988507,
            "name": "Paris",
            "cod": 200
        },
        "Tokyo": {
            "coord": Coordinates(lat=35.6895, lon=139.6917),
            "weather": [WeatherCondition(id=500, main="Rain", description="light rain", icon="10d")],
            "base": "stations",
            "main": MainWeatherData(
                temp=18.3,
                feels_like=17.8,
                temp_min=16.0,
                temp_max=20.0,
                pressure=1008,
                humidity=82
            ),
            "visibility": 8000,
            "wind": Wind(speed=4.2, deg=90),
            "clouds": Clouds(all=75),
            "dt": int(datetime.now().timestamp()),
            "sys": Sys(
                country="JP",
                sunrise=int(datetime.now().replace(hour=5, minute=30).timestamp()),
                sunset=int(datetime.now().replace(hour=17, minute=15).timestamp())
            ),
            "timezone": 32400,
            "id": 1850144,
            "name": "Tokyo",
            "cod": 200
        }
    }

    # Return demo data for requested city or default
    city_data = demo_data.get(city, demo_data["London"])
    return city_data
