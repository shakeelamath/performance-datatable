"""Quick test script to verify backend endpoints."""
import asyncio
import time
import httpx


BASE_URL = "http://localhost:8000"


async def test_endpoints():
    """Test all backend endpoints."""
    async with httpx.AsyncClient() as client:
        print("🧪 Testing Backend Endpoints\n")
        print("=" * 60)
        
        # Test 1: Health Check
        print("\n1️⃣  Testing Health Check...")
        start = time.time()
        response = await client.get(f"{BASE_URL}/health")
        elapsed = (time.time() - start) * 1000
        print(f"   Status: {response.status_code}")
        print(f"   Response time: {elapsed:.2f}ms")
        print(f"   Response: {response.json()}")
        
        # Test 2: Root Endpoint
        print("\n2️⃣  Testing Root Endpoint...")
        start = time.time()
        response = await client.get(f"{BASE_URL}/")
        elapsed = (time.time() - start) * 1000
        print(f"   Status: {response.status_code}")
        print(f"   Response time: {elapsed:.2f}ms")
        
        # Test 3: List Products (first page)
        print("\n3️⃣  Testing Product List (page 1)...")
        start = time.time()
        response = await client.get(f"{BASE_URL}/api/v1/products?limit=50")
        elapsed = (time.time() - start) * 1000
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Response time: {elapsed:.2f}ms")
        print(f"   Total products: {data.get('total', 0)}")
        print(f"   Products returned: {len(data.get('data', []))}")
        print(f"   Total pages: {data.get('pages', 0)}")
        
        if elapsed < 100:
            print(f"   ✅ Performance target met (< 100ms)")
        else:
            print(f"   ⚠️  Performance target missed (> 100ms)")
        
        # Test 4: List Products with Filters
        print("\n4️⃣  Testing Product List with Filters...")
        start = time.time()
        response = await client.get(
            f"{BASE_URL}/api/v1/products",
            params={"category": "Electronics", "limit": 20, "sort_by": "price", "sort_order": "desc"}
        )
        elapsed = (time.time() - start) * 1000
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Response time: {elapsed:.2f}ms")
        print(f"   Filtered results: {len(data.get('data', []))}")
        
        if elapsed < 100:
            print(f"   ✅ Performance target met (< 100ms)")
        else:
            print(f"   ⚠️  Performance target missed (> 100ms)")
        
        # Test 5: Get Product Details
        print("\n5️⃣  Testing Product Detail...")
        start = time.time()
        response = await client.get(f"{BASE_URL}/api/v1/products/1")
        elapsed = (time.time() - start) * 1000
        print(f"   Status: {response.status_code}")
        print(f"   Response time: {elapsed:.2f}ms")
        if response.status_code == 200:
            product = response.json()
            print(f"   Product: {product.get('name', 'N/A')}")
            print(f"   Price: ${product.get('price', 0)}")
            print(f"   Category: {product.get('category', 'N/A')}")
        
        # Test 6: Get Stats
        print("\n6️⃣  Testing Statistics Endpoint...")
        start = time.time()
        response = await client.get(f"{BASE_URL}/api/v1/products/stats")
        elapsed = (time.time() - start) * 1000
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Response time: {elapsed:.2f}ms")
        print(f"   Total products: {data.get('total_products', 0)}")
        print(f"   Total categories: {data.get('total_categories', 0)}")
        print(f"   Total brands: {data.get('total_brands', 0)}")
        print(f"   Price range: ${data.get('price_min', 0)} - ${data.get('price_max', 0)}")
        print(f"   Avg rating: {data.get('avg_rating', 0)}")
        
        # Test 7: Get Categories
        print("\n7️⃣  Testing Categories Endpoint...")
        start = time.time()
        response = await client.get(f"{BASE_URL}/api/v1/products/categories")
        elapsed = (time.time() - start) * 1000
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Response time: {elapsed:.2f}ms")
        print(f"   Categories: {data.get('total', 0)}")
        print(f"   List: {', '.join(data.get('categories', [])[:5])}...")
        
        # Test 8: Get Brands
        print("\n8️⃣  Testing Brands Endpoint...")
        start = time.time()
        response = await client.get(f"{BASE_URL}/api/v1/products/brands")
        elapsed = (time.time() - start) * 1000
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Response time: {elapsed:.2f}ms")
        print(f"   Brands: {data.get('total', 0)}")
        
        # Test 9: Search Products
        print("\n9️⃣  Testing Search...")
        start = time.time()
        response = await client.get(
            f"{BASE_URL}/api/v1/products",
            params={"search": "Tech", "limit": 10}
        )
        elapsed = (time.time() - start) * 1000
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Response time: {elapsed:.2f}ms")
        print(f"   Search results: {len(data.get('data', []))}")
        
        # Test 10: Cached Request (should be faster)
        print("\n🔟 Testing Cached Request (same as test 3)...")
        start = time.time()
        response = await client.get(f"{BASE_URL}/api/v1/products?limit=50")
        elapsed = (time.time() - start) * 1000
        print(f"   Status: {response.status_code}")
        print(f"   Response time: {elapsed:.2f}ms (should be faster)")
        
        if elapsed < 50:
            print(f"   ✅ Cache working! Response < 50ms")
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!\n")


if __name__ == "__main__":
    print("\n🚀 Backend API Test Suite")
    print("Make sure the backend is running on http://localhost:8000\n")
    
    try:
        asyncio.run(test_endpoints())
    except httpx.ConnectError:
        print("\n❌ Error: Could not connect to backend.")
        print("   Make sure the server is running:")
        print("   - docker-compose up")
        print("   - OR: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")
