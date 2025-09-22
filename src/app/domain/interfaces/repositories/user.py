from abc import abstractmethod
from typing import Protocol

import uuid_utils as uuid

from app.domain.entities.base import BaseEntity


class IUserRepository[UserEntity: BaseEntity](Protocol):
    @abstractmethod
    async def save(self, user_entity: UserEntity) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> UserEntity | None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None:
        raise NotImplementedError()
