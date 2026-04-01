"""
Database Configuration and Session Management Module.

This module handles all database connections, session management,
and provides async SQLAlchemy support.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base

from backend.core.config import settings


# Create async engine
engine = create_async_engine(
    settings.database.url,
    echo=settings.database.echo,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    pool_timeout=settings.database.pool_timeout,
    pool_recycle=settings.database.pool_recycle,
)

# Create async session maker
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Create declarative base
Base = declarative_base()


class TimestampMixin:
    """Mixin for timestamp columns."""
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


class ProductModel(Base, TimestampMixin):
    """Product database model."""
    
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True, index=True)
    cost_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=True)
    margin_percent = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)
    review_count = Column(Integer, nullable=True)
    estimated_orders = Column(Integer, nullable=True)
    demand_score = Column(Float, nullable=True, index=True)
    supplier_id = Column(String(100), nullable=True)
    supplier_rating = Column(Float, nullable=True)
    shipping_time_days = Column(Integer, nullable=True)
    stock_quantity = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    is_published = Column(Boolean, default=False, index=True)
    source = Column(String(50), default="scraped")
    store_product_id = Column(String(100), nullable=True)


class SaleModel(Base, TimestampMixin):
    """Sale database model."""
    
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, nullable=False, index=True)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=False)
    profit = Column(Float, nullable=False)
    customer_name = Column(String(100), nullable=True)
    sale_date = Column(DateTime, default=datetime.utcnow, index=True)


class AnalyticsModel(Base, TimestampMixin):
    """Analytics database model."""
    
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    total_revenue = Column(Float, default=0.0)
    total_profit = Column(Float, default=0.0)
    total_sales = Column(Integer, default=0)
    active_products = Column(Integer, default=0)
    published_products = Column(Integer, default=0)
    conversion_rate = Column(Float, nullable=True)
    avg_order_value = Column(Float, nullable=True)


class AgentRunModel(Base, TimestampMixin):
    """Agent execution log model."""
    
    __tablename__ = "agent_runs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_type = Column(String(50), nullable=False)
    status = Column(String(20), default="running", index=True)
    products_analyzed = Column(Integer, nullable=True)
    products_selected = Column(Integer, nullable=True)
    products_published = Column(Integer, nullable=True)
    revenue_generated = Column(Float, nullable=True)
    details = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)


class UserModel(Base, TimestampMixin):
    """User database model for authentication."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(200), unique=True, nullable=False, index=True)
    hashed_password = Column(String(200), nullable=False)
    full_name = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)


async def init_db() -> None:
    """
    Initialize database by creating all tables.
    
    This function creates all database tables based on the models.
    Should be called on application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
    """
    Drop all database tables.
    
    WARNING: This will delete all data!
    Should only be used in development/testing.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def close_db() -> None:
    """
    Close database connections.
    
    Should be called on application shutdown.
    """
    await engine.dispose()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session.
    
    This is the main database session dependency for FastAPI.
    Yields an async session and ensures proper cleanup.
    
    Yields:
        AsyncSession: Database session
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session as a context manager.
    
    Alternative to get_db() for use outside of FastAPI dependencies.
    
    Yields:
        AsyncSession: Database session
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_db_connection() -> bool:
    """
    Check if database connection is healthy.
    
    Returns:
        bool: True if connection is successful
    """
    try:
        async with async_session_maker() as session:
            await session.execute("SELECT 1")
            return True
    except Exception:
        return False
