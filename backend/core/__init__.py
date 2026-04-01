"""Core module initialization."""

from backend.core.config import settings, get_settings
from backend.core.database import (
    Base,
    engine,
    async_session_maker,
    get_db,
    init_db,
    close_db,
)
from backend.core.security import (
    auth_service,
    create_access_token,
    verify_password,
    get_password_hash,
    create_tokens,
)
from backend.core.dependencies import (
    get_current_user,
    get_optional_user,
    get_db_session,
    PaginationParams,
)

__all__ = [
    "settings",
    "get_settings",
    "Base",
    "engine",
    "async_session_maker",
    "get_db",
    "init_db",
    "close_db",
    "auth_service",
    "create_access_token",
    "verify_password",
    "get_password_hash",
    "create_tokens",
    "get_current_user",
    "get_optional_user",
    "get_db_session",
    "PaginationParams",
]
