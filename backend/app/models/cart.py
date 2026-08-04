from pydantic import Field

from app.models.common import CamelModel


class CartItem(CamelModel):
    product_id: str
    quantity: int = Field(ge=1)
    name: str
    price: float
    thumbnail_url: str
    line_total: float


class Cart(CamelModel):
    cart_id: str
    items: list[CartItem]
    total: float


class AddToCartRequest(CamelModel):
    product_id: str
    quantity: int = Field(default=1, ge=1)


class UpdateCartItemRequest(CamelModel):
    quantity: int = Field(ge=1)
