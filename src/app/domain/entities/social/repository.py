import uuid

from sqlalchemy import select

from app.domain.entities.social.entity import SocialProfileEntity, SocialProfileEntityList
from app.domain.interfaces.repositories.social import ISocialProfileRepository
from app.infra.db.sqla.models import SocialProfile as SocialProfileModel


class SocialProfileRepository(ISocialProfileRepository):
    """
    A SQLAlchemy implementation of the SocialRepository.
    """

    def __init__(self, session):
        self.session = session

    async def save(self, social_entity: SocialProfileEntity) -> None:
        new_social_profile = SocialProfileModel(**social_entity.model_dump())
        await self.session.merge(new_social_profile)

    async def get_by_provider_id(self, provider: str, provider_user_id: str) -> SocialProfileEntity | None:
        stmt = select(SocialProfileModel).where(
            SocialProfileModel.provider == provider,
            SocialProfileModel.provider_user_id == provider_user_id,
        )
        result = await self.session.execute(stmt)
        social_profile = result.scalar_one_or_none()

        if social_profile:
            return SocialProfileEntity.model_validate(social_profile)
        return None

    async def find_by_user_id(self, user_id: uuid.UUID) -> list[SocialProfileEntity]:
        stmt = select(SocialProfileModel).where(SocialProfileModel.user_id == user_id)
        result = await self.session.execute(stmt)
        social_profiles = result.scalars().all()

        return SocialProfileEntityList.validate_python(social_profiles)
