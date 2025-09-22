from abc import abstractmethod
from typing import Protocol

import uuid_utils as uuid

from app.domain.entities.base import BaseEntity


class ISocialProfileRepository[SocialProfileEntity: BaseEntity](Protocol):
    @abstractmethod
    async def save(self, social_entity: SocialProfileEntity) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_provider_id(self, provider: str, provider_user_id: str) -> SocialProfileEntity | None:
        raise NotImplementedError()

    @abstractmethod
    async def find_by_user_id(self, user_id: uuid.UUID) -> list[SocialProfileEntity]:
        raise NotImplementedError()
