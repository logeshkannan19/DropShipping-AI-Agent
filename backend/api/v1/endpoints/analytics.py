"""Analytics API endpoints."""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db


router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])


class MetricsResponse(BaseModel):
    """Overall metrics response model."""
    
    total_revenue: float = 0.0
    total_profit: float = 0.0
    total_sales: int = 0
    total_products: int = 0
    active_products: int = 0
    published_products: int = 0
    conversion_rate: Optional[float] = None
    avg_order_value: Optional[float] = None
    profit_margin: float = 0.0


class TopProductResponse(BaseModel):
    """Top product response model."""
    
    id: int
    name: str
    category: Optional[str]
    revenue: float
    selling_price: Optional[float]
    demand_score: Optional[float]
    is_published: bool


class DailyStatResponse(BaseModel):
    """Daily statistics response model."""
    
    date: str
    revenue: float
    profit: float
    sales: int


class CategoryPerformanceResponse(BaseModel):
    """Category performance response model."""
    
    category: str
    product_count: int
    revenue: float
    profit: float


class AnalyticsSummaryResponse(BaseModel):
    """Full analytics summary response model."""
    
    metrics: MetricsResponse
    top_products: List[TopProductResponse]
    daily_stats: List[DailyStatResponse]
    category_performance: List[CategoryPerformanceResponse]
    generated_at: datetime


@router.get("", response_model=MetricsResponse)
async def get_analytics(
    days: int = Query(7, ge=1, le=90),
    db: AsyncSession = Depends(get_db)
):
    """
    Get overall business analytics metrics.
    
    Args:
        days: Number of days to include in stats
        db: Database session
    """
    from backend.core.database import ProductModel, SaleModel
    
    sales_result = await db.execute(
        select(
            func.coalesce(func.sum(SaleModel.total_price), 0).label("revenue"),
            func.coalesce(func.sum(SaleModel.profit), 0).label("profit"),
            func.count(SaleModel.id).label("sales_count")
        )
    )
    sales_row = sales_result.one()
    
    revenue = float(sales_row.revenue or 0)
    profit = float(sales_row.profit or 0)
    sales_count = int(sales_row.sales_count or 0)
    
    product_result = await db.execute(
        select(
            func.count(ProductModel.id).label("total"),
            func.sum(func.cast(ProductModel.is_active, int)).label("active"),
            func.sum(func.cast(ProductModel.is_published, int)).label("published")
        )
    )
    product_row = product_result.one()
    
    total_products = int(product_row.total or 0)
    active_products = int(product_row.active or 0)
    published_products = int(product_row.published or 0)
    
    conversion_rate = round(
        (sales_count / max(published_products * 100, 1)) * 100, 2
    )
    avg_order_value = round(revenue / max(sales_count, 1), 2)
    profit_margin = round((profit / revenue * 100) if revenue > 0 else 0, 2)
    
    return MetricsResponse(
        total_revenue=round(revenue, 2),
        total_profit=round(profit, 2),
        total_sales=sales_count,
        total_products=total_products,
        active_products=active_products,
        published_products=published_products,
        conversion_rate=conversion_rate,
        avg_order_value=avg_order_value,
        profit_margin=profit_margin
    )


@router.get("/top-products", response_model=List[TopProductResponse])
async def get_top_products(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Get top performing products by revenue.
    
    Args:
        limit: Number of products to return
        db: Database session
    """
    from backend.core.database import ProductModel, SaleModel
    
    result = await db.execute(
        select(
            ProductModel,
            func.coalesce(func.sum(SaleModel.total_price), 0).label("revenue")
        )
        .outerjoin(SaleModel, ProductModel.id == SaleModel.product_id)
        .group_by(ProductModel.id)
        .order_by(func.sum(SaleModel.total_price).desc())
        .limit(limit)
    )
    
    rows = result.all()
    
    return [
        TopProductResponse(
            id=product.id,
            name=product.name,
            category=product.category,
            revenue=float(row.revenue or 0),
            selling_price=product.selling_price,
            demand_score=product.demand_score,
            is_published=product.is_published
        )
        for product, row in rows
    ]


@router.get("/daily-stats", response_model=List[DailyStatResponse])
async def get_daily_stats(
    days: int = Query(7, ge=1, le=90),
    db: AsyncSession = Depends(get_db)
):
    """
    Get daily sales statistics.
    
    Args:
        days: Number of days to include
        db: Database session
    """
    from backend.core.database import SaleModel
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    result = await db.execute(
        select(SaleModel).where(SaleModel.sale_date >= start_date)
    )
    sales = result.scalars().all()
    
    daily_data = {}
    for sale in sales:
        date_key = sale.sale_date.strftime("%Y-%m-%d")
        if date_key not in daily_data:
            daily_data[date_key] = {"revenue": 0, "profit": 0, "sales": 0}
        daily_data[date_key]["revenue"] += sale.total_price
        daily_data[date_key]["profit"] += sale.profit
        daily_data[date_key]["sales"] += 1
    
    return [
        DailyStatResponse(
            date=date,
            revenue=round(data["revenue"], 2),
            profit=round(data["profit"], 2),
            sales=data["sales"]
        )
        for date, data in sorted(daily_data.items())
    ]


@router.get("/categories", response_model=List[CategoryPerformanceResponse])
async def get_category_performance(
    db: AsyncSession = Depends(get_db)
):
    """
    Get performance metrics by category.
    
    Args:
        db: Database session
    """
    from backend.core.database import ProductModel, SaleModel
    
    result = await db.execute(
        select(
            ProductModel.category,
            func.count(ProductModel.id).label("product_count"),
            func.coalesce(func.sum(SaleModel.total_price), 0).label("revenue"),
            func.coalesce(func.sum(SaleModel.profit), 0).label("profit")
        )
        .outerjoin(SaleModel, ProductModel.id == SaleModel.product_id)
        .group_by(ProductModel.category)
        .order_by(func.sum(SaleModel.total_price).desc())
    )
    
    rows = result.all()
    
    return [
        CategoryPerformanceResponse(
            category=row.category or "Uncategorized",
            product_count=int(row.product_count or 0),
            revenue=float(row.revenue or 0),
            profit=float(row.profit or 0)
        )
        for row in rows
    ]


@router.get("/summary", response_model=AnalyticsSummaryResponse)
async def get_analytics_summary(
    db: AsyncSession = Depends(get_db)
):
    """
    Get comprehensive analytics summary.
    
    Args:
        db: Database session
    """
    metrics = await get_analytics(db=db)
    top_products = await get_top_products(limit=5, db=db)
    daily_stats = await get_daily_stats(days=7, db=db)
    category_performance = await get_category_performance(db=db)
    
    return AnalyticsSummaryResponse(
        metrics=metrics,
        top_products=top_products,
        daily_stats=daily_stats,
        category_performance=category_performance,
        generated_at=datetime.utcnow()
    )
