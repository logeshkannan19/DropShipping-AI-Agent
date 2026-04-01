"""Pytest configuration and fixtures."""

import pytest
import asyncio
from typing import Generator, AsyncGenerator
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.models.database import Base, init_db, close_db, get_session
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    test_db_url = "sqlite+aiosqlite:///./data/test_dropshipping.db"
    await init_db(test_db_url)
    
    session = await get_session()
    
    try:
        yield session
    finally:
        await session.close()
        await close_db()


@pytest.fixture
def sample_product_data():
    """Sample product data for testing."""
    return {
        "name": "Test Product",
        "description": "A test product for unit testing",
        "category": "Electronics",
        "cost_price": 25.99,
        "selling_price": 49.99,
        "rating": 4.5,
        "review_count": 150,
        "estimated_orders": 500,
        "supplier_id": "SUP-001",
        "supplier_rating": 4.8,
        "shipping_time_days": 14,
        "stock_quantity": 100,
        "source": "test"
    }


@pytest.fixture
def sample_demand_features():
    """Sample demand prediction features."""
    return {
        "category": "Electronics",
        "price": 35.99,
        "rating": 4.5,
        "review_count": 200,
        "competitor_count": 25,
        "supplier_rating": 4.7,
        "shipping_days": 12
    }


@pytest.fixture
def sample_pricing_data():
    """Sample pricing data."""
    return {
        "cost_price": 15.99,
        "competitor_prices": [25.99, 29.99, 27.99, 32.99],
        "demand_score": 0.75,
        "target_margin": 30.0
    }
