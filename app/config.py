"""
Configuration Management for PRAISA

Centralized configuration using Pydantic Settings.
Loads from environment variables and .env file.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Database Configuration
    database_url: str = "sqlite:///./praisa_demo.db"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_title: str = "PRAISA Healthcare Interoperability API"
    api_version: str = "1.0.0"

    # Matching Algorithm Thresholds
    phonetic_match_threshold: float = 90.0
    fuzzy_match_threshold: float = 80.0
    review_threshold: float = 60.0

    # CORS Settings
    cors_origins: list = ["*"]  # For development; restrict in production

    # Environment
    env: str = "development"
    debug: bool = True

    # Frontend URL
    vite_api_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
