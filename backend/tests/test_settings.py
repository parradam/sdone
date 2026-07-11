"""Tests for environment-driven application settings."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from app.core.config import Settings, get_settings

if TYPE_CHECKING:
    import pytest


def test_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    # Isolate from any SDONE_* vars in the environment and from a local .env
    # file so we assert the class defaults, not the developer's config.
    for key in list(os.environ):
        if key.startswith("SDONE_"):
            monkeypatch.delenv(key)
    # _env_file is a pydantic-settings runtime override the mypy plugin can't see.
    settings = Settings(_env_file=None)  # type: ignore[call-arg]
    assert settings.database_url == "sqlite:///./sdone.db"
    assert settings.log_level == "INFO"
    assert settings.env == "dev"


def test_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SDONE_DATABASE_URL", "sqlite:///./override.db")
    get_settings.cache_clear()
    try:
        assert get_settings().database_url == "sqlite:///./override.db"
    finally:
        get_settings.cache_clear()
