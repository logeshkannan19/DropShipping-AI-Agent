"""
Store Automation Service Module

This module provides mock Shopify API integration:
- Create products
- Update prices
- Publish products
- Manage store operations
"""

import random
import uuid
from typing import List, Dict, Optional, Any
from datetime import datetime
from loguru import logger
from backend.config.settings import get_settings

settings = get_settings()


class StoreProduct:
    """Represents a product in the store."""
    
    def __init__(
        self,
        store_product_id: str,
        title: str,
        description: str,
        price: float,
        status: str = "draft",
        images: List[str] = None
    ):
        self.store_product_id = store_product_id
        self.title = title
        self.description = description
        self.price = price
        self.status = status
        self.images = images or []
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.variants = []
        self.tags = []


class StoreService:
    """
    Service for managing store operations.
    
    Provides mock Shopify API for store management.
    """
    
    def __init__(self):
        """Initialize the store service."""
        self.products: Dict[str, StoreProduct] = {}
        self.order_count = 0
        logger.info("StoreService initialized (mock Shopify API)")
    
    def _generate_product_id(self) -> str:
        """Generate a unique store product ID."""
        return f"SHOPIFY-{random.randint(100000, 999999)}"
    
    async def create_product(
        self,
        title: str,
        description: str,
        price: float,
        images: List[str] = None,
        tags: List[str] = None,
        vendor: str = "Dropshipping Store"
    ) -> Dict[str, Any]:
        """
        Create a new product in the store.
        
        Args:
            title: Product title
            description: Product description
            price: Selling price
            images: List of image URLs
            tags: Product tags
            vendor: Product vendor
            
        Returns:
            Created product data
        """
        logger.info(f"Creating product: {title}")
        
        # Simulate API delay
        await self._simulate_delay()
        
        store_product_id = self._generate_product_id()
        
        product = StoreProduct(
            store_product_id=store_product_id,
            title=title,
            description=description,
            price=price,
            status="draft",
            images=images
        )
        
        if tags:
            product.tags = tags
        
        self.products[store_product_id] = product
        
        logger.info(f"Product created with ID: {store_product_id}")
        
        return {
            "success": True,
            "store_product_id": store_product_id,
            "title": title,
            "status": "draft",
            "created_at": product.created_at.isoformat()
        }
    
    async def update_product(
        self,
        store_product_id: str,
        title: str = None,
        description: str = None,
        price: float = None,
        images: List[str] = None,
        status: str = None
    ) -> Dict[str, Any]:
        """
        Update an existing product.
        
        Args:
            store_product_id: Store product ID
            title: New title
            description: New description
            price: New price
            images: New images
            status: New status
            
        Returns:
            Update result
        """
        await self._simulate_delay()
        
        product = self.products.get(store_product_id)
        if not product:
            return {"success": False, "message": "Product not found"}
        
        if title is not None:
            product.title = title
        if description is not None:
            product.description = description
        if price is not None:
            product.price = price
        if images is not None:
            product.images = images
        if status is not None:
            product.status = status
        
        product.updated_at = datetime.utcnow()
        
        logger.info(f"Product {store_product_id} updated")
        
        return {
            "success": True,
            "store_product_id": store_product_id,
            "updated_fields": {
                "title": title,
                "description": description,
                "price": price,
                "status": status
            }
        }
    
    async def update_price(
        self,
        store_product_id: str,
        new_price: float
    ) -> Dict[str, Any]:
        """
        Update product price.
        
        Args:
            store_product_id: Store product ID
            new_price: New price
            
        Returns:
            Update result
        """
        await self._simulate_delay()
        
        product = self.products.get(store_product_id)
        if not product:
            return {"success": False, "message": "Product not found"}
        
        old_price = product.price
        product.price = new_price
        product.updated_at = datetime.utcnow()
        
        logger.info(f"Price updated for {store_product_id}: {old_price} -> {new_price}")
        
        return {
            "success": True,
            "store_product_id": store_product_id,
            "old_price": old_price,
            "new_price": new_price,
            "change_percent": round((new_price - old_price) / old_price * 100, 2)
        }
    
    async def publish_product(self, store_product_id: str) -> Dict[str, Any]:
        """
        Publish a product (change status to active).
        
        Args:
            store_product_id: Store product ID
            
        Returns:
            Publish result
        """
        await self._simulate_delay()
        
        product = self.products.get(store_product_id)
        if not product:
            return {"success": False, "message": "Product not found"}
        
        if product.status == "active":
            return {"success": True, "message": "Product already published", "status": "active"}
        
        product.status = "active"
        product.updated_at = datetime.utcnow()
        
        logger.info(f"Product {store_product_id} published")
        
        return {
            "success": True,
            "store_product_id": store_product_id,
            "status": "active",
            "product_url": f"https://store.example.com/products/{store_product_id}"
        }
    
    async def unpublish_product(self, store_product_id: str) -> Dict[str, Any]:
        """
        Unpublish a product (change status to draft).
        
        Args:
            store_product_id: Store product ID
            
        Returns:
            Result
        """
        await self._simulate_delay()
        
        product = self.products.get(store_product_id)
        if not product:
            return {"success": False, "message": "Product not found"}
        
        product.status = "draft"
        product.updated_at = datetime.utcnow()
        
        logger.info(f"Product {store_product_id} unpublished")
        
        return {
            "success": True,
            "store_product_id": store_product_id,
            "status": "draft"
        }
    
    async def delete_product(self, store_product_id: str) -> Dict[str, Any]:
        """
        Delete a product from the store.
        
        Args:
            store_product_id: Store product ID
            
        Returns:
            Deletion result
        """
        await self._simulate_delay()
        
        if store_product_id not in self.products:
            return {"success": False, "message": "Product not found"}
        
        del self.products[store_product_id]
        
        logger.info(f"Product {store_product_id} deleted")
        
        return {
            "success": True,
            "message": "Product deleted"
        }
    
    async def get_product(self, store_product_id: str) -> Optional[Dict[str, Any]]:
        """
        Get product details.
        
        Args:
            store_product_id: Store product ID
            
        Returns:
            Product data or None
        """
        await self._simulate_delay()
        
        product = self.products.get(store_product_id)
        if not product:
            return None
        
        return {
            "store_product_id": product.store_product_id,
            "title": product.title,
            "description": product.description,
            "price": product.price,
            "status": product.status,
            "images": product.images,
            "tags": product.tags,
            "created_at": product.created_at.isoformat(),
            "updated_at": product.updated_at.isoformat()
        }
    
    async def list_products(
        self,
        status: str = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        List products in the store.
        
        Args:
            status: Filter by status
            limit: Maximum number of products
            
        Returns:
            List of products
        """
        await self._simulate_delay()
        
        products = list(self.products.values())
        
        if status:
            products = [p for p in products if p.status == status]
        
        products = products[:limit]
        
        return [
            {
                "store_product_id": p.store_product_id,
                "title": p.title,
                "price": p.price,
                "status": p.status,
                "created_at": p.created_at.isoformat()
            }
            for p in products
        ]
    
    async def simulate_order(
        self,
        store_product_id: str,
        quantity: int = 1
    ) -> Dict[str, Any]:
        """
        Simulate an order for a product.
        
        Args:
            store_product_id: Store product ID
            quantity: Order quantity
            
        Returns:
            Order details
        """
        await self._simulate_delay()
        
        product = self.products.get(store_product_id)
        if not product:
            return {"success": False, "message": "Product not found"}
        
        if product.status != "active":
            return {"success": False, "message": "Product is not active"}
        
        self.order_count += 1
        
        order_id = f"ORD-{random.randint(100000, 999999)}"
        total_price = product.price * quantity
        
        logger.info(f"Order {order_id} created for product {store_product_id}")
        
        return {
            "success": True,
            "order_id": order_id,
            "store_product_id": store_product_id,
            "product_title": product.title,
            "quantity": quantity,
            "unit_price": product.price,
            "total_price": total_price,
            "order_date": datetime.utcnow().isoformat()
        }
    
    async def get_store_stats(self) -> Dict[str, Any]:
        """
        Get store statistics.
        
        Returns:
            Store statistics
        """
        await self._simulate_delay()
        
        active_products = [p for p in self.products.values() if p.status == "active"]
        draft_products = [p for p in self.products.values() if p.status == "draft"]
        
        return {
            "total_products": len(self.products),
            "active_products": len(active_products),
            "draft_products": len(draft_products),
            "total_orders": self.order_count,
            "total_revenue": sum(p.price for p in active_products)
        }
    
    async def _simulate_delay(self) -> None:
        """Simulate API delay."""
        import asyncio
        await asyncio.sleep(random.uniform(0.1, 0.3))


_store_service_instance = None


def get_store_service() -> StoreService:
    """Get or create store service instance."""
    global _store_service_instance
    if _store_service_instance is None:
        _store_service_instance = StoreService()
    return _store_service_instance