"""
Supplier Service Module

This module provides supplier management functionality:
- Mock supplier API with inventory and shipping info
- Supplier rating and performance tracking
- Stock level monitoring
"""

import asyncio
import random
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from loguru import logger
from backend.config.settings import get_settings

settings = get_settings()


class Supplier:
    """Supplier data model."""
    
    def __init__(
        self,
        supplier_id: str,
        name: str,
        rating: float,
        shipping_time_days: int,
        location: str,
        categories: List[str]
    ):
        self.supplier_id = supplier_id
        self.name = name
        self.rating = rating
        self.shipping_time_days = shipping_time_days
        self.location = location
        self.categories = categories


class SupplierProduct:
    """Product from supplier."""
    
    def __init__(
        self,
        product_id: str,
        supplier_id: str,
        name: str,
        cost_price: float,
        stock_quantity: int,
        min_order_quantity: int = 1
    ):
        self.product_id = product_id
        self.supplier_id = supplier_id
        self.name = name
        self.cost_price = cost_price
        self.stock_quantity = stock_quantity
        self.min_order_quantity = min_order_quantity


class SupplierService:
    """
    Service for managing supplier interactions.
    
    Provides mock supplier API with inventory and shipping info.
    """
    
    def __init__(self):
        """Initialize the supplier service."""
        self.suppliers = self._initialize_suppliers()
        self.products = self._initialize_products()
        logger.info(f"SupplierService initialized with {len(self.suppliers)} suppliers")
    
    def _initialize_suppliers(self) -> Dict[str, Supplier]:
        """Initialize mock suppliers."""
        suppliers = {
            "SUP-001": Supplier(
                supplier_id="SUP-001",
                name="Global Trade Co",
                rating=4.8,
                shipping_time_days=12,
                location="China",
                categories=["Electronics", "Home & Garden"]
            ),
            "SUP-002": Supplier(
                supplier_id="SUP-002",
                name="FastShip Trading",
                rating=4.5,
                shipping_time_days=8,
                location="China",
                categories=["Fashion", "Beauty"]
            ),
            "SUP-003": Supplier(
                supplier_id="SUP-003",
                name="Quality Goods Inc",
                rating=4.9,
                shipping_time_days=15,
                location="Vietnam",
                categories=["Sports", "Toys"]
            ),
            "SUP-004": Supplier(
                supplier_id="SUP-004",
                name="Express Wholesale",
                rating=4.3,
                shipping_time_days=7,
                location="China",
                categories=["Automotive", "Electronics"]
            ),
            "SUP-005": Supplier(
                supplier_id="SUP-005",
                name="Eco Products Ltd",
                rating=4.7,
                shipping_time_days=14,
                location="India",
                categories=["Health", "Home & Garden"]
            )
        }
        return suppliers
    
    def _initialize_products(self) -> Dict[str, SupplierProduct]:
        """Initialize mock supplier products."""
        products = {
            "PROD-001": SupplierProduct(
                product_id="PROD-001",
                supplier_id="SUP-001",
                name="Wireless Bluetooth Earbuds",
                cost_price=15.99,
                stock_quantity=500
            ),
            "PROD-002": SupplierProduct(
                product_id="PROD-002",
                supplier_id="SUP-001",
                name="Smart Watch Band",
                cost_price=8.99,
                stock_quantity=1000
            ),
            "PROD-003": SupplierProduct(
                product_id="PROD-003",
                supplier_id="SUP-002",
                name="Yoga Leggings",
                cost_price=12.99,
                stock_quantity=800
            ),
            "PROD-004": SupplierProduct(
                product_id="PROD-004",
                supplier_id="SUP-002",
                name="Vitamin C Serum",
                cost_price=6.99,
                stock_quantity=1200
            ),
            "PROD-005": SupplierProduct(
                product_id="PROD-005",
                supplier_id="SUP-003",
                name="Resistance Bands Set",
                cost_price=9.99,
                stock_quantity=600
            ),
            "PROD-006": SupplierProduct(
                product_id="PROD-006",
                supplier_id="SUP-003",
                name="Building Blocks Toy Set",
                cost_price=14.99,
                stock_quantity=400
            ),
            "PROD-007": SupplierProduct(
                product_id="PROD-007",
                supplier_id="SUP-004",
                name="Car Phone Mount",
                cost_price=5.99,
                stock_quantity=2000
            ),
            "PROD-008": SupplierProduct(
                product_id="PROD-008",
                supplier_id="SUP-004",
                name="Portable Charger 10000mAh",
                cost_price=18.99,
                stock_quantity=350
            ),
            "PROD-009": SupplierProduct(
                product_id="PROD-009",
                supplier_id="SUP-005",
                name="Organic Face Mask Pack",
                cost_price=4.99,
                stock_quantity=1500
            ),
            "PROD-010": SupplierProduct(
                product_id="PROD-010",
                supplier_id="SUP-005",
                name="Bamboo Cutting Board",
                cost_price=7.99,
                stock_quantity=900
            )
        }
        return products
    
    async def get_supplier(self, supplier_id: str) -> Optional[Dict[str, Any]]:
        """
        Get supplier information.
        
        Args:
            supplier_id: Supplier ID
            
        Returns:
            Supplier data or None
        """
        await asyncio.sleep(0.1)  # Simulate API call
        
        supplier = self.suppliers.get(supplier_id)
        if not supplier:
            logger.warning(f"Supplier {supplier_id} not found")
            return None
        
        return {
            "supplier_id": supplier.supplier_id,
            "name": supplier.name,
            "rating": supplier.rating,
            "shipping_time_days": supplier.shipping_time_days,
            "location": supplier.location,
            "categories": supplier.categories
        }
    
    async def get_suppliers_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get suppliers that offer a specific category.
        
        Args:
            category: Product category
            
        Returns:
            List of supplier data
        """
        await asyncio.sleep(0.1)
        
        matching = []
        for supplier in self.suppliers.values():
            if category in supplier.categories:
                matching.append({
                    "supplier_id": supplier.supplier_id,
                    "name": supplier.name,
                    "rating": supplier.rating,
                    "shipping_time_days": supplier.shipping_time_days,
                    "location": supplier.location
                })
        
        return matching
    
    async def get_supplier_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Get product information from a supplier.
        
        Args:
            product_id: Product ID
            
        Returns:
            Product data or None
        """
        await asyncio.sleep(0.1)
        
        product = self.products.get(product_id)
        if not product:
            logger.warning(f"Product {product_id} not found")
            return None
        
        supplier = self.suppliers.get(product.supplier_id)
        
        return {
            "product_id": product.product_id,
            "supplier_id": product.supplier_id,
            "supplier_name": supplier.name if supplier else "Unknown",
            "name": product.name,
            "cost_price": product.cost_price,
            "stock_quantity": product.stock_quantity,
            "min_order_quantity": product.min_order_quantity,
            "supplier_rating": supplier.rating if supplier else 0,
            "shipping_time_days": supplier.shipping_time_days if supplier else 0
        }
    
    async def check_stock(self, product_id: str, quantity: int = 1) -> Dict[str, Any]:
        """
        Check if product is in stock.
        
        Args:
            product_id: Product ID
            quantity: Required quantity
            
        Returns:
            Stock check result
        """
        await asyncio.sleep(0.1)
        
        product = self.products.get(product_id)
        if not product:
            return {"available": False, "reason": "Product not found"}
        
        available = product.stock_quantity >= quantity
        
        return {
            "available": available,
            "product_id": product_id,
            "requested_quantity": quantity,
            "available_quantity": product.stock_quantity,
            "estimated_restock_date": (
                (datetime.now() + timedelta(days=random.randint(5, 15))).strftime("%Y-%m-%d")
            ) if not available else None
        }
    
    async def place_order(
        self,
        product_id: str,
        quantity: int,
        shipping_address: str = "Warehouse"
    ) -> Dict[str, Any]:
        """
        Place an order with a supplier.
        
        Args:
            product_id: Product ID
            quantity: Order quantity
            shipping_address: Shipping destination
            
        Returns:
            Order confirmation
        """
        await asyncio.sleep(0.2)  # Simulate order processing
        
        product = self.products.get(product_id)
        if not product:
            return {"success": False, "message": "Product not found"}
        
        if product.stock_quantity < quantity:
            return {
                "success": False,
                "message": f"Insufficient stock. Available: {product.stock_quantity}"
            }
        
        # Simulate order
        order_id = f"ORD-{random.randint(10000, 99999)}"
        total_cost = product.cost_price * quantity
        
        # Reduce stock
        product.stock_quantity -= quantity
        
        return {
            "success": True,
            "order_id": order_id,
            "product_id": product_id,
            "product_name": product.name,
            "quantity": quantity,
            "unit_cost": product.cost_price,
            "total_cost": total_cost,
            "supplier_id": product.supplier_id,
            "estimated_delivery": (
                datetime.now() + timedelta(days=random.randint(7, 14))
            ).strftime("%Y-%m-%d"),
            "tracking_number": f"TRK{random.randint(100000, 999999)}"
        }
    
    async def get_supplier_performance(self, supplier_id: str) -> Dict[str, Any]:
        """
        Get supplier performance metrics.
        
        Args:
            supplier_id: Supplier ID
            
        Returns:
            Performance metrics
        """
        await asyncio.sleep(0.1)
        
        supplier = self.suppliers.get(supplier_id)
        if not supplier:
            return {"error": "Supplier not found"}
        
        # Generate mock performance data
        return {
            "supplier_id": supplier_id,
            "name": supplier.name,
            "rating": supplier.rating,
            "on_time_delivery_rate": round(random.uniform(90, 99), 1),
            "quality_score": round(random.uniform(4.0, 5.0), 1),
            "response_time_hours": random.randint(2, 24),
            "total_orders": random.randint(50, 500),
            "total_revenue": round(random.uniform(10000, 100000), 2)
        }
    
    def list_all_products(self) -> List[Dict[str, Any]]:
        """
        List all products from all suppliers.
        
        Returns:
            List of all products
        """
        result = []
        for product in self.products.values():
            supplier = self.suppliers.get(product.supplier_id)
            result.append({
                "product_id": product.product_id,
                "supplier_id": product.supplier_id,
                "supplier_name": supplier.name if supplier else "Unknown",
                "name": product.name,
                "cost_price": product.cost_price,
                "stock_quantity": product.stock_quantity,
                "supplier_rating": supplier.rating if supplier else 0,
                "shipping_time_days": supplier.shipping_time_days if supplier else 0
            })
        return result


_supplier_service_instance = None


def get_supplier_service() -> SupplierService:
    """Get or create supplier service instance."""
    global _supplier_service_instance
    if _supplier_service_instance is None:
        _supplier_service_instance = SupplierService()
    return _supplier_service_instance