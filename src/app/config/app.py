from enum import Enum

from pydantic import BaseModel


class EnvironmentEnum(str, Enum):
    PROD = "prod"
    STAGE = "stage"
    DEV = "dev"


class AppSettings(BaseModel):
    name: str = "Authorization app"
    environment: EnvironmentEnum = EnvironmentEnum.DEV
    debug: bool = False
    frontend_url: str = "http://localhost:3000"

    # tokens
    secret_key: str = "secret"
    access_token_expires_minutes: int = 60
    refresh_token_expires_days: int = 30
