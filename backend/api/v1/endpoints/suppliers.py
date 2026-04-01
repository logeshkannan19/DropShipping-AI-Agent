"""Suppliers API endpoints."""

from typing import List, Optional
import random
import asyncio

from fastapi import APIRouter, HTTPException, Depends, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db


router = APIRouter(prefix="/api/v1/suppliers", tags=["Suppliers"])


class SupplierResponse(BaseModel):
    """Supplier response model."""
    
    supplier_id: str
    name: str
    rating: float
    shipping_time_days: int
    location: str
    categories: List[str]
    is_active: bool = True


class SupplierProductResponse(BaseModel):
    """Supplier product response model."""
    
    product_id: str
    supplier_id: str
    supplier_name: str
    name: str
    cost_price: float
    stock_quantity: int
    min_order_quantity: int = 1
    supplier_rating: float
    shipping_time_days: int


class StockCheckResponse(BaseModel):
    """Stock check response model."""
    
    available: bool
    product_id: str
    requested_quantity: int
    available_quantity: int
    estimated_restock_date: Optional[str] = None


class OrderResponse(BaseModel):
    """Order response model."""
    
    success: bool
    order_id: Optional[str] = None
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    quantity: Optional[int] = None
    unit_cost: Optional[float] = None
    total_cost: Optional[float] = None
    supplier_id: Optional[str] = None
    estimated_delivery: Optional[str] = None
    tracking_number: Optional[str] = None
    message: Optional[str] = None


SUPPLIERS_DATA = {
    "SUP-001": {
        "supplier_id": "SUP-001",
        "name": "Global Trade Co",
        "rating": 4.8,
        "shipping_time_days": 12,
        "location": "China",
        "categories": ["Electronics", "Home & Garden"]
    },
    "SUP-002": {
        "supplier_id": "SUP-002",
        "name": "FastShip Trading",
        "rating": 4.5,
        "shipping_time_days": 8,
        "location": "China",
        "categories": ["Fashion", "Beauty"]
    },
    "SUP-003": {
        "supplier_id": "SUP-003",
        "name": "Quality Goods Inc",
        "rating": 4.9,
        "shipping_time_days": 15,
        "location": "Vietnam",
        "categories": ["Sports", "Toys"]
    },
    "SUP-004": {
        "supplier_id": "SUP-004",
        "name": "Express Wholesale",
        "rating": 4.3,
        "shipping_time_days": 7,
        "location": "China",
        "categories": ["Automotive", "Electronics"]
    },
    "SUP-005": {
        "supplier_id": "SUP-005",
        "name": "Eco Products Ltd",
        "rating": 4.7,
        "shipping_time_days": 14,
        "location": "India",
        "categories": ["Health", "Home & Garden"]
    }
}

PRODUCTS_DATA = {
    "PROD-001": {
        "product_id": "PROD-001",
        "supplier_id": "SUP-001",
        "name": "Wireless Bluetooth Earbuds",
        "cost_price": 15.99,
        "stock_quantity": 500
    },
    "PROD-002": {
        "product_id": "PROD-002",
        "supplier_id": "SUP-001",
        "name": "Smart Watch Band",
        "cost_price": 8.99,
        "stock_quantity": 1000
    },
    "PROD-003": {
        "product_id": "PROD-003",
        "supplier_id": "SUP-002",
        "name": "Yoga Leggings",
        "cost_price": 12.99,
        "stock_quantity": 800
    },
    "PROD-004": {
        "product_id": "PROD-004",
        "supplier_id": "SUP-002",
        "name": "Vitamin C Serum",
        "cost_price": 6.99,
        "stock_quantity": 1200
    },
    "PROD-005": {
        "product_id": "PROD-005",
        "supplier_id": "SUP-003",
        "name": "Resistance Bands Set",
        "cost_price": 9.99,
        "stock_quantity": 600
    }
}


@router.get("", response_model=List[SupplierResponse])
async def list_suppliers(
    category: Optional[str] = None
):
    """
    List all available suppliers.
    
    Args:
        category: Filter by category
    """
    suppliers = list(SUPPLIERS_DATA.values())
    
    if category:
        suppliers = [
            s for s in suppliers
            if category in s["categories"]
        ]
    
    return [
        SupplierResponse(
            supplier_id=s["supplier_id"],
            name=s["name"],
            rating=s["rating"],
            shipping_time_days=s["shipping_time_days"],
            location=s["location"],
            categories=s["categories"],
            is_active=True
        )
        for s in suppliers
    ]


