"""Store API endpoints (Mock Shopify)."""

from typing import List, Optional
from datetime import datetime
import random
import asyncio

from fastapi import APIRouter, HTTPException, Depends, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db


router = APIRouter(prefix="/api/v1/store", tags=["Store"])


class StoreProductCreate(BaseModel):
    """Schema for creating a store product."""
    
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    images: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    vendor: str = "Dropshipping Store"


class StoreProductUpdate(BaseModel):
    """Schema for updating a store product."""
    
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    images: Optional[List[str]] = None
    status: Optional[str] = None


class StoreProductResponse(BaseModel):
    """Store product response model."""
    
    store_product_id: str
    title: str
    description: Optional[str]
    price: float
    status: str
    images: List[str]
    tags: List[str]
    vendor: str
    created_at: str
    updated_at: str


class StoreOrderResponse(BaseModel):
    """Store order response model."""
    
    success: bool
    order_id: Optional[str] = None
    store_product_id: Optional[str] = None
    product_title: Optional[str] = None
    quantity: int
    unit_price: float
    total_price: float
    order_date: str


class StoreStatsResponse(BaseModel):
    """Store statistics response model."""
    
    total_products: int
    active_products: int
    draft_products: int
    total_orders: int
    total_revenue: float


MOCK_STORE = {}


@router.get("/products", response_model=List[StoreProductResponse])
async def list_store_products(
    status: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100)
):
    """
    List products in the store.
    
    Args:
        status: Filter by status (draft/active)
        limit: Maximum number of products to return
    """
    products = list(MOCK_STORE.values())
    
    if status:
        products = [p for p in products if p["status"] == status]
    
    products = products[:limit]
    
    return [
        StoreProductResponse(
            store_product_id=p["store_product_id"],
            title=p["title"],
            description=p["description"],
            price=p["price"],
            status=p["status"],
            images=p["images"],
            tags=p["tags"],
            vendor=p["vendor"],
            created_at=p["created_at"],
            updated_at=p["updated_at"]
        )
        for p in products
    ]


@router.get("/products/{store_product_id}", response_model=StoreProductResponse)
async def get_store_product(store_product_id: str):
    """
    Get store product details.
    
    Args:
        store_product_id: Store product ID
    """
    product = MOCK_STORE.get(store_product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {store_product_id} not found"
        )
    
    return StoreProductResponse(
        store_product_id=product["store_product_id"],
        title=product["title"],
        description=product["description"],
        price=product["price"],
        status=product["status"],
        images=product["images"],
        tags=product["tags"],
        vendor=product["vendor"],
        created_at=product["created_at"],
        updated_at=product["updated_at"]
    )


@router.post("/products", response_model=StoreProductResponse)
async def create_store_product(product: StoreProductCreate):
    """
    Create a new product in the store.
    
    Args:
        product: Product data
    """
    await asyncio.sleep(0.1)
    
    store_product_id = f"SHOPIFY-{random.randint(100000, 999999)}"
    now = datetime.utcnow().isoformat()
    
    store_product = {
        "store_product_id": store_product_id,
        "title": product.title,
        "description": product.description,
        "price": product.price,
        "status": "draft",
        "images": product.images,
        "tags": product.tags,
        "vendor": product.vendor,
        "created_at": now,
        "updated_at": now
    }
    
    MOCK_STORE[store_product_id] = store_product
    
    return StoreProductResponse(**store_product)


@router.patch("/products/{store_product_id}", response_model=StoreProductResponse)
async def update_store_product(
    store_product_id: str,
    product_update: StoreProductUpdate
):
    """
    Update a store product.
    
    Args:
        store_product_id: Store product ID
        product_update: Fields to update
    """
    product = MOCK_STORE.get(store_product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {store_product_id} not found"
        )
    
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        product[field] = value
    
    product["updated_at"] = datetime.utcnow().isoformat()
    
    return StoreProductResponse(**product)


@router.post("/products/{store_product_id}/publish", response_model=StoreProductResponse)
async def publish_store_product(store_product_id: str):
    """
    Publish a store product.
    
    Args:
        store_product_id: Store product ID
    """
    product = MOCK_STORE.get(store_product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {store_product_id} not found"
        )
    
    if product["status"] == "active":
        return StoreProductResponse(**product)
    
    product["status"] = "active"
    product["updated_at"] = datetime.utcnow().isoformat()
    
    return StoreProductResponse(**product)


@router.post("/products/{store_product_id}/unpublish", response_model=StoreProductResponse)
async def unpublish_store_product(store_product_id: str):
    """
    Unpublish a store product.
    
    Args:
        store_product_id: Store product ID
    """
    product = MOCK_STORE.get(store_product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {store_product_id} not found"
        )
    
    product["status"] = "draft"
    product["updated_at"] = datetime.utcnow().isoformat()
    
    return StoreProductResponse(**product)


@router.delete("/products/{store_product_id}")
async def delete_store_product(store_product_id: str):
    """
    Delete a store product.
    
    Args:
        store_product_id: Store product ID
    """
    if store_product_id not in MOCK_STORE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {store_product_id} not found"
        )
    
    del MOCK_STORE[store_product_id]
    
    return {"success": True, "message": "Product deleted"}


@router.post("/products/{store_product_id}/order", response_model=StoreOrderResponse)
async def create_store_order(
    store_product_id: str,
    quantity: int = Query(1, ge=1)
):
    """
    Simulate an order for a store product.
    
    Args:
        store_product_id: Store product ID
        quantity: Order quantity
    """
    await asyncio.sleep(0.1)
    
    product = MOCK_STORE.get(store_product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {store_product_id} not found"
        )
    
    if product["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product is not active"
        )
    
    total_price = product["price"] * quantity
    
    return StoreOrderResponse(
        success=True,
        order_id=f"ORD-{random.randint(100000, 999999)}",
        store_product_id=store_product_id,
        product_title=product["title"],
        quantity=quantity,
        unit_price=product["price"],
        total_price=total_price,
        order_date=datetime.utcnow().isoformat()
    )


@router.get("/stats", response_model=StoreStatsResponse)
async def get_store_stats():
    """
    Get store statistics.
    """
    products = list(MOCK_STORE.values())
    active = [p for p in products if p["status"] == "active"]
    draft = [p for p in products if p["status"] == "draft"]
    
    return StoreStatsResponse(
        total_products=len(products),
        active_products=len(active),
        draft_products=len(draft),
        total_orders=0,
        total_revenue=sum(p["price"] for p in active)
    )
