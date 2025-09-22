import uuid_utils as uuid

from app.domain.entities.social import SocialProfileEntity
from app.domain.entities.user import UserEntity
from app.domain.entities.user.exceptions import UserNotFoundError
from app.domain.interfaces.uow import AbstractUnitOfWork


class UserService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def update_or_crate_user_oauth(self, email: str, provider: str, provider_id: str) -> UserEntity:
        async with self.uow as uow:
            user_entity = await uow.users.get_by_email(email)
            if user_entity is None:
                user_entity = UserEntity(email=email)
                await uow.users.save(user_entity)

            social_profile_entity = await uow.socials.get_by_provider_id(provider, str(provider_id))
            if social_profile_entity is None:
                social_profile_entity = SocialProfileEntity(
                    user_id=user_entity.id,
                    provider=provider,
                    provider_user_id=provider_id,
                )
                await uow.socials.save(social_profile_entity)

        return user_entity

    async def get_user_by_id(self, id: uuid.UUID) -> UserEntity:
        async with self.uow as uow:
            user_entity = await uow.users.get_by_id(id)

            if user_entity is None:
                raise UserNotFoundError(identifier=id)

        return user_entity