@router.get("/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(supplier_id: str):
    """
    Get supplier details.
    
    Args:
        supplier_id: Supplier ID
    """
    supplier = SUPPLIERS_DATA.get(supplier_id)
    
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier {supplier_id} not found"
        )
    
    return SupplierResponse(
        supplier_id=supplier["supplier_id"],
        name=supplier["name"],
        rating=supplier["rating"],
        shipping_time_days=supplier["shipping_time_days"],
        location=supplier["location"],
        categories=supplier["categories"],
        is_active=True
    )


@router.get("/{supplier_id}/products", response_model=List[SupplierProductResponse])
async def get_supplier_products(supplier_id: str):
    """
    Get products from a specific supplier.
    
    Args:
        supplier_id: Supplier ID
    """
    supplier = SUPPLIERS_DATA.get(supplier_id)
    
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier {supplier_id} not found"
        )
    
    supplier_products = [
        p for p in PRODUCTS_DATA.values()
        if p["supplier_id"] == supplier_id
    ]
    
    return [
        SupplierProductResponse(
            product_id=p["product_id"],
            supplier_id=p["supplier_id"],
            supplier_name=supplier["name"],
            name=p["name"],
            cost_price=p["cost_price"],
            stock_quantity=p["stock_quantity"],
            min_order_quantity=1,
            supplier_rating=supplier["rating"],
            shipping_time_days=supplier["shipping_time_days"]
        )
        for p in supplier_products
    ]


@router.get("/products", response_model=List[SupplierProductResponse])
async def list_all_products():
    """
    List all products from all suppliers.
    """
    return [
        SupplierProductResponse(
            product_id=p["product_id"],
            supplier_id=p["supplier_id"],
            supplier_name=SUPPLIERS_DATA[p["supplier_id"]]["name"],
            name=p["name"],
            cost_price=p["cost_price"],
            stock_quantity=p["stock_quantity"],
            min_order_quantity=1,
            supplier_rating=SUPPLIERS_DATA[p["supplier_id"]]["rating"],
            shipping_time_days=SUPPLIERS_DATA[p["supplier_id"]]["shipping_time_days"]
        )
        for p in PRODUCTS_DATA.values()
    ]


@router.get("/products/{product_id}/stock", response_model=StockCheckResponse)
async def check_stock(
    product_id: str,
    quantity: int = Query(1, ge=1)
):
    """
    Check product stock availability.
    
    Args:
        product_id: Product ID
        quantity: Required quantity
    """
    product = PRODUCTS_DATA.get(product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found"
        )
    
    available = product["stock_quantity"] >= quantity
    
    return StockCheckResponse(
        available=available,
        product_id=product_id,
        requested_quantity=quantity,
        available_quantity=product["stock_quantity"],
        estimated_restock_date=None if available else "2024-12-31"
    )


@router.post("/order", response_model=OrderResponse)
async def place_order(
    product_id: str,
    quantity: int = Query(1, ge=1),
    shipping_address: str = "Warehouse"
):
    """
    Place an order with a supplier.
    
    Args:
        product_id: Product ID to order
        quantity: Order quantity
        shipping_address: Shipping destination
    """
    await asyncio.sleep(0.1)
    
    product = PRODUCTS_DATA.get(product_id)
    
    if not product:
        return OrderResponse(
            success=False,
            message=f"Product {product_id} not found"
        )
    
    if product["stock_quantity"] < quantity:
        return OrderResponse(
            success=False,
            message=f"Insufficient stock. Available: {product['stock_quantity']}"
        )
    
    supplier = SUPPLIERS_DATA[product["supplier_id"]]
    total_cost = product["cost_price"] * quantity
    
    PRODUCTS_DATA[product_id]["stock_quantity"] -= quantity
    
    return OrderResponse(
        success=True,
        order_id=f"ORD-{random.randint(10000, 99999)}",
        product_id=product_id,
        product_name=product["name"],
        quantity=quantity,
        unit_cost=product["cost_price"],
        total_cost=total_cost,
        supplier_id=product["supplier_id"],
        estimated_delivery="2024-12-15",
        tracking_number=f"TRK{random.randint(100000, 999999)}"
    )
