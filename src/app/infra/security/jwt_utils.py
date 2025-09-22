from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.config.settings import Settings


class JWTService:
    """
    A dedicated class to handle JWT creation and decoding, configured via settings.
    """

    def __init__(self, settings: Settings):
        self._secret_key = settings.app.secret_key
        self._algorithm = "HS256"
        self._access_token_expires_minutes = settings.app.access_token_expires_minutes
        self._refresh_token_expires_days = settings.app.refresh_token_expires_days

    def _create_jwt_token(self, subject: str, expires_delta: timedelta, token_type: str) -> str:
        """Internal helper to create a JWT token."""
        now = datetime.now(timezone.utc)
        payload: dict[str, Any] = {
            "sub": subject,
            "type": token_type,
            "iat": int(now.timestamp()),
            "exp": int((now + expires_delta).timestamp()),
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def create_access_token(self, user_id: str) -> str:
        """Create an access token for the given user ID."""
        return self._create_jwt_token(
            subject=user_id,
            expires_delta=timedelta(minutes=self._access_token_expires_minutes),
            token_type="access",
        )

    def create_refresh_token(self, user_id: str) -> str:
        """Create a refresh token for the given user ID."""
        return self._create_jwt_token(
            subject=user_id,
            expires_delta=timedelta(days=self._refresh_token_expires_days),
            token_type="refresh",
        )

    def decode_token(self, token: str) -> dict[str, Any] | None:
        """Decode a JWT token and return the payload, or None if invalid."""
        try:
            return jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
        except jwt.PyJWTError:
            return None
