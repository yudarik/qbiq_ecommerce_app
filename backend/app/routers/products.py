from typing import Literal

from fastapi import APIRouter, HTTPException, Query

from app.models.product import Product, ProductListResponse
from app.services import product_service

router = APIRouter(prefix="/api", tags=["products"])


@router.get("/products", response_model=ProductListResponse)
def get_products(
    name: str | None = Query(default=None),
    category: str | None = Query(default=None),
    sort_by: Literal["price", "name"] | None = Query(default=None),
    sort_order: Literal["asc", "desc"] = Query(default="asc"),
):
    return product_service.list_products(
        name=name, category=category, sort_by=sort_by, sort_order=sort_order
    )


@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: str):
    product = product_service.get_product_by_id(product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/categories", response_model=list[str])
def get_categories():
    return product_service.list_categories()
