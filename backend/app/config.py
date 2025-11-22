"""Application configuration."""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "High-Performance Data Table API"
    DEBUG: bool = False
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Cache TTL (in seconds)
    CACHE_TTL_LIST: int = 120
    CACHE_TTL_DETAIL: int = 900
    CACHE_TTL_STATS: int = 300
    CACHE_TTL_CATEGORIES: int = 3600
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )


settings = Settings()
