from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import orjson

from loguru import logger

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

    from app.config.database import DatabaseSettings


class Database:
    def __init__(self, config: "DatabaseSettings") -> None:
        # TODO: Configure with env variables
        self.connect_args = {
            "timeout": 300,
            "command_timeout": 300,
            "server_settings": {
                "jit": "off",
                "application_name": "default",
                "timezone": "UTC",
            },
        }

        # if config.use_bouncer:
        #     self.connect_args["server_settings"].pop("jit", None)
        #     self.connect_args["server_settings"].pop("lock_timeout", None)
        #     self.connect_args["prepared_statement_name_func"] = lambda: f"__asyncpg_{uuid.uuid4()}__"
        #     self.connect_args["prepared_statement_cache_size"] = 0
        #     self.connect_args["statement_cache_size"] = 0

        self._engine = create_async_engine(
            config.dsn,
            pool_class=NullPool,
            future=True,
            echo=config.debug,
        )

        self._engine: AsyncEngine = create_async_engine(
            url=config.dsn,
            poolclass=NullPool,
            connect_args=self.connect_args,
            json_serializer=orjson.dumps,  # TODO: will be bytes on output, replace with strings
            json_deserializer=orjson.loads,
            echo=config.debug,
        )

        self._session_factory = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
            expire_on_commit=False,
        )

    @property
    def engine(self) -> "AsyncEngine":
        return self._engine

    @asynccontextmanager
    async def session(self):
        session: "AsyncSession" = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise  # TODO: raise custom exception
        finally:
            await session.close()
