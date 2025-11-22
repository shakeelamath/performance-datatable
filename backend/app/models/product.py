"""Product database model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, Index
from sqlalchemy.sql import func

from app.database import Base


class Product(Base):
    """Product model with optimized indexing."""
    
    __tablename__ = "products"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Information
    sku = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Categorization
    category = Column(String(100), nullable=False, index=True)
    brand = Column(String(100), nullable=False, index=True)
    
    # Pricing & Inventory
    price = Column(Numeric(10, 2), nullable=False, index=True)
    stock_quantity = Column(Integer, nullable=False, default=0)
    
    # Ratings
    rating = Column(Numeric(3, 2), nullable=False, default=0.0)
    reviews_count = Column(Integer, nullable=False, default=0)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Composite indexes for common query patterns
    __table_args__ = (
        Index('idx_category_price', 'category', 'price'),
        Index('idx_brand_price', 'brand', 'price'),
        Index('idx_created_at_desc', created_at.desc()),
        Index('idx_price_desc', price.desc()),
        Index('idx_rating_desc', rating.desc()),
    )
    
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, sku='{self.sku}', name='{self.name}')>"
