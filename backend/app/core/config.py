"""Application configuration loaded from the environment / .env file."""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings, sourced from environment variables (prefix ``SDONE_``)."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SDONE_",
        extra="ignore",
    )

    database_url: str = "sqlite:///./sdone.db"
    log_level: str = "INFO"
    env: Literal["dev", "test", "prod"] = "dev"


@lru_cache
def get_settings() -> Settings:
    """Return the cached :class:`Settings` instance.

    Cached with ``lru_cache`` so the ``.env`` file is read once. Tests can
    override values by clearing the cache (``get_settings.cache_clear()``) after
    monkeypatching the environment, or via FastAPI dependency overrides.
    """
    return Settings()
