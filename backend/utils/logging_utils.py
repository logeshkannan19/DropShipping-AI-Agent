import logging
import sys
from pathlib import Path
from loguru import logger
from backend.config.settings import get_settings

settings = get_settings()


def setup_logging() -> None:
    """Configure logging for the application."""
    logger.remove()
    
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    log_dir = Path(settings.data_dir) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        log_dir / "app_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="30 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module."""
    return logger.bind(name=name)