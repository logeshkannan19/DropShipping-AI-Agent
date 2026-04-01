"""DropShipping AI Agent Backend Application."""

__version__ = "1.0.0"
__author__ = "DropShipping AI Agent Team"

from backend.core.config import settings
from backend.core.database import Base, engine, async_session_maker, get_db

__all__ = [
    "settings",
    "Base",
    "engine",
    "async_session_maker",
    "get_db",
]
