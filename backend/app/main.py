from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import cart, products

app = FastAPI(title="qbiq eCommerce API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Cart-Id"],
)

app.include_router(products.router)
app.include_router(cart.router)


@app.get("/health")
def health():
    return {"status": "ok"}
