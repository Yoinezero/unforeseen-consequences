from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application's resource lifecycle.
    """
    logger.info("Initializing application resources.")

    container = app.container

    container.init_resources()

    yield

    logger.info("Shutting down application resources.")
    container.shutdown_resources()
