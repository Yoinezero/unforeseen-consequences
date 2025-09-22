from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

import orjson

from loguru import logger

from app.config.database import DatabaseSettings


class Database:
    def __init__(self, config: DatabaseSettings) -> None:
        self.connect_args = {
            "timeout": 300,
            "command_timeout": 300,
            "server_settings": {
                "timezone": "UTC",
            },
        }

        logger.info(f"* Connecting to {config.dsn}.")

        self._engine: AsyncEngine = create_async_engine(
            url=config.dsn,
            poolclass=NullPool,
            connect_args=self.connect_args,
            json_serializer=orjson.dumps,
            json_deserializer=orjson.loads,
            echo=config.debug,
        )

        logger.info(f"* Connected to {config.dsn}.")

        self._session_factory = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
            expire_on_commit=False,
        )

    @property
    def engine(self) -> "AsyncEngine":
        return self._engine

    @property
    def session(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory
