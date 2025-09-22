import uuid_utils as uuid

from pydantic import Field, TypeAdapter

from app.domain.entities.base import BaseEntity


class SocialProfileEntity(BaseEntity):
    """
    A Pydantic-based entity for a User's social media link.
    It is immutable and self-validating.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid7)
    user_id: uuid.UUID
    provider: str
    provider_user_id: str


SocialProfileEntityList = TypeAdapter(list[SocialProfileEntity])
