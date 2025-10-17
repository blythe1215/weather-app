from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # API Configuration
    app_name: str = "Weather API Service"
    app_version: str = "1.0.0"
    debug: bool = False

    # Weather API
    weather_api_key: str = ""
    weather_api_base_url: str = "https://api.openweathermap.org/data/2.5"

    # Supabase Configuration
    supabase_url: str = ""
    supabase_key: str = ""

    # OpenAI Configuration (for LangGraph)
    openai_api_key: str = ""

    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:3001"]

    # Database
    database_url: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


settings = Settings()
