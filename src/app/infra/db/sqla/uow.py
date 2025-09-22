from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain.entities.social import SocialProfileRepository
from app.domain.entities.user import UserRepository
from app.domain.interfaces.uow import AbstractUnitOfWork


class SQLAUnitOfWork(AbstractUnitOfWork):
    repositories = {
        "users": UserRepository,
        "socials": SocialProfileRepository,
    }

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory

    async def __aenter__(self):
        self.session = self._session_factory()
        return self

    async def commit(self):
        """Commits the transaction and closes the session."""
        await self.session.commit()
        await self.session.close()

    async def rollback(self):
        """Rolls back the transaction and closes the session."""
        await self.session.rollback()
        await self.session.close()
