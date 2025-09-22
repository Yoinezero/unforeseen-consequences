from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config.app import AppSettings
from app.config.database import DatabaseSettings
from app.config.logging import LoggingSettings
from app.config.oauth_providers import ProviderSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    app: AppSettings
    oauth2: ProviderSettings
    database: DatabaseSettings
    logging: LoggingSettings
