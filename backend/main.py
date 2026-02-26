from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import categories, products
from backend.database import engine, Base

# Create tables on startup (simple approach, alternative to alembic for dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Walk n Style API")

# CORS
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories.router)
app.include_router(products.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Walk n Style API"}
