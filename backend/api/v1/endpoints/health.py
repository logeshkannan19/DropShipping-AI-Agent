"""Health check endpoints."""

from typing import Dict, Any
from datetime import datetime

from fastapi import APIRouter, status
from pydantic import BaseModel

from backend.core.config import settings
from backend.core.database import check_db_connection


router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str
    version: str
    environment: str
    database_connected: bool
    timestamp: datetime


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check the health status of the API"
)
async def health_check() -> HealthResponse:
    """
    Perform health check on the API and its dependencies.
    
    Returns:
        HealthResponse: Health status including database connectivity
    """
    db_connected = await check_db_connection()
    
    return HealthResponse(
        status="healthy" if db_connected else "degraded",
        version=settings.app.version,
        environment=settings.app.environment,
        database_connected=db_connected,
        timestamp=datetime.utcnow()
    )


@router.get(
    "/ready",
    status_code=status.HTTP_200_OK,
    summary="Readiness Check",
    description="Check if the API is ready to receive traffic"
)
async def readiness_check() -> Dict[str, str]:
    """
    Perform readiness check for the API.
    
    Returns:
        Dict with ready status
    """
    return {"status": "ready"}


@router.get(
    "/live",
    status_code=status.HTTP_200_OK,
    summary="Liveness Check",
    description="Check if the API is alive"
)
async def liveness_check() -> Dict[str, str]:
    """
    Perform liveness check for the API.
    
    Returns:
        Dict with alive status
    """
    return {"status": "alive"}
