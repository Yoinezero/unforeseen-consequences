from authlib.integrations.starlette_client import OAuth
from loguru import logger

from app.config.settings import Settings

oauth = OAuth()


def setup_oauth_providers(settings: Settings):
    """
    Registers OAuth providers using configuration from the Settings object.
    This function should be called once at application startup.
    """
    oauth.register(
        name="github",
        access_token_url="https://github.com/login/oauth/access_token",
        access_token_params=None,
        authorize_url="https://github.com/login/oauth/authorize",
        authorize_params=None,
        api_base_url="https://api.github.com/",
        # Use the settings object provided by the DI container
        client_id=settings.oauth2.github.client_id,
        client_secret=settings.oauth2.github.client_secret,
        client_kwargs={"scope": "user:email"},
    )
    logger.info(oauth.github)
