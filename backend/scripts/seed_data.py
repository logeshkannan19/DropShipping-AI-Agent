"""
Seed Script for DropShipping AI Agent

This script seeds the database with initial demo data.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.models.database import init_db, get_session
from backend.models.database import Product, Sale, Analytics
from backend.services.analytics_service import get_analytics_service
from backend.utils.logging_utils import setup_logging, get_logger

setup_logging()
logger = get_logger("seed")


async def seed_database():
    """Seed the database with demo data."""
    logger.info("Starting database seeding...")
    
    await init_db("sqlite+aiosqlite:///./data/dropshipping.db")
    
    analytics = get_analytics_service()
    result = await analytics.seed_demo_data()
    
    logger.info(f"Seeding complete: {result}")
    print(f"\n✅ Database seeded successfully!")
    print(f"   Products created: {result.get('products_created', 0)}")
    print(f"   Sales created: {result.get('sales_created', 0)}")


if __name__ == "__main__":
    asyncio.run(seed_database())