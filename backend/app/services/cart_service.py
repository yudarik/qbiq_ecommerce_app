import uuid

from app.data.loader import PRODUCTS_BY_ID

# cart_id -> {product_id: quantity}. In-memory only; resets on restart.
_carts: dict[str, dict[str, int]] = {}


def new_cart_id() -> str:
    return str(uuid.uuid4())


def _serialize(cart_id: str) -> dict:
    quantities = _carts.get(cart_id, {})
    items = []
    total = 0.0
    for product_id, quantity in quantities.items():
        product = PRODUCTS_BY_ID.get(product_id)
        if product is None:
            continue
        line_total = round(product["price"] * quantity, 2)
        total += line_total
        items.append(
            {
                "productId": product_id,
                "quantity": quantity,
                "name": product["name"],
                "price": product["price"],
                "thumbnailUrl": product["thumbnailUrl"],
                "lineTotal": line_total,
            }
        )
    return {"cartId": cart_id, "items": items, "total": round(total, 2)}


def get_cart(cart_id: str) -> dict:
    _carts.setdefault(cart_id, {})
    return _serialize(cart_id)


def add_item(cart_id: str, product_id: str, quantity: int) -> dict:
    if product_id not in PRODUCTS_BY_ID:
        raise KeyError(product_id)
    quantities = _carts.setdefault(cart_id, {})
    quantities[product_id] = quantities.get(product_id, 0) + quantity
    return _serialize(cart_id)


def update_item(cart_id: str, product_id: str, quantity: int) -> dict:
    quantities = _carts.setdefault(cart_id, {})
    if product_id not in quantities:
        raise KeyError(product_id)
    quantities[product_id] = quantity
    return _serialize(cart_id)


def remove_item(cart_id: str, product_id: str) -> dict:
    quantities = _carts.setdefault(cart_id, {})
    quantities.pop(product_id, None)
    return _serialize(cart_id)
