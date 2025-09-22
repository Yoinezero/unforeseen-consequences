import abc

from typing import Type

from app.domain.interfaces.repositories.social import ISocialProfileRepository
from app.domain.interfaces.repositories.user import IUserRepository


def _repository_property_factory(repo_name: str):
    """A factory function to create a lazy-loading property for a repository."""
    private_repo_name = f"_{repo_name}_repo"

    @property
    def lazy_repo_property(self):
        """
        This property will be attached to the UoW class.
        'self' is an instance of the Unit of Work.
        """
        if not hasattr(self, private_repo_name):
            repo_class = self.repositories[repo_name]
            instance = repo_class(self.session)
            setattr(self, private_repo_name, instance)

        # Return the cached repository instance
        return getattr(self, private_repo_name)

    return lazy_repo_property


class UnitOfWorkMeta(abc.ABCMeta):
    """
    Metaclass to automatically add lazy-loading repository properties
    to any class that uses it and defines a 'repositories' dictionary.
    """

    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)

        if repositories_map := dct.get("repositories"):
            for repo_name in repositories_map:
                # For each repository name, create and attach the lazy-loading property
                setattr(new_class, repo_name, _repository_property_factory(repo_name))

        return new_class


class AbstractUnitOfWork(abc.ABC, metaclass=UnitOfWorkMeta):
    """
    An abstract Unit of Work that handles transaction logic and provides
    repository properties defined in the 'repositories' dictionary.
    """

    repositories: dict[str, Type] = {
        "users": IUserRepository,
        "socials": ISocialProfileRepository,
    }

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError
