"""Health check router."""

from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.api.rest.v1.users.views import UserView
from app.containers import Container
from app.domain.entities.user import UserEntity
from app.infra.security.dependencies import current_user

router = APIRouter()


@router.get("/me")
@inject
async def get_me(
    user: Annotated[UserEntity, Depends(current_user)],
) -> UserView:
    return user
