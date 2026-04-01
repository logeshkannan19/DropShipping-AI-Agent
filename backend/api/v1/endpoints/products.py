"""Products API endpoints."""

from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.core.config import settings


router = APIRouter(prefix="/api/v1/products", tags=["Products"])


class ProductBase(BaseModel):
    """Base product schema."""
    
    name: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    category: Optional[str] = None
    cost_price: float = Field(..., gt=0)


class ProductCreate(ProductBase):
    """Schema for creating a product."""
    
    rating: Optional[float] = Field(None, ge=0, le=5)
    review_count: Optional[int] = Field(None, ge=0)
    estimated_orders: Optional[int] = Field(None, ge=0)
    supplier_id: Optional[str] = None
    supplier_rating: Optional[float] = Field(None, ge=0, le=5)
    shipping_time_days: Optional[int] = Field(None, ge=0)
    stock_quantity: Optional[int] = Field(None, ge=0)


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    category: Optional[str] = None
    cost_price: Optional[float] = Field(None, gt=0)
    selling_price: Optional[float] = Field(None, gt=0)
    rating: Optional[float] = Field(None, ge=0, le=5)
    review_count: Optional[int] = Field(None, ge=0)
    demand_score: Optional[float] = Field(None, ge=0, le=1)
    is_published: Optional[bool] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    """Schema for product response."""
    
    id: int
    selling_price: Optional[float] = None
    margin_percent: Optional[float] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    estimated_orders: Optional[int] = None
    demand_score: Optional[float] = None
    supplier_id: Optional[str] = None
    supplier_rating: Optional[float] = None
    shipping_time_days: Optional[int] = None
    stock_quantity: Optional[int] = None
    is_active: bool = True
    is_published: bool = False
    source: str = "manual"
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Schema for list of products."""
    
    products: List[ProductResponse]
    total: int
    skip: int
    limit: int


class DemandPredictionRequest(BaseModel):
    """Request schema for demand prediction."""
    
    category: str = Field(..., description="Product category")
    price: float = Field(..., gt=0, description="Product price")
    rating: float = Field(..., ge=0, le=5, description="Product rating")
    review_count: int = Field(..., ge=0, description="Number of reviews")
    competitor_count: int = Field(..., ge=1, description="Number of competitors")
    supplier_rating: float = Field(..., ge=0, le=5, description="Supplier rating")
    shipping_days: int = Field(..., ge=0, description="Shipping time in days")


class DemandPredictionResponse(BaseModel):
    """Response schema for demand prediction."""
    
    demand_score: float = Field(..., ge=0, le=1)
    confidence: Optional[float] = Field(None, ge=0, le=1)
    factors: Optional[dict] = None


@router.get("", response_model=ProductListResponse)
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[str] = None,
    published_only: bool = False,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """
    List all products with optional filtering.
    
    Args:
        skip: Number of products to skip
        limit: Maximum number of products to return
        category: Filter by category
        published_only: Only return published products
        active_only: Only return active products
        db: Database session
    """
    from backend.core.database import ProductModel
    
    query = select(ProductModel)
    
    if category:
        query = query.where(ProductModel.category == category)
    if published_only:
        query = query.where(ProductModel.is_published == True)
    if active_only:
        query = query.where(ProductModel.is_active == True)
    
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    query = query.offset(skip).limit(limit).order_by(ProductModel.created_at.desc())
    result = await db.execute(query)
    products = result.scalars().all()
    
    return ProductListResponse(
        products=[ProductResponse.model_validate(p) for p in products],
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific product by ID.
    
    Args:
        product_id: Product ID
        db: Database session
    """
    from backend.core.database import ProductModel
    
    result = await db.execute(
        select(ProductModel).where(ProductModel.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    return ProductResponse.model_validate(product)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new product.
    
    Args:
        product: Product data
        db: Database session
    """
    from backend.core.database import ProductModel
    
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    
    return ProductResponse.model_validate(db_product)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing product.
    
    Args:
        product_id: Product ID
        product_update: Fields to update
        db: Database session
    """
    from backend.core.database import ProductModel
    
    result = await db.execute(
        select(ProductModel).where(ProductModel.id == product_id)
    )
    db_product = result.scalar_one_or_none()
    
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    await db.commit()
    await db.refresh(db_product)
    
    return ProductResponse.model_validate(db_product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a product.
    
    Args:
        product_id: Product ID
        db: Database session
    """
    from backend.core.database import ProductModel
    
    result = await db.execute(
        select(ProductModel).where(ProductModel.id == product_id)
    )
    db_product = result.scalar_one_or_none()
    
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    await db.delete(db_product)
    await db.commit()
