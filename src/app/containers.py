from dependency_injector import containers, providers

from app.config.settings import Settings
from app.infra.db.sqla.container import Database
from app.infra.db.sqla.uow import SQLAUnitOfWork
from app.infra.security.jwt_utils import JWTService
from app.infra.security.oauth2 import setup_oauth_providers
from app.logging import setup_logging
from app.services.user import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.api.rest",
        ]
    )

    config = providers.Singleton(Settings)
    db = providers.Singleton(Database, config=config.provided.database)

    oauth = providers.Resource(setup_oauth_providers, settings=config.provided)
    logging = providers.Resource(setup_logging, settings=config.provided)

    security = providers.Singleton(JWTService, settings=config.provided)

    unit_of_work = providers.Factory(
        SQLAUnitOfWork,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        uow=unit_of_work,
    )
