from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.models import Product, Category
from typing import List, Optional

def get_products(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    query = db.query(Product)

    if category_id:
        # Include subcategories
        # 1. Fetch all categories
        # 2. Find children of category_id recursively
        # This is expensive in python, but better than recursive SQL queries for simple app
        # Ideally using CTEs in SQL.
        # For now, let's just do exact match OR simple 1-level child match if needed.
        # Or just fetch all Category IDs that are children.
        
        # Simplified: Get all categories, build list of IDs
        all_cats = db.query(Category).all()
        
        def get_children_ids(parent_id):
            ids = [parent_id]
            for c in all_cats:
                if c.parent_id == parent_id:
                    ids.extend(get_children_ids(c.id))
            return ids
            
        cat_ids = get_children_ids(category_id)
        query = query.filter(Product.category_id.in_(cat_ids))

    if min_price is not None:
        query = query.filter(Product.base_price >= min_price)
    
    if max_price is not None:
        query = query.filter(Product.base_price <= max_price)

    return query.offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()
