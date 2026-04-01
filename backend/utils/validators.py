"""Data validation utilities."""

from typing import Any, Dict, List, Optional, Type, TypeVar
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime
import re

T = TypeVar("T", bound=BaseModel)


class ProductValidator(BaseModel):
    """Validator for product data."""
    
    name: str = Field(..., min_length=1, max_length=500)
    price: float = Field(..., gt=0)
    cost: float = Field(..., ge=0)
    rating: float = Field(..., ge=0, le=5)
    reviews: int = Field(..., ge=0)
    orders: int = Field(..., ge=0)
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate product name."""
        if not v.strip():
            raise ValueError("Product name cannot be empty")
        return v.strip()
    
    @field_validator("price", "cost")
    @classmethod
    def validate_price(cls, v: float) -> float:
        """Validate price values."""
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return round(v, 2)


class PricingRequestValidator(BaseModel):
    """Validator for pricing request."""
    
    cost: float = Field(..., gt=0)
    competitor_price: Optional[float] = Field(None, gt=0)
    demand_score: float = Field(..., ge=0, le=1)
    category: Optional[str] = Field(None, max_length=100)


class DemandPredictionValidator(BaseModel):
    """Validator for demand prediction input."""
    
    price: float = Field(..., gt=0)
    rating: float = Field(..., ge=0, le=5)
    reviews: int = Field(..., ge=0)
    orders: int = Field(..., ge=0)
    competition_level: int = Field(..., ge=1, le=10)
    shipping_time: int = Field(..., ge=0)
    supplier_rating: float = Field(..., ge=0, le=5)
    category_popularity: float = Field(..., ge=0, le=1)


def validate_data(model: Type[T], data: Dict[str, Any]) -> T:
    """
    Validate data against a Pydantic model.
    
    Args:
        model: The Pydantic model class
        data: Dictionary of data to validate
        
    Returns:
        Validated model instance
        
    Raises:
        ValidationError: If validation fails
    """
    return model(**data)


def validate_batch(model: Type[T], data_list: List[Dict[str, Any]]) -> List[T]:
    """
    Validate a batch of data against a Pydantic model.
    
    Args:
        model: The Pydantic model class
        data_list: List of dictionaries to validate
        
    Returns:
        List of validated model instances
    """
    return [model(**data) for data in data_list]


def sanitize_string(text: str) -> str:
    """Sanitize a string by removing potentially harmful characters."""
    if not text:
        return ""
    text = re.sub(r'[<>\"\'`]', '', text)
    return text.strip()


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url: str) -> bool:
    """Validate URL format."""
    pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
    return bool(re.match(pattern, url))


def validate_date_range(start_date: datetime, end_date: datetime) -> bool:
    """Validate that a date range is valid."""
    return start_date < end_date
