from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.auth_router import router as auth_router
from routers.user_router import router as user_router
from routers.product_router import router as product_router
from routers.order_router import router as order_router

# modular routers
from app.modules.brands import router as brands_router
from app.modules.products import router as products_router
from app.modules.variants import router as variants_router
from app.modules.images import router as images_router
from app.modules.users import router as users_router
from app.modules.orders import router as orders_router
from app.modules.inventory import inventory_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    print("🚀 Walk n Style API starting...")
    yield
    print("🛑 Walk n Style API shutting down...")


app = FastAPI(
    title="Walk n Style API",
    description="Shoe E-Commerce REST API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
PREFIX = "/api/v1"
app.include_router(auth_router, prefix=PREFIX)
app.include_router(user_router, prefix=PREFIX)
app.include_router(product_router, prefix=PREFIX)
app.include_router(order_router, prefix=PREFIX)

# include modular routers as well (they may replicate functionality)
app.include_router(brands_router, prefix=PREFIX)
app.include_router(products_router, prefix=PREFIX)
app.include_router(variants_router, prefix=PREFIX)
app.include_router(images_router, prefix=PREFIX)
app.include_router(users_router, prefix=PREFIX)
app.include_router(orders_router, prefix=PREFIX)
app.include_router(inventory_router, prefix=PREFIX)


# Health Check Routes
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint."""
    return {
        "status": "ok",
        "app": "Walk n Style API",
        "version": "1.0.0",
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
