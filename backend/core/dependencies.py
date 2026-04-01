"""
Dependency Injection Module.

This module provides FastAPI dependencies for authentication,
database sessions, and other common dependencies.
"""

from typing import Optional, AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.core.security import auth_service


# HTTP Bearer security scheme
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> dict:
    """
    Get current authenticated user.
    
    This dependency requires a valid JWT token in the Authorization header.
    Used for protected endpoints that require authentication.
    
    Args:
        credentials: HTTP Authorization credentials
        
    Returns:
        dict: User data from token
        
    Raises:
        HTTPException: If token is invalid or missing
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if credentials is None:
        raise credentials_exception
    
    token = credentials.credentials
    payload = auth_service.verify_token(token, "access")
    
    if payload is None:
        raise credentials_exception
    
    user_id = payload.get("sub")
    username = payload.get("username")
    
    if user_id is None:
        raise credentials_exception
    
    return {"id": int(user_id), "username": username}


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[dict]:
    """
    Get current user if authenticated, None otherwise.
    
    This dependency allows optional authentication.
    Used for endpoints that behave differently for authenticated users.
    
    Args:
        credentials: HTTP Authorization credentials
        
    Returns:
        Optional[dict]: User data if authenticated, None otherwise
    """
    if credentials is None:
        return None
    
    token = credentials.credentials
    payload = auth_service.verify_token(token, "access")
    
    if payload is None:
        return None
    
    user_id = payload.get("sub")
    username = payload.get("username")
    
    if user_id is None:
        return None
    
    return {"id": int(user_id), "username": username}


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session dependency.
    
    This is a wrapper around get_db that provides proper typing.
    
    Yields:
        AsyncSession: Database session
    """
    async for session in get_db():
        yield session


class PaginationParams:
    """
    Pagination parameters for list endpoints.
    
    Provides standard pagination with limit and offset.
    """
    
    def __init__(
        self,
        skip: int = 0,
        limit: int = 100,
        max_limit: int = 1000
    ):
        """
        Initialize pagination parameters.
        
        Args:
            skip: Number of items to skip
            limit: Maximum number of items to return
            max_limit: Maximum allowed limit
        """
        self.skip = max(0, skip)
        self.limit = min(max(1, limit), max_limit)


def get_pagination_params(
    skip: int = 0,
    limit: int = 100
) -> PaginationParams:
    """
    Get pagination parameters dependency.
    
    Args:
        skip: Number of items to skip
        limit: Maximum number of items to return
        
    Returns:
        PaginationParams: Pagination parameters instance
    """
    return PaginationParams(skip=skip, limit=limit)
