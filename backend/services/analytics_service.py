"""
Analytics Module

This module handles business analytics and metrics:
- Track revenue, profit, conversion rate
- Store data in SQLite
- Provide analytics queries and aggregation
"""

import random
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy import select, func, and_
from loguru import logger
from backend.models.database import Product, Sale, Analytics, get_session


class AnalyticsService:
    """
    Service for business analytics and metrics.
    
    Tracks revenue, profit, conversion rate and provides
    analytics queries.
    """
    
    def __init__(self):
        """Initialize the analytics service."""
        logger.info("AnalyticsService initialized")
    
    async def get_overall_metrics(self) -> Dict[str, Any]:
        """
        Get overall business metrics.
        
        Returns:
            Dictionary of metrics
        """
        session = await get_session()
        
        try:
            # Get total revenue and profit from sales
            total_result = await session.execute(
                select(
                    func.sum(Sale.total_price).label("revenue"),
                    func.sum(Sale.profit).label("profit"),
                    func.count(Sale.id).label("sales_count")
                )
            )
            total_row = total_result.first()
            
            revenue = float(total_row.revenue or 0)
            profit = float(total_row.profit or 0)
            sales_count = int(total_row.sales_count or 0)
            
            # Get product counts
            product_result = await session.execute(
                select(
                    func.count(Product.id).label("total"),
                    func.sum(func.cast(Product.is_active, int)).label("active"),
                    func.sum(func.cast(Product.is_published, int)).label("published")
                )
            )
            product_row = product_result.first()
            
            total_products = int(product_row.total or 0)
            active_products = int(product_row.active or 0)
            published_products = int(product_row.published or 0)
            
            # Calculate conversion rate (mock - would need actual visitor data)
            conversion_rate = round((sales_count / max(published_products * 100, 1)) * 100, 2)
            
            # Calculate average order value
            avg_order_value = round(revenue / max(sales_count, 1), 2)
            
            return {
                "total_revenue": round(revenue, 2),
                "total_profit": round(profit, 2),
                "total_sales": sales_count,
                "total_products": total_products,
                "active_products": active_products,
                "published_products": published_products,
                "conversion_rate": conversion_rate,
                "avg_order_value": avg_order_value,
                "profit_margin": round((profit / revenue * 100) if revenue > 0 else 0, 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting metrics: {e}")
            return self._get_default_metrics()
        finally:
            await session.close()
    
    def _get_default_metrics(self) -> Dict[str, Any]:
        """Get default metrics when database is empty."""
        return {
            "total_revenue": 0.0,
            "total_profit": 0.0,
            "total_sales": 0,
            "total_products": 0,
            "active_products": 0,
            "published_products": 0,
            "conversion_rate": 0.0,
            "avg_order_value": 0.0,
            "profit_margin": 0.0
        }
    
    async def get_top_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top performing products.
        
        Args:
            limit: Number of products to return
            
        Returns:
            List of top products
        """
        session = await get_session()
        
        try:
            result = await session.execute(
                select(Product, func.sum(Sale.total_price).label("revenue"))
                .join(Sale, Product.id == Sale.product_id)
                .group_by(Product.id)
                .order_by(func.sum(Sale.total_price).desc())
                .limit(limit)
            )
            
            products = []
            for row in result:
                product = row[0]
                products.append({
                    "id": product.id,
                    "name": product.name,
                    "category": product.category,
                    "revenue": float(row.revenue),
                    "selling_price": product.selling_price,
                    "demand_score": product.demand_score,
                    "is_published": product.is_published
                })
            
            return products
            
        except Exception as e:
            logger.error(f"Error getting top products: {e}")
            return []
        finally:
            await session.close()
    
    async def get_daily_stats(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get daily statistics for the last N days.
        
        Args:
            days: Number of days to retrieve
            
        Returns:
            List of daily stats
        """
        session = await get_session()
        
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            result = await session.execute(
                select(Sale)
                .where(Sale.sale_date >= start_date)
                .order_by(Sale.sale_date)
            )
            
            sales = result.scalars().all()
            
            # Group by date
            daily_data = {}
            for sale in sales:
                date_key = sale.sale_date.strftime("%Y-%m-%d")
                if date_key not in daily_data:
                    daily_data[date_key] = {"revenue": 0, "profit": 0, "sales": 0}
                daily_data[date_key]["revenue"] += sale.total_price
                daily_data[date_key]["profit"] += sale.profit
                daily_data[date_key]["sales"] += 1
            
            return [
                {
                    "date": date,
                    "revenue": round(data["revenue"], 2),
                    "profit": round(data["profit"], 2),
                    "sales": data["sales"]
                }
                for date, data in sorted(daily_data.items())
            ]
            
        except Exception as e:
            logger.error(f"Error getting daily stats: {e}")
            return []
        finally:
            await session.close()
    
    async def get_category_performance(self) -> List[Dict[str, Any]]:
        """
        Get performance by product category.
        
        Returns:
            List of category performance
        """
        session = await get_session()
        
        try:
            result = await session.execute(
                select(
                    Product.category,
                    func.count(Product.id).label("product_count"),
                    func.sum(Sale.total_price).label("revenue"),
                    func.sum(Sale.profit).label("profit")
                )
                .join(Sale, Product.id == Sale.product_id)
                .group_by(Product.category)
                .order_by(func.sum(Sale.total_price).desc())
            )
            
            categories = []
            for row in result:
                categories.append({
                    "category": row.category or "Uncategorized",
                    "product_count": row.product_count,
                    "revenue": float(row.revenue or 0),
                    "profit": float(row.profit or 0)
                })
            
            return categories
            
        except Exception as e:
            logger.error(f"Error getting category performance: {e}")
            return []
        finally:
            await session.close()
    
    async def record_sale(
        self,
        product_id: int,
        quantity: int,
        unit_price: float,
        cost_price: float,
        customer_name: str = None
    ) -> int:
        """
        Record a sale in the database.
        
        Args:
            product_id: Product ID
            quantity: Quantity sold
            unit_price: Selling price per unit
            cost_price: Cost price per unit
            customer_name: Customer name (optional)
            
        Returns:
            Sale ID
        """
        session = await get_session()
        
        try:
            total_price = unit_price * quantity
            profit = (unit_price - cost_price) * quantity
            
            sale = Sale(
                product_id=product_id,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                cost_price=cost_price * quantity,
                profit=profit,
                customer_name=customer_name,
                sale_date=datetime.utcnow()
            )
            
            session.add(sale)
            await session.commit()
            await session.refresh(sale)
            
            logger.info(f"Sale recorded: ID={sale.id}, Product={product_id}, Amount=${total_price:.2f}")
            
            return sale.id
            
        except Exception as e:
            await session.rollback()
            logger.error(f"Error recording sale: {e}")
            raise
        finally:
            await session.close()
    
    async def seed_demo_data(self) -> Dict[str, Any]:
        """
        Seed demo data for testing analytics.
        
        Returns:
            Seeding results
        """
        session = await get_session()
        
        try:
            # Check if data already exists
            existing = await session.execute(select(Product).limit(1))
            if existing.scalars().first():
                logger.info("Demo data already exists, skipping seed")
                return {"status": "skipped", "message": "Data already exists"}
            
            # Create demo products
            products_data = [
                {"name": "Wireless Earbuds", "category": "Electronics", "cost_price": 15.99, "selling_price": 35.99, "rating": 4.5, "demand_score": 0.85, "is_published": True},
                {"name": "Yoga Mat", "category": "Sports", "cost_price": 12.99, "selling_price": 29.99, "rating": 4.7, "demand_score": 0.78, "is_published": True},
                {"name": "LED Desk Lamp", "category": "Electronics", "cost_price": 18.99, "selling_price": 39.99, "rating": 4.3, "demand_score": 0.72, "is_published": True},
                {"name": "Face Serum", "category": "Beauty", "cost_price": 8.99, "selling_price": 24.99, "rating": 4.6, "demand_score": 0.65, "is_published": True},
                {"name": "Resistance Bands", "category": "Sports", "cost_price": 9.99, "selling_price": 22.99, "rating": 4.8, "demand_score": 0.82, "is_published": True},
                {"name": "Phone Charger", "category": "Electronics", "cost_price": 11.99, "selling_price": 25.99, "rating": 4.2, "demand_score": 0.68, "is_published": False},
                {"name": "Water Bottle", "category": "Sports", "cost_price": 7.99, "selling_price": 19.99, "rating": 4.4, "demand_score": 0.55, "is_published": False},
                {"name": "Skincare Kit", "category": "Beauty", "cost_price": 14.99, "selling_price": 34.99, "rating": 4.5, "demand_score": 0.71, "is_published": True},
            ]
            
            products = []
            for p in products_data:
                product = Product(**p)
                session.add(product)
                products.append(product)
            
            await session.flush()
            
            # Create demo sales
            sales_data = []
            for product in products:
                if product.is_published:
                    num_sales = random.randint(5, 20)
                    for _ in range(num_sales):
                        sale = Sale(
                            product_id=product.id,
                            quantity=random.randint(1, 3),
                            unit_price=product.selling_price,
                            total_price=product.selling_price * random.randint(1, 3),
                            cost_price=product.cost_price * random.randint(1, 3),
                            profit=(product.selling_price - product.cost_price) * random.randint(1, 3),
                            sale_date=datetime.utcnow() - timedelta(days=random.randint(0, 30))
                        )
                        session.add(sale)
                        sales_data.append(sale)
            
            await session.commit()
            
            logger.info(f"Seeded {len(products)} products and {len(sales_data)} sales")
            
            return {
                "status": "success",
                "products_created": len(products),
                "sales_created": len(sales_data)
            }
            
        except Exception as e:
            await session.rollback()
            logger.error(f"Error seeding data: {e}")
            raise
        finally:
            await session.close()
    
    async def get_analytics_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive analytics summary.
        
        Returns:
            Full analytics summary
        """
        metrics = await self.get_overall_metrics()
        top_products = await self.get_top_products(5)
        daily_stats = await self.get_daily_stats(7)
        category_performance = await self.get_category_performance()
        
        return {
            "metrics": metrics,
            "top_products": top_products,
            "daily_stats": daily_stats,
            "category_performance": category_performance,
            "generated_at": datetime.utcnow().isoformat()
        }


_analytics_service_instance = None


def get_analytics_service() -> AnalyticsService:
    """Get or create analytics service instance."""
    global _analytics_service_instance
    if _analytics_service_instance is None:
        _analytics_service_instance = AnalyticsService()
    return _analytics_service_instance