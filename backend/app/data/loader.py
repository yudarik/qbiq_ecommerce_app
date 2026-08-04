import json
from pathlib import Path

_DATA_FILE = Path(__file__).parent / "products.json"

with open(_DATA_FILE) as f:
    PRODUCTS: list[dict] = json.load(f)

PRODUCTS_BY_ID: dict[str, dict] = {p["id"]: p for p in PRODUCTS}
