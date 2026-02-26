from sqlalchemy.orm import Session
from backend.models import Category

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_tree(db: Session):
    # Fetch all and build tree in memory execution for simplicity, 
    # or just return flat list and let frontend build tree.
    # For now, return top level with loaded children relationship if we configured it correctly.
    # In models.py we have `children` relationship via backref.
    return db.query(Category).filter(Category.parent_id == None).all()
