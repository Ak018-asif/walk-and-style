"""
Walk n Style API - Main Entry Point
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.auth.controller import router as auth_router
from app.modules.users.controller import router as users_router
from app.modules.categories.controller import router as categories_router
from app.modules.brands.controller import router as brands_router
from app.modules.products.controller import router as products_router
from app.modules.variants.controller import router as variants_router
from app.modules.images.controller import router as images_router
from app.modules.orders.controller import router as orders_router
from app.modules.payments.controller import router as payments_router
from app.modules.inventory.controller import router as inventory_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Walk n Style API starting...")
    yield
    # Shutdown
    print("🛑 Walk n Style API shutting down...")


app = FastAPI(
    title="Walk n Style API",
    description="Shoe E-Commerce REST API — Modular Architecture",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")
app.include_router(brands_router, prefix="/api/v1")
app.include_router(products_router, prefix="/api/v1")
app.include_router(variants_router, prefix="/api/v1")
app.include_router(images_router, prefix="/api/v1")
app.include_router(orders_router, prefix="/api/v1")
app.include_router(payments_router, prefix="/api/v1")
app.include_router(inventory_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "status": "ok",
        "app": "Walk n Style API",
        "version": "1.0.0",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
