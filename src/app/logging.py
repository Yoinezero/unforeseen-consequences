import logging
import sys

from loguru import logger
from loguru import logger as loguru_logger

from app.config.settings import Settings


class InterceptHandler(logging.Handler):
    """
    Default handler to redirect standard logging (logging module) to Loguru.
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Map the level: if standard has similar name → use that, else fallback
        try:
            level = loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find the calling frame so Loguru shows correct file/line
        frame, depth = logging.currentframe(), 2
        # climb up until you're out of logging module frames
        while frame is not None and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        loguru_logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(settings: Settings) -> None:
    # Remove existing root handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Intercept everything via root logger
    logging.root.setLevel(logging.DEBUG)  # or desired minimum

    logging.root.addHandler(InterceptHandler())

    # Configure other loggers: uvicorn, fastapi, sqlalchemy, etc.
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi", "sqlalchemy", "sqlalchemy.engine"):
        l = logging.getLogger(name)
        l.setLevel(logging.DEBUG)
        l.handlers = []  # remove default handlers
        l.propagate = True  # so messages reach root/InterceptHandler

    # Setup Loguru sinks: file, console, rotation, etc.
    loguru_logger.remove()  # remove default sink
    loguru_logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <7}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
    )
    # e.g. file with rotation
    loguru_logger.add("logs/app.log", rotation="10 MB", retention="7 days", compression="zip", level="DEBUG")
