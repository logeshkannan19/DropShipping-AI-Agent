"""API v1 Router Module."""

from fastapi import APIRouter

from backend.api.v1.endpoints import (
    products,
    analytics,
    agent,
    suppliers,
    store,
    health,
)


api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(agent.router, prefix="/agent", tags=["AI Agent"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["Suppliers"])
api_router.include_router(store.router, prefix="/store", tags=["Store"])
