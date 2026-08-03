from fastapi import APIRouter, HTTPException
from fastapi.params import Header

from app.models.cart import AddToCartRequest, Cart, UpdateCartItemRequest
from app.services import cart_service

router = APIRouter(prefix="/api/cart", tags=["cart"])


def _resolve_cart_id(x_cart_id: str | None) -> str:
    return x_cart_id if x_cart_id else cart_service.new_cart_id()


@router.get("", response_model=Cart)
def get_cart(x_cart_id: str | None = Header(default=None)):
    cart_id = _resolve_cart_id(x_cart_id)
    return cart_service.get_cart(cart_id)


@router.post("/items", response_model=Cart)
def add_item(body: AddToCartRequest, x_cart_id: str | None = Header(default=None)):
    cart_id = _resolve_cart_id(x_cart_id)
    try:
        return cart_service.add_item(cart_id, body.product_id, body.quantity)
    except KeyError:
        raise HTTPException(status_code=404, detail="Product not found")


@router.put("/items/{product_id}", response_model=Cart)
def update_item(
    product_id: str,
    body: UpdateCartItemRequest,
    x_cart_id: str | None = Header(default=None),
):
    cart_id = _resolve_cart_id(x_cart_id)
    try:
        return cart_service.update_item(cart_id, product_id, body.quantity)
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not in cart")


@router.delete("/items/{product_id}", response_model=Cart)
def remove_item(product_id: str, x_cart_id: str | None = Header(default=None)):
    cart_id = _resolve_cart_id(x_cart_id)
    return cart_service.remove_item(cart_id, product_id)
