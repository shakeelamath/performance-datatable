# Setup & Deployment Guide

Complete guide to running the High-Performance Data Table application.

## 🚀 Quick Start (Docker - Recommended)

The easiest way to run the entire application:

```bash
# Clone the repository
git clone <your-repo-url>
cd MiniProject

# Start all services with one command
docker-compose up --build

# Wait for services to start and database to seed (~2-3 minutes)
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

That's it! The application will:
1. Start PostgreSQL database
2. Start Redis cache
3. Build and start the backend API
4. Seed 100,000 products into the database
5. Build and start the frontend

## 📋 Prerequisites

### For Docker (Recommended)
- Docker Desktop 4.0+
- Docker Compose 2.0+
- 4GB RAM minimum
- 10GB free disk space

### For Manual Setup
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- npm or yarn

## 🐳 Docker Setup (Detailed)

### First Time Setup

```bash
# Navigate to project directory
cd MiniProject

# Build all services
docker-compose build

# Start services in detached mode
docker-compose up -d

# Watch logs
docker-compose logs -f
```

### Managing Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v

# Restart a specific service
docker-compose restart backend
docker-compose restart frontend

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Execute commands in containers
docker-compose exec backend python -m app.utils.seed_data
docker-compose exec frontend npm run build
```

### Troubleshooting Docker

**Issue: Port already in use**
```bash
# Change ports in docker-compose.yml
# For backend: "8001:8000" instead of "8000:8000"
# For frontend: "3001:3000" instead of "3000:3000"
```

**Issue: Build fails**
```bash
# Clear Docker cache and rebuild
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
docker-compose up
```

**Issue: Database seed fails**
```bash
# Manually seed after startup
docker-compose exec backend python -m app.utils.seed_data
```

## 💻 Manual Setup

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your database credentials
# DATABASE_URL=postgresql+asyncpg://admin:password@localhost:5432/products_db
# REDIS_URL=redis://localhost:6379

# Start PostgreSQL and Redis (separate terminals or services)

# Seed the database
python -m app.utils.seed_data

# Run the backend
uvicorn app.main:app --reload
```

Backend will be available at http://localhost:8000

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install

# Create .env.local file
cp .env.example .env.local

# Edit .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Run development server
npm run dev
# or
yarn dev
```

Frontend will be available at http://localhost:3000

## 🧪 Testing the Application

### Backend Tests

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Run API tests
python test_api.py

# Test specific endpoint
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/products?limit=10
```

### Frontend Tests

Open browser and test:
1. Navigate to http://localhost:3000
2. Search for products
3. Apply filters (category, brand, price)
4. Sort columns
5. Navigate pages
6. Click "View" to see product details
7. Test responsiveness (resize browser)

### Performance Tests

```bash
# Check API response times
curl -w "@curl-format.txt" http://localhost:8000/api/v1/products

# Create curl-format.txt:
echo "time_total: %{time_total}s\n" > curl-format.txt
```

Expected response times:
- First request (cold): 50-100ms
- Cached requests: 10-50ms

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://admin:password@localhost:5432/products_db

# Redis
REDIS_URL=redis://localhost:6379

# API Settings
API_V1_PREFIX=/api/v1
DEBUG=False

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Cache TTL (seconds)
CACHE_TTL_LIST=120
CACHE_TTL_DETAIL=900
CACHE_TTL_STATS=300
CACHE_TTL_CATEGORIES=3600
```

### Frontend Configuration

Edit `frontend/.env.local`:

```bash
# API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🌐 Production Deployment

### Build Production Images

```bash
# Build optimized images
docker-compose -f docker-compose.prod.yml build

# Start production services
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables for Production

```bash
# Backend
DATABASE_URL=postgresql+asyncpg://user:pass@db-host:5432/products_db
REDIS_URL=redis://redis-host:6379
DEBUG=False
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### Nginx Reverse Proxy (Optional)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Monitoring

### Check Service Health

```bash
# Backend health
curl http://localhost:8000/health

# Database connection
docker-compose exec postgres pg_isready

# Redis connection
docker-compose exec redis redis-cli ping
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Performance Monitoring

```bash
# Check container stats
docker stats

# Backend metrics
curl http://localhost:8000/api/v1/products/stats

# Check response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/v1/products
```

## 🗄️ Database Management

### Backup Database

```bash
# Export database
docker-compose exec postgres pg_dump -U admin products_db > backup.sql

# With Docker
docker exec products_db pg_dump -U admin products_db > backup.sql
```

### Restore Database

```bash
# Import database
docker-compose exec -T postgres psql -U admin products_db < backup.sql
```

### Reset Database

```bash
# Stop services
docker-compose down

# Remove volumes
docker volume rm products_postgres_data

# Start fresh
docker-compose up -d
```

## 🔍 Common Issues & Solutions

### Issue: "Connection refused" to database

**Solution:**
```bash
# Check if PostgreSQL is running
docker-compose ps

# Check PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Issue: "Redis connection error"

**Solution:**
```bash
# Check if Redis is running
docker-compose ps

# Test Redis connection
docker-compose exec redis redis-cli ping

# Restart Redis
docker-compose restart redis
```

### Issue: "Module not found" in frontend

**Solution:**
```bash
cd frontend

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# or with Docker
docker-compose down
docker-compose build --no-cache frontend
docker-compose up
```

### Issue: Slow performance

**Solution:**
```bash
# Check Docker resources (Docker Desktop > Settings > Resources)
# Allocate at least 4GB RAM

# Check Redis cache
docker-compose exec redis redis-cli INFO stats

# Check database indexes
docker-compose exec postgres psql -U admin products_db -c "\d products"

# Rebuild and restart
docker-compose down
docker-compose up --build
```

## 📞 Support

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Verify all services are running: `docker-compose ps`
3. Check environment variables in `.env` files
4. Review the troubleshooting sections above
5. Check the individual README files in `backend/` and `frontend/`

## 🎓 Development Workflow

### Making Changes

```bash
# Backend changes
cd backend
# Edit files
# Backend auto-reloads with uvicorn --reload

# Frontend changes
cd frontend
# Edit files
# Frontend auto-reloads with Next.js dev server

# With Docker
docker-compose up --build
# Or rebuild specific service
docker-compose up --build backend
```

### Adding Dependencies

```bash
# Backend
cd backend
pip install <package>
pip freeze > requirements.txt
docker-compose build backend

# Frontend
cd frontend
npm install <package>
docker-compose build frontend
```

## 🚀 Ready to Go!

Your high-performance data table application is now ready to handle 100,000+ records with blazing-fast performance!

For more details:
- Backend docs: `backend/README.md`
- Frontend docs: `frontend/README.md`
- Implementation plan: `IMPLEMENTATION_PLAN.md`
