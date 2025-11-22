"""Database seeding script to generate realistic product data."""
import asyncio
import random
from datetime import datetime, timedelta
from typing import List

from faker import Faker
from sqlalchemy import select, func

from ..database import AsyncSessionLocal, engine
from ..models.product import Product, Base

fake = Faker()

# Product categories and their related data
CATEGORIES = {
    "Electronics": ["Samsung", "Apple", "Sony", "LG", "Dell", "HP", "Lenovo", "Asus"],
    "Clothing": ["Nike", "Adidas", "Zara", "H&M", "Uniqlo", "Levi's", "Gap", "Puma"],
    "Home & Garden": ["IKEA", "Home Depot", "Wayfair", "Target", "Walmart", "Lowes"],
    "Books": ["Penguin", "HarperCollins", "Simon & Schuster", "Hachette", "Macmillan"],
    "Sports": ["Nike", "Adidas", "Under Armour", "Puma", "Reebok", "New Balance"],
    "Toys": ["LEGO", "Mattel", "Hasbro", "Fisher-Price", "Nerf", "Hot Wheels"],
    "Beauty": ["L'Oréal", "Maybelline", "Neutrogena", "Dove", "Nivea", "Clinique"],
    "Food": ["Nestlé", "Kraft", "General Mills", "Kellogg's", "Campbell's", "Heinz"],
}

# Status options
STATUSES = ["active", "inactive", "out_of_stock", "discontinued"]


def generate_product_name(category: str) -> str:
    """Generate realistic product names based on category."""
    adjectives = ["Premium", "Professional", "Advanced", "Classic", "Modern", "Ultimate", "Deluxe", "Essential"]
    
    templates = {
        "Electronics": [
            f"{random.choice(adjectives)} {fake.word().title()} {random.choice(['Pro', 'Plus', 'Max', 'Air', 'Ultra'])}",
            f"{fake.word().title()} {random.choice(['Wireless', 'Smart', 'Digital', '4K', 'HD'])} {random.choice(['Device', 'Gadget', 'System'])}",
        ],
        "Clothing": [
            f"{random.choice(adjectives)} {random.choice(['Cotton', 'Denim', 'Leather', 'Wool'])} {random.choice(['Shirt', 'Pants', 'Jacket', 'Shoes', 'Dress'])}",
            f"{fake.word().title()} {random.choice(['Running', 'Casual', 'Formal', 'Sport'])} {random.choice(['Wear', 'Apparel', 'Outfit'])}",
        ],
        "Home & Garden": [
            f"{random.choice(adjectives)} {random.choice(['Wooden', 'Metal', 'Glass', 'Plastic'])} {random.choice(['Table', 'Chair', 'Lamp', 'Shelf', 'Cabinet'])}",
            f"{fake.word().title()} {random.choice(['Garden', 'Kitchen', 'Bedroom', 'Living Room'])} {random.choice(['Set', 'Collection', 'Essentials'])}",
        ],
        "Books": [
            f"The {fake.word().title()} {random.choice(['Journey', 'Adventure', 'Mystery', 'Story', 'Guide'])}",
            f"{random.choice(adjectives)} {random.choice(['Guide to', 'Handbook of', 'Introduction to'])} {fake.word().title()}",
        ],
        "Sports": [
            f"{random.choice(adjectives)} {random.choice(['Running', 'Training', 'Yoga', 'Fitness'])} {random.choice(['Shoes', 'Mat', 'Gear', 'Equipment'])}",
            f"{fake.word().title()} {random.choice(['Pro', 'Elite', 'Performance'])} {random.choice(['Ball', 'Racket', 'Kit'])}",
        ],
        "Toys": [
            f"{random.choice(adjectives)} {fake.word().title()} {random.choice(['Set', 'Collection', 'Kit', 'Pack'])}",
            f"{random.choice(['Building', 'Action', 'Educational', 'Creative'])} {fake.word().title()} Toy",
        ],
        "Beauty": [
            f"{random.choice(adjectives)} {random.choice(['Face', 'Skin', 'Hair', 'Body'])} {random.choice(['Cream', 'Serum', 'Lotion', 'Oil', 'Mask'])}",
            f"{fake.word().title()} {random.choice(['Hydrating', 'Moisturizing', 'Nourishing'])} {random.choice(['Formula', 'Treatment', 'Care'])}",
        ],
        "Food": [
            f"{random.choice(adjectives)} {fake.word().title()} {random.choice(['Snack', 'Cereal', 'Sauce', 'Mix'])}",
            f"{random.choice(['Organic', 'Natural', 'Gourmet'])} {fake.word().title()} {random.choice(['Pack', 'Box', 'Bundle'])}",
        ],
    }
    
    return random.choice(templates.get(category, [fake.word().title() + " Product"]))


