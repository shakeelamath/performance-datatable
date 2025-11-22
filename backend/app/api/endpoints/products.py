"""Product API endpoints."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_product_service
from app.services.product_service import ProductService
from app.schemas.product import ProductList, ProductDetail, ProductStats, CategoryList


router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=ProductList)
async def list_products(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("id", description="Sort by field"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order"),
    category: Optional[str] = Query(None, description="Filter by category"),
    brand: Optional[str] = Query(None, description="Filter by brand"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    search: Optional[str] = Query(None, description="Search in name, description, SKU"),
    product_service: ProductService = Depends(get_product_service),
):
    """
    Get paginated list of products with filtering and sorting.
    
    - **page**: Page number (default: 1)
    - **limit**: Items per page (default: 50, max: 100)
    - **sort_by**: Field to sort by (default: id)
    - **sort_order**: Sort order asc/desc (default: asc)
    - **category**: Filter by category
    - **brand**: Filter by brand
    - **min_price**: Minimum price filter
    - **max_price**: Maximum price filter
    - **search**: Search term for name/description/SKU
    """
    return await product_service.get_products(
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        category=category,
        brand=brand,
        min_price=min_price,
        max_price=max_price,
        search=search,
    )


@router.get("/stats", response_model=ProductStats)
async def get_stats(
    product_service: ProductService = Depends(get_product_service),
):
    """
    Get aggregate statistics about products.
    
    Returns total counts, price ranges, and averages.
    """
    return await product_service.get_stats()


@router.get("/categories", response_model=CategoryList)
async def get_categories(
    product_service: ProductService = Depends(get_product_service),
):
    """
    Get list of unique product categories.
    
    Useful for populating filter dropdowns.
    """
    return await product_service.get_categories()


@router.get("/brands")
async def get_brands(
    product_service: ProductService = Depends(get_product_service),
):
    """
    Get list of unique product brands.
    
    Useful for populating filter dropdowns.
    """
    return await product_service.get_brands()


@router.get("/{product_id}", response_model=ProductDetail)
async def get_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
):
    """
    Get detailed information about a specific product.
    
    - **product_id**: Product ID
    """
    product = await product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
