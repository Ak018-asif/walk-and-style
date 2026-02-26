from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine, Base
from backend.models import Category, Product, ProductVariant, ProductImage
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    Base.metadata.create_all(bind=engine)

def seed_categories(db: Session):
    # Check if data exists
    if db.query(Category).first():
        logger.info("Categories already exist. Skipping seed.")
        return

    # Taxonomy
    taxonomy = {
        "Men": ["Shoes", "Sandals", "Hawais", "Perfumes", "Belts"],
        "Women": ["Shoes", "Sandals", "Perfumes", "Casual (v-shape)"],
        "Kids": ["Boys & Girls", "Shoes (casual)", "Sandals", "Hawai and crocs"],
        "Accessories": ["Bags", "Extras"]
    }
    
    # Sub-sub categories map
    sub_taxonomy = {
        "Shoes": ["Formal", "Casual"], # For Men
        "Belts": ["Autolock", "Casual belt"], # For Men
        "Bags": ["Gym bags", "School and college bags", "Tourister bags"],
        "Extras": ["Shoe polish and socks"]
    }

    # Helper to create category
    def create_cat(name, parent_id=None):
        cat = Category(name=name, parent_id=parent_id)
        db.add(cat)
        db.commit()
        db.refresh(cat)
        return cat

    for main_cat, subs in taxonomy.items():
        parent = create_cat(main_cat)
        for sub in subs:
            child = create_cat(sub, parent.id)
            
            # Check for sub-sub categories logic (simplified matching)
            # "Shoes" appears in Men, Women, Kids. 
            # The prompt specific hierarchy:
            # Men -> Shoes -> (Formal, Casual)
            # Accessories -> Bags -> (...)
            # Accessories -> Extras -> (...)
            
            if main_cat == "Men" and sub == "Shoes":
                 create_cat("Formal", child.id)
                 create_cat("Casual", child.id)
            elif main_cat == "Men" and sub == "Belts":
                 create_cat("Autolock", child.id)
                 create_cat("Casual belt", child.id)
            elif main_cat == "Accessories" and sub == "Bags":
                 create_cat("Gym bags", child.id)
                 create_cat("School and college bags", child.id)
                 create_cat("Tourister bags", child.id)
            elif main_cat == "Accessories" and sub == "Extras":
                 create_cat("Shoe polish and socks", child.id)

    logger.info("Categories seeded.")

def seed_products(db: Session):
    if db.query(Product).first():
        logger.info("Products already exist. Skipping seed.")
        return

    # Helper to find category by name (and potentially parent)
    def get_cat_id(name, parent_name=None):
        # This is a simple lookup, might collide if names are not unique globally
        # But for seed it's fine
        cat = db.query(Category).filter(Category.name == name).first()
        return cat.id if cat else None

    # We need specific IDs we just created. 
    # Let's fetch some IDs for sample products.
    men_casual_shoes = db.query(Category).filter(Category.name == "Casual").first() # Men->Shoes->Casual
    women_sandals = db.query(Category).filter(Category.name == "Sandals", Category.parent.has(name="Women")).first()
    
    if not men_casual_shoes or not women_sandals:
        logger.warning("Could not find categories for products. Skipping product seed.")
        return

    # Product 1
    p1 = Product(
        category_id=men_casual_shoes.id,
        name="Urban Trekker Sneakers",
        description="Lightweight and breathable casual sneakers perfect for daily wear.",
        base_price=2499.00
    )
    db.add(p1)
    db.commit()
    db.refresh(p1)

    db.add(ProductVariant(product_id=p1.id, size="40", color="Red/White", sku="UTS-RD-40", stock_quantity=10))
    db.add(ProductVariant(product_id=p1.id, size="41", color="Black/White", sku="UTS-BK-41", stock_quantity=8))
    
    db.add(ProductImage(product_id=p1.id, image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&q=80&w=1000", is_primary=True))
    db.add(ProductImage(product_id=p1.id, image_url="https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?auto=format&fit=crop&q=80&w=1000", is_primary=False))

    # Product 2
    p2 = Product(
        category_id=women_sandals.id,
        name="Summer Breeze Strappy Sandals",
        description="Chic and comfortable strappy sandals.",
        base_price=1299.00
    )
    db.add(p2)
    db.commit()
    db.refresh(p2)

    db.add(ProductVariant(product_id=p2.id, size="36", color="Gold", sku="SBS-GD-36", stock_quantity=20))
    db.add(ProductImage(product_id=p2.id, image_url="https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&q=80&w=1000", is_primary=True))

    db.commit()
    logger.info("Products seeded.")

def main():
    init_db()
    db = SessionLocal()
    try:
        seed_categories(db)
        seed_products(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
