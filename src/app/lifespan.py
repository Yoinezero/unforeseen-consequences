from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing fastapi application.")
    yield
    logger.info("Shutting down fastapi application.")
