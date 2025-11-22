"""Product service with optimized queries."""
from typing import Optional, List
from decimal import Decimal
from sqlalchemy import select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductList, ProductDetail, ProductStats, CategoryList
from app.services.cache import cache_service
from app.config import settings


class ProductService:
    """Service for product operations with caching."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_products(
        self,
        page: int = 1,
        limit: int = 50,
        sort_by: str = "id",
        sort_order: str = "asc",
        category: Optional[str] = None,
        brand: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        search: Optional[str] = None,
    ) -> ProductList:
        """Get paginated products with filters and sorting."""
        
        # Generate cache key
        cache_params = {
            "page": page,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "category": category,
            "brand": brand,
            "min_price": min_price,
            "max_price": max_price,
            "search": search,
        }
        cache_key = cache_service._generate_key("products:list", cache_params)
        
        # Try to get from cache
        cached = await cache_service.get(cache_key)
        if cached:
            return ProductList(**cached)
        
        # Build query
        query = select(Product)
        
        # Apply filters
        if category:
            query = query.where(Product.category == category)
        if brand:
            query = query.where(Product.brand == brand)
        if min_price is not None:
            query = query.where(Product.price >= min_price)
        if max_price is not None:
            query = query.where(Product.price <= max_price)
        if search:
            search_term = f"%{search}%"
            query = query.where(
                (Product.name.ilike(search_term)) |
                (Product.description.ilike(search_term)) |
                (Product.sku.ilike(search_term))
            )
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        result = await self.db.execute(count_query)
        total = result.scalar_one()
        
        # Apply sorting
        sort_column = getattr(Product, sort_by, Product.id)
        if sort_order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # Apply pagination
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)
        
        # Execute query
        result = await self.db.execute(query)
        products = result.scalars().all()
        
        # Calculate pages
        pages = (total + limit - 1) // limit
        
        # Build response
        response = ProductList(
            data=products,
            total=total,
            page=page,
            limit=limit,
            pages=pages,
        )
        
        # Cache the response
        await cache_service.set(
            cache_key,
            response.model_dump(mode='json'),
            ttl=settings.CACHE_TTL_LIST
        )
        
        return response
    
    async def get_product(self, product_id: int) -> Optional[ProductDetail]:
        """Get single product by ID."""
        
        # Try cache first
        cache_key = f"products:detail:{product_id}"
        cached = await cache_service.get(cache_key)
        if cached:
            return ProductDetail(**cached)
        
        # Query database
        query = select(Product).where(Product.id == product_id)
        result = await self.db.execute(query)
        product = result.scalar_one_or_none()
        
        if not product:
            return None
        
        # Convert to detail schema
        product_detail = ProductDetail.model_validate(product)
        
        # Cache the result
        await cache_service.set(
            cache_key,
            product_detail.model_dump(mode='json'),
            ttl=settings.CACHE_TTL_DETAIL
        )
        
        return product_detail
    
    async def get_stats(self) -> ProductStats:
        """Get aggregate statistics."""
        
        # Try cache first
        cache_key = "products:stats"
        cached = await cache_service.get(cache_key)
        if cached:
            return ProductStats(**cached)
        
        # Query for stats
        stats_query = select(
            func.count(Product.id).label("total_products"),
            func.count(distinct(Product.category)).label("total_categories"),
            func.count(distinct(Product.brand)).label("total_brands"),
            func.min(Product.price).label("price_min"),
            func.max(Product.price).label("price_max"),
            func.avg(Product.rating).label("avg_rating"),
            func.sum(Product.stock_quantity).label("total_stock"),
        )
        
        result = await self.db.execute(stats_query)
        row = result.one()
        
        stats = ProductStats(
            total_products=row.total_products,
            total_categories=row.total_categories,
            total_brands=row.total_brands,
            price_min=row.price_min or Decimal(0),
            price_max=row.price_max or Decimal(0),
            avg_rating=row.avg_rating or Decimal(0),
            total_stock=row.total_stock or 0,
        )
        
        # Cache the stats
        await cache_service.set(
            cache_key,
            stats.model_dump(mode='json'),
            ttl=settings.CACHE_TTL_STATS
        )
        
        return stats
    
    async def get_categories(self) -> CategoryList:
        """Get list of unique categories."""
        
        # Try cache first
        cache_key = "products:categories"
        cached = await cache_service.get(cache_key)
        if cached:
            return CategoryList(**cached)
        
        # Query for unique categories
        query = select(distinct(Product.category)).order_by(Product.category)
        result = await self.db.execute(query)
        categories = [row[0] for row in result.all()]
        
        category_list = CategoryList(
            categories=categories,
            total=len(categories)
        )
        
        # Cache the categories
        await cache_service.set(
            cache_key,
            category_list.model_dump(mode='json'),
            ttl=settings.CACHE_TTL_CATEGORIES
        )
        
        return category_list
    
    async def get_brands(self) -> dict:
        """Get list of unique brands."""
        
        # Try cache first
        cache_key = "products:brands"
        cached = await cache_service.get(cache_key)
        if cached:
            return cached
        
        # Query for unique brands
        query = select(distinct(Product.brand)).order_by(Product.brand)
        result = await self.db.execute(query)
        brands = [row[0] for row in result.all()]
        
        brand_list = {
            "brands": brands,
            "total": len(brands)
        }
        
        # Cache the brands
        await cache_service.set(
            cache_key,
            brand_list,
            ttl=settings.CACHE_TTL_CATEGORIES
        )
        
        return brand_list
