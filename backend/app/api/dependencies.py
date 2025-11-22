"""API dependencies."""
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.product_service import ProductService


async def get_product_service(
    db: AsyncSession = Depends(get_db)
) -> AsyncGenerator[ProductService, None]:
    """Dependency for getting product service."""
    yield ProductService(db)
