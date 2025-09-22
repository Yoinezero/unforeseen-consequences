from sqlalchemy import select

import uuid_utils as uuid

from app.domain.entities.user.entity import UserEntity
from app.domain.interfaces.repositories.user import IUserRepository
from app.infra.db.sqla.models import User as UserModel


class UserRepository(IUserRepository):
    """
    A SQLAlchemy implementation of the UserRepository.
    """

    def __init__(self, db_session_factory):
        # Dependency: a callable that returns an async session, like db.session
        self.get_session = db_session_factory

    async def save(self, user_entity: UserEntity) -> None:
        async with self.get_session() as session:
            # Check if user exists to decide between INSERT and UPDATE
            existing_user = await session.get(UserModel, user_entity.id)

            if existing_user:
                # Update existing user
                existing_user.email = user_entity.email
                existing_user.is_active = user_entity.is_active
            else:
                new_user = UserModel(**user_entity.model_dump())
                session.add(new_user)

    async def get_by_id(self, user_id: uuid.UUID) -> UserEntity | None:
        async with self.get_session() as session:
            user = await session.get(UserModel, user_id)

            if user:
                return UserEntity.model_validate(user)
            return None

    async def get_by_email(self, email: str) -> UserEntity | None:
        async with self.get_session() as session:
            stmt = select(UserModel).where(UserModel.email == email)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user:
                return UserEntity.model_validate(user)
            return None
