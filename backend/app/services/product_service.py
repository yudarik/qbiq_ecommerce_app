from app.cache.decorators import cache_ttl
from app.config import settings
from app.data.loader import PRODUCTS, PRODUCTS_BY_ID


def _matches(product: dict, name: str | None, category: str | None) -> bool:
    if name and name.lower() not in product["name"].lower():
        return False
    if category and product["category"] != category:
        return False
    return True


@cache_ttl(settings.cache_ttl_seconds, key_prefix="products:list")
def list_products(
    name: str | None = None,
    category: str | None = None,
    sort_by: str | None = None,
    sort_order: str = "asc",
) -> dict:
    items = [p for p in PRODUCTS if _matches(p, name, category)]

    if sort_by in ("price", "name"):
        items = sorted(items, key=lambda p: p[sort_by], reverse=sort_order == "desc")

    summaries = [
        {
            "id": p["id"],
            "name": p["name"],
            "price": p["price"],
            "shortDescription": p["shortDescription"],
            "thumbnailUrl": p["thumbnailUrl"],
            "category": p["category"],
        }
        for p in items
    ]
    return {"items": summaries, "total": len(summaries)}


@cache_ttl(settings.cache_ttl_seconds, key_prefix="products:byId")
def get_product_by_id(product_id: str) -> dict | None:
    return PRODUCTS_BY_ID.get(product_id)


def list_categories() -> list[str]:
    return sorted({p["category"] for p in PRODUCTS})
