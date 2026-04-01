"""Product Research Agent Module."""

import random
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import asyncio


@dataclass
class Product:
    """Product data class."""
    
    name: str
    category: str
    cost_price: float
    rating: float
    review_count: int
    estimated_orders: int
    supplier_id: str
    supplier_rating: float
    shipping_time_days: int
    stock_quantity: int
    description: Optional[str] = None
    source: str = "scraped"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "category": self.category,
            "cost_price": self.cost_price,
            "rating": self.rating,
            "review_count": self.review_count,
            "estimated_orders": self.estimated_orders,
            "supplier_id": self.supplier_id,
            "supplier_rating": self.supplier_rating,
            "shipping_time_days": self.shipping_time_days,
            "stock_quantity": self.stock_quantity,
            "description": self.description,
            "source": self.source
        }


class ProductResearchAgent:
    """
    Agent responsible for researching and scraping trending products.
    
    Supports both mock mode (for testing) and real scraping mode.
    """
    
    CATEGORIES = [
        "Electronics", "Home & Garden", "Fashion", "Beauty",
        "Sports", "Toys", "Automotive", "Health"
    ]
    
    PRODUCT_TEMPLATES = [
        ("Wireless Bluetooth Headphones", "Electronics", 25.99, 4.5, 1250),
        ("Smart LED Desk Lamp", "Electronics", 35.99, 4.3, 890),
        ("Yoga Mat Premium", "Sports", 19.99, 4.7, 2100),
        ("Stainless Steel Water Bottle", "Home & Garden", 15.99, 4.4, 1800),
        ("Organic Face Serum", "Beauty", 28.99, 4.6, 950),
        ("Portable Phone Charger", "Electronics", 22.99, 4.2, 3200),
        ("Cozy Blanket Throw", "Home & Garden", 32.99, 4.5, 750),
        ("Fitness Tracker Watch", "Electronics", 45.99, 4.1, 1500),
        ("Kitchen Knife Set", "Home & Garden", 29.99, 4.4, 620),
        ("Scented Candle Collection", "Home & Garden", 18.99, 4.8, 2800),
        ("Wireless Mouse", "Electronics", 15.99, 4.3, 4500),
        ("Running Shoes", "Sports", 55.99, 4.6, 1100),
        ("Skeleton Hoodie", "Fashion", 24.99, 4.2, 890),
        ("Skincare Kit", "Beauty", 38.99, 4.5, 670),
        ("Car Phone Mount", "Automotive", 12.99, 4.1, 5600),
        ("Resistance Bands Set", "Sports", 14.99, 4.7, 3200),
        ("LED Strip Lights", "Electronics", 19.99, 4.4, 4100),
        ("Cotton T-Shirt Pack", "Fashion", 21.99, 4.3, 2200),
        ("Vitamin Supplements", "Health", 24.99, 4.5, 1800),
        ("Pet Toy Set", "Toys", 16.99, 4.6, 1900),
    ]
    
    def __init__(self, mock_mode: bool = True):
        """
        Initialize the product research agent.
        
        Args:
            mock_mode: Whether to use mock data
        """
        self.mock_mode = mock_mode
    
    async def research_products(
        self,
        limit: int = 20,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Research trending products.
        
        Args:
            limit: Maximum number of products to fetch
            category: Optional category filter
            
        Returns:
            List of product dictionaries
        """
        if self.mock_mode:
            return await self._generate_mock_products(limit, category)
        else:
            return await self._scrape_real_products(limit, category)
    
    async def _generate_mock_products(
        self,
        limit: int,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Generate mock product data."""
        await asyncio.sleep(0.3)
        
        products = []
        templates = self.PRODUCT_TEMPLATES
        
        if category:
            templates = [t for t in templates if t[1] == category]
            if not templates:
                templates = self.PRODUCT_TEMPLATES
        
        for name, cat, cost, rating, orders in templates[:limit]:
            cost_variance = random.uniform(0.9, 1.1)
            
            product = Product(
                name=name,
                category=cat,
                cost_price=round(cost * cost_variance, 2),
                rating=round(random.uniform(max(1, rating - 0.2), min(5, rating + 0.2)), 1),
                review_count=max(0, orders + random.randint(-200, 200)),
                estimated_orders=max(0, orders + random.randint(-200, 200)),
                supplier_id=f"SUP-{random.randint(1000, 9999)}",
                supplier_rating=round(random.uniform(4.0, 5.0), 1),
                shipping_time_days=random.randint(7, 21),
                stock_quantity=random.randint(100, 1000),
                description=f"High-quality {name.lower()} - perfect for everyday use.",
                source="mock"
            )
            
            products.append(product.to_dict())
        
        return products
    
    async def _scrape_real_products(
        self,
        limit: int,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Scrape real products (placeholder)."""
        return await self._generate_mock_products(limit, category)
    
    async def analyze_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a product and compute additional metrics.
        
        Args:
            product_data: Raw product data
            
        Returns:
            Product data with analysis
        """
        cost = product_data.get("cost_price", 0)
        rating = product_data.get("rating", 0)
        orders = product_data.get("estimated_orders", 0)
        
        base_score = (rating / 5.0) * 0.3 + min(orders / 5000, 1.0) * 0.4
        if cost < 20:
            base_score += 0.2
        elif cost < 40:
            base_score += 0.1
        
        product_data["profitability_score"] = round(base_score, 3)
        product_data["trend_indicator"] = "up" if orders > 1500 else "stable"
        
        return product_data
