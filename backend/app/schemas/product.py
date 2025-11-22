"""Product Pydantic schemas for request/response validation."""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    """Base product schema."""
    sku: str
    name: str
    description: Optional[str] = None
    category: str
    brand: str
    price: Decimal
    stock_quantity: int
    rating: Decimal
    reviews_count: int


class Product(ProductBase):
    """Product schema for list responses."""
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ProductDetail(ProductBase):
    """Product schema with full details."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ProductList(BaseModel):
    """Paginated product list response."""
    data: List[Product]
    total: int
    page: int
    limit: int
    pages: int


class ProductStats(BaseModel):
    """Aggregate statistics about products."""
    total_products: int
    total_categories: int
    total_brands: int
    price_min: Decimal
    price_max: Decimal
    avg_rating: Decimal
    total_stock: int


class CategoryList(BaseModel):
    """List of unique categories."""
    categories: List[str]
    total: int
