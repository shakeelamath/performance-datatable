# Backend API - High-Performance Data Table

FastAPI backend with 100,000+ records, PostgreSQL, and Redis caching.

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Local Development

1. **Create virtual environment:**
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your database and Redis URLs
```

4. **Initialize and seed database:**
```bash
# Start PostgreSQL and Redis
# Then run:
python -m app.utils.seed_data
```

5. **Run the server:**
```bash
uvicorn app.main:app --reload
```

The API will be available at: http://localhost:8000

## API Documentation

Interactive API documentation: http://localhost:8000/docs

### Endpoints

#### `GET /api/v1/products`
Get paginated list of products with filtering and sorting.

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `limit` (int): Items per page (default: 50, max: 100)
- `sort_by` (str): Field to sort by (default: "id")
- `sort_order` (str): "asc" or "desc" (default: "asc")
- `category` (str): Filter by category
- `brand` (str): Filter by brand
- `min_price` (float): Minimum price
- `max_price` (float): Maximum price
- `search` (str): Search in name/description/SKU

**Response:**
```json
{
  "data": [...],
  "total": 100000,
  "page": 1,
  "limit": 50,
  "pages": 2000
}
```

#### `GET /api/v1/products/{id}`
Get detailed product information.

#### `GET /api/v1/products/stats`
Get aggregate statistics (counts, price ranges, averages).

#### `GET /api/v1/products/categories`
Get list of unique categories.

#### `GET /api/v1/products/brands`
Get list of unique brands.

#### `GET /health`
Health check endpoint.

## Performance Optimizations

### Database
- **Indexes:** Composite indexes on commonly filtered columns (category+price, brand+price)
- **Async Queries:** Using asyncpg for non-blocking database operations
- **Connection Pooling:** Configured with pool_size=10, max_overflow=20
- **Selective Columns:** Queries only necessary columns

### Caching
- **Redis Layer:** Caches API responses with appropriate TTLs
- **Cache Keys:** Hashed query parameters for unique cache entries
- **TTL Strategy:**
  - Product lists: 2 minutes
  - Product details: 15 minutes
  - Stats: 5 minutes
  - Categories/Brands: 1 hour

### API
- **Response Time Header:** Every response includes `X-Process-Time` header
- **Pagination:** Efficient offset-based pagination
- **Compression:** Gzip middleware for response compression
- **CORS:** Configured for frontend access

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings
│   ├── database.py          # Database connection
│   ├── models/
│   │   └── product.py       # SQLAlchemy models
│   ├── schemas/
│   │   └── product.py       # Pydantic schemas
│   ├── api/
│   │   ├── dependencies.py  # DI
│   │   └── endpoints/
│   │       └── products.py  # API routes
│   ├── services/
│   │   ├── cache.py         # Redis caching
│   │   └── product_service.py
│   └── utils/
│       └── seed_data.py     # Data seeding
├── Dockerfile
├── requirements.txt
└── .env
```

## Testing

Run a quick performance test:
```bash
# Install httpie or curl
pip install httpie

# Test basic endpoint
http GET http://localhost:8000/api/v1/products

# Test with filters
http GET http://localhost:8000/api/v1/products category=="Electronics" limit==100

# Check response time (should be < 100ms)
# Look for X-Process-Time header
```

## Docker

Build and run with Docker:
```bash
docker build -t backend-api .
docker run -p 8000:8000 --env-file .env backend-api
```

## Notes

- First request may be slower (cache warming)
- Subsequent requests should be < 50ms with cache hits
- Database queries optimized to < 30ms
- All timestamps in UTC
