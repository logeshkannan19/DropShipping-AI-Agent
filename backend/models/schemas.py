from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base product schema."""
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    category: Optional[str] = Field(None, description="Product category")
    cost_price: float = Field(..., description="Cost price from supplier")


class ProductCreate(ProductBase):
    """Schema for creating a new product."""
    rating: Optional[float] = Field(None, description="Product rating")
    review_count: Optional[int] = Field(None, description="Number of reviews")
    estimated_orders: Optional[int] = Field(None, description="Estimated monthly orders")
    supplier_id: Optional[str] = Field(None, description="Supplier ID")
    supplier_rating: Optional[float] = Field(None, description="Supplier rating")
    shipping_time_days: Optional[int] = Field(None, description="Shipping time in days")
    stock_quantity: Optional[int] = Field(None, description="Available stock")


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    selling_price: Optional[float] = None
    margin_percent: Optional[float] = None
    demand_score: Optional[float] = None
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
    source: str = "scraped"
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Schema for list of products."""
    products: List[ProductResponse]
    total: int


class PredictDemandRequest(BaseModel):
    """Request schema for demand prediction."""
    category: str = Field(..., description="Product category")
    price: float = Field(..., description="Product price")
    rating: float = Field(..., description="Product rating")
    review_count: int = Field(..., description="Number of reviews")
    competitor_count: int = Field(..., description="Number of competitors")
    supplier_rating: float = Field(..., description="Supplier rating")
    shipping_days: int = Field(..., description="Shipping time in days")


class PredictDemandResponse(BaseModel):
    """Response schema for demand prediction."""
    demand_score: float = Field(..., description="Predicted demand score (0-1)")
    confidence: Optional[float] = Field(None, description="Model confidence")
    factors: Optional[dict] = Field(None, description="Key factors influencing prediction")


class OptimizePriceRequest(BaseModel):
    """Request schema for price optimization."""
    product_id: Optional[int] = Field(None, description="Product ID")
    cost_price: float = Field(..., description="Cost price from supplier")
    competitor_prices: List[float] = Field(..., description="Competitor prices")
    demand_score: float = Field(..., description="Demand score (0-1)")
    target_margin: float = Field(30.0, description="Target margin percentage")


class OptimizePriceResponse(BaseModel):
    """Response schema for price optimization."""
    optimal_price: float = Field(..., description="Optimal selling price")
    margin_percent: float = Field(..., description="Margin percentage")
    estimated_profit: float = Field(..., description="Estimated profit per unit")
    pricing_strategy: str = Field(..., description="Pricing strategy used")
    recommendations: List[str] = Field(default_factory=list, description="Additional recommendations")


class UploadProductRequest(BaseModel):
    """Request schema for uploading product to store."""
    product_id: int = Field(..., description="Product ID to upload")
    title: str = Field(..., description="Product title")
    description: str = Field(..., description="Product description")
    price: float = Field(..., description="Selling price")
    images: Optional[List[str]] = Field(default_factory=list, description="Image URLs")


class UploadProductResponse(BaseModel):
    """Response schema for product upload."""
    success: bool
    product_id: int
    store_product_id: Optional[str] = None
    message: str


class AnalyticsResponse(BaseModel):
    """Response schema for analytics data."""
    total_revenue: float
    total_profit: float
    total_sales: int
    active_products: int
    published_products: int
    conversion_rate: Optional[float] = None
    avg_order_value: Optional[float] = None
    top_products: List[dict] = Field(default_factory=list)
    daily_stats: List[dict] = Field(default_factory=list)


class AgentRunRequest(BaseModel):
    """Request schema for running the AI agent."""
    max_products: int = Field(10, description="Maximum products to analyze")
    min_demand_score: float = Field(0.5, description="Minimum demand score threshold")
    auto_publish: bool = Field(True, description="Auto publish selected products")


class AgentRunResponse(BaseModel):
    """Response schema for agent run."""
    run_id: int
    status: str
    products_analyzed: int
    products_selected: int
    products_published: int
    revenue_generated: float
    message: str


class SaleCreate(BaseModel):
    """Schema for creating a sale."""
    product_id: int
    quantity: int = 1
    unit_price: float
    customer_name: Optional[str] = None


class SaleResponse(BaseModel):
    """Response schema for sale."""
    id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float
    profit: float
    sale_date: datetime
    
    class Config:
        from_attributes = True