def generate_description(category: str, name: str) -> str:
    """Generate realistic product descriptions."""
    features = [
        "high-quality materials",
        "durable construction",
        "ergonomic design",
        "easy to use",
        "eco-friendly",
        "great value",
        "trusted brand",
        "premium quality",
        "long-lasting",
        "innovative features",
    ]
    
    description = f"{name} is a must-have product in the {category} category. "
    description += f"Features include {', '.join(random.sample(features, 3))}. "
    description += fake.sentence()
    
    return description


async def create_products_batch(batch_size: int, offset: int) -> List[Product]:
    """Create a batch of product instances."""
    products = []
    
    for i in range(batch_size):
        category = random.choice(list(CATEGORIES.keys()))
        brand = random.choice(CATEGORIES[category])
        name = generate_product_name(category)
        
        product = Product(
            name=name,
            description=generate_description(category, name),
            price=round(random.uniform(9.99, 999.99), 2),
            category=category,
            brand=brand,
            stock_quantity=random.randint(0, 1000),
            rating=round(random.uniform(1.0, 5.0), 1),
            status=random.choices(
                STATUSES,
                weights=[70, 10, 15, 5],  # Weighted towards 'active'
                k=1
            )[0],
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 730)),
            updated_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
        )
        products.append(product)
    
    return products


async def seed_products(total_records: int = 100000, batch_size: int = 1000):
    """Seed the database with products."""
    async with AsyncSessionLocal() as session:
        # Check if products already exist
        result = await session.execute(select(func.count(Product.id)))
        existing_count = result.scalar()
        
        if existing_count >= total_records:
            print(f"Database already contains {existing_count} products.")
            print(f"Skipping seeding. To reseed, delete existing products first.")
            return
        
        if existing_count > 0:
            print(f"Database contains {existing_count} products.")
            remaining = total_records - existing_count
            print(f"Adding {remaining} more products to reach {total_records} total.")
            total_records = remaining
        
        print(f"Generating {total_records} products in batches of {batch_size}...")
        
        total_batches = (total_records + batch_size - 1) // batch_size
        
        for batch_num in range(total_batches):
            offset = batch_num * batch_size
            current_batch_size = min(batch_size, total_records - offset)
            
            products = await create_products_batch(current_batch_size, offset)
            session.add_all(products)
            await session.commit()
            
            progress = ((batch_num + 1) / total_batches) * 100
            print(f"Progress: {progress:.1f}% ({offset + current_batch_size}/{total_records} products)")
        
        print(f"\n✅ Successfully seeded {total_records} products!")
        
        # Display statistics
        result = await session.execute(
            select(
                func.count(Product.id).label("total"),
                func.count(func.distinct(Product.category)).label("categories"),
                func.count(func.distinct(Product.brand)).label("brands"),
                func.min(Product.price).label("min_price"),
                func.max(Product.price).label("max_price"),
                func.avg(Product.rating).label("avg_rating"),
            )
        )
        stats = result.first()
        
        print("\n📊 Database Statistics:")
        print(f"   Total Products: {stats.total:,}")
        print(f"   Categories: {stats.categories}")
        print(f"   Brands: {stats.brands}")
        print(f"   Price Range: ${stats.min_price:.2f} - ${stats.max_price:.2f}")
        print(f"   Average Rating: {stats.avg_rating:.2f}")


async def main():
    """Main function to run the seeder."""
    print("Starting database seeding with 100000 records...")
    
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed the database
    total_records = 100000
    await seed_products(total_records=total_records)
    
    print("\n🎉 Database seeding completed!")


if __name__ == "_main_":
    asyncio.run(main())