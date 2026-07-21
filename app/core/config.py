"""
Sentinel AI XDR

Configuration Management

Purpose:
Load application configuration from the .env file and provide
a single settings object across the application.

Author:
Sairaj Kulkarni

Project:
Sentinel AI XDR
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# --------------------------------------------------
# Project Root
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """
    Application settings loaded from .env
    """

    # --------------------------------------------------
    # Application
    # --------------------------------------------------

    app_name: str
    app_version: str
    debug: bool = True

    # --------------------------------------------------
    # Server
    # --------------------------------------------------

    host: str = "127.0.0.1"
    port: int = 8000

    # --------------------------------------------------
    # Security
    # --------------------------------------------------

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # --------------------------------------------------
    # Database
    # --------------------------------------------------

    database_url: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()


settings = get_settings()