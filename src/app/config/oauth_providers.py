from pydantic import BaseModel


class OAuthSettings(BaseModel):
    client_id: str = ""
    client_secret: str = ""


class ProviderSettings(BaseModel):
    # google: OAuthSettings
    github: OAuthSettings
