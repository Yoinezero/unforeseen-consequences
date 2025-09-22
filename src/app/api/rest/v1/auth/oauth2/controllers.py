from typing import Annotated, Literal

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from loguru import logger

from app.config.settings import Settings
from app.containers import Container
from app.infra.security.jwt_utils import JWTService

# Import from your new central module
from app.infra.security.oauth2 import oauth
from app.services.user import UserService

# Your create_access_token function and other imports would be here

router = APIRouter()


@router.get("/login/{provider}")
async def login_via_provider(
    request: Request,
    provider: Literal["github"],
):
    """
    Redirects the user to the OAuth provider's login page.
    """
    redirect_uri = request.url_for("auth_callback", provider=provider)
    return await getattr(oauth, provider).authorize_redirect(request, redirect_uri)


@router.get("/callback/{provider}")
@inject
async def auth_callback(
    request: Request,
    provider: Literal["github"],
    user_service: Annotated[UserService, Depends(Provide[Container.user_service])],
    settings: Annotated[Settings, Depends(Provide[Container.config])],
    jwt: Annotated[JWTService, Depends(Provide[Container.security])],
):
    """
    Handles the callback from the OAuth provider after the user has authenticated.
    """
    try:
        token = await getattr(oauth, provider).authorize_access_token(request)
        # TODO: move logic to a dedicated service
        match provider:
            case "github":
                resp = await oauth.github.get("user", token=token)
                user_data = resp.json()
                if not user_data.get("email"):
                    resp_email = await oauth.github.get("user/emails", token=token)
                    email_data = resp_email.json()
                    primary_email = next((e["email"] for e in email_data if e["primary"]), None)
                    user_data["email"] = primary_email

        user = await user_service.update_or_crate_user_oauth(
            email=user_data["email"],
            provider=provider,
            provider_id=user_data["id"],
        )

        access_token = jwt.create_access_token(user_id=str(user.id))
        refresh_token = jwt.create_refresh_token(user_id=str(user.id))

        redirect_url = f"{settings.app.frontend_url}/auth/callback?access_token={access_token}"

        response = RedirectResponse(url=redirect_url)

        response.set_cookie(
            key=settings.app.refresh_token_cookie_name,
            value=refresh_token,
            max_age=settings.app.refresh_token_expires_days * 24 * 60 * 60,
            httponly=True,
            secure=settings.app.cookie_secure,
            samesite=settings.app.cookie_samesite,
        )

        return response

    except Exception as e:
        logger.error(f"Error during OAuth callback: {e}")
        error_redirect_url = f"{settings.app.frontend_url}/auth/error?error=oauth_failed"
        return RedirectResponse(url=error_redirect_url)
