"""Script to seed demo data into the database."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.models.database import init_db, get_session, close_db
from backend.services.analytics_service import get_analytics_service


async def seed_data():
    """Seed demo data into the database."""
    print("Initializing database...")
    await init_db("sqlite+aiosqlite:///./data/dropshipping.db")
    
    print("Seeding demo data...")
    analytics = get_analytics_service()
    result = await analytics.seed_demo_data()
    
    print(f"Seeding result: {result}")
    
    await close_db()
    print("Done!")


if __name__ == "__main__":
    asyncio.run(seed_data())
