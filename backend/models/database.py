from datetime import datetime
from typing import Optional
from sqlalchemy import String, Float, Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class Product(Base):
    """Product model representing scraped/dropshipped products."""
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Cost and pricing
    cost_price: Mapped[float] = mapped_column(Float, nullable=False)
    selling_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    margin_percent: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Product metrics
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    review_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    estimated_orders: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Demand prediction
    demand_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Supplier info
    supplier_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    supplier_rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    shipping_time_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    stock_quantity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    source: Mapped[str] = mapped_column(String(50), default="scraped")
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sales: Mapped[list["Sale"]] = relationship(back_populates="product")


class Sale(Base):
    """Sale model representing product orders."""
    __tablename__ = "sales"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    cost_price: Mapped[float] = mapped_column(Float, nullable=False)
    profit: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Customer info (mock)
    customer_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Timestamps
    sale_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product: Mapped["Product"] = relationship(back_populates="sales")


class Analytics(Base):
    """Analytics model for tracking daily metrics."""
    __tablename__ = "analytics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Revenue metrics
    total_revenue: Mapped[float] = mapped_column(Float, default=0.0)
    total_profit: Mapped[float] = mapped_column(Float, default=0.0)
    total_sales: Mapped[int] = mapped_column(Integer, default=0)
    
    # Product metrics
    active_products: Mapped[int] = mapped_column(Integer, default=0)
    published_products: Mapped[int] = mapped_column(Integer, default=0)
    
    # Conversion metrics
    conversion_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    avg_order_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AgentRun(Base):
    """Model for tracking AI agent execution logs."""
    __tablename__ = "agent_runs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="running")
    
    # Results
    products_analyzed: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    products_selected: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    products_published: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    revenue_generated: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Details (JSON)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


# Database setup
engine = None
async_session_maker = None


async def init_db(database_url: str) -> None:
    """Initialize database connection and create tables."""
    global engine, async_session_maker
    
    engine = create_async_engine(database_url, echo=False)
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """Get a database session."""
    if async_session_maker is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    async with async_session_maker() as session:
        return session


async def close_db() -> None:
    """Close database connection."""
    if engine is not None:
        await engine.dispose()