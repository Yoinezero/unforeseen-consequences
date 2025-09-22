from typing import Annotated

import uuid_utils as uuid

from pydantic import UUID7, BeforeValidator, Field, TypeAdapter

from app.domain.entities.base import BaseEntity


class SocialProfileEntity(BaseEntity):
    """
    A Pydantic-based entity for a User's social media link.
    It is immutable and self-validating.
    """

    id: UUID7 = Field(default_factory=uuid.uuid7)
    user_id: UUID7
    provider: str
    provider_user_id: Annotated[str, BeforeValidator(lambda x: str(x))]


SocialProfileEntityList = TypeAdapter(list[SocialProfileEntity])
