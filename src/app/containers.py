from dependency_injector import containers, providers

from app.config.settings import Settings
from app.infra.db.container import Database


class Container(containers.DeclarativeContainer):
    # wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    config = Settings()

    db = providers.Singleton(Database, config=config.database)
