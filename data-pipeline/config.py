from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Data pipeline settings"""

    # Weather API
    weather_api_key: str = ""
    weather_api_base_url: str = "https://api.openweathermap.org/data/2.5"

    # Supabase Configuration
    supabase_url: str = ""
    supabase_key: str = ""

    # Data collection settings
    collection_interval_minutes: int = 60
    cities_to_track: list[int] = [5128581, 2643743, 1850144, 5368361, 2988507]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


settings = Settings()
