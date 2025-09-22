from typing import Annotated

import uuid_utils as uuid

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from loguru import logger

from app.containers import Container
from app.domain.entities.user import UserEntity
from app.infra.security.jwt_utils import JWTService
from app.services.user import UserService

bearer_scheme = HTTPBearer(auto_error=True)

@inject
async def current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    user_service: Annotated[UserService, Depends(Provide[Container.user_service])],
    jwt: Annotated[JWTService, Depends(Provide[Container.security])],
) -> UserEntity:
    """Extract and validate the current user from JWT token."""
    token = credentials.credentials
    payload = jwt.decode_token(token)
    logger.info(f"Payload: {payload}")
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_service.get_user_by_id(uuid.UUID(user_id, version=7))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
