from pydantic_settings import BaseSettings


class OAuthSettings(BaseSettings):
    client_id: str = ""
    client_secret: str = ""


class ProviderSettings(BaseSettings):
    # google: OAuthSettings
    github: OAuthSettings = OAuthSettings()
