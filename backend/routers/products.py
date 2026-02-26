from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.database import get_db
from backend.models import Product, Category
from backend.schemas import Product as ProductSchema

router = APIRouter(
    prefix="/api/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[ProductSchema])
def read_products(
    skip: int = 0, 
    limit: int = 100, 
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if category_id:
        # Get all subcategory IDs
        # To do this efficiently we need a recursive query or helper
        # Using a simplified approach: just get direct matches for now to avoid complexity in this step
        # Or better: fetch all categories and filter in python (small dataset)
        
        # Helper to get all descendant IDs
        def get_all_children(cat_id):
            children = db.query(Category).filter(Category.parent_id == cat_id).all()
            ids = [cat_id]
            for child in children:
                ids.extend(get_all_children(child.id))
            return ids
            
        cat_ids = get_all_children(category_id)
        query = query.filter(Product.category_id.in_(cat_ids))

    if min_price is not None:
        query = query.filter(Product.base_price >= min_price)
    if max_price is not None:
        query = query.filter(Product.base_price <= max_price)

    return query.offset(skip).limit(limit).all()


@router.get("/{product_id}", response_model=ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
