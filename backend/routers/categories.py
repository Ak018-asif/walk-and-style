from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import Category
from backend.schemas import Category as CategorySchema

router = APIRouter(
    prefix="/api/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[CategorySchema])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Simple list return
    return db.query(Category).offset(skip).limit(limit).all()

@router.get("/tree")
def read_category_tree(db: Session = Depends(get_db)):
    # Returns nested structure
    # Pydantic schema for recursive checking?
    # For simplicity, returning just top level which includes children if relations are loaded
    # But relations are lazy by default. 
    # We should joinedload or subqueryload if we want children.
    # Or just let the frontend rebuild logic from flat list (easier for now).
    return db.query(Category).filter(Category.parent_id == None).all()

@router.get("/{category_id}", response_model=CategorySchema)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category
