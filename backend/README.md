# Backend — qbiq eCommerce API

FastAPI + Python backend with server-side filtering/sorting, Redis TTL caching, and in-memory cart storage.

## Tech Stack

- **Python 3.10+**
- **FastAPI** — REST API framework
- **Pydantic v2** — data models and validation
- **Redis** — TTL caching via `redis-py`
- **fakeredis** — in-process Redis for tests (no live Redis required)
- **pytest** — test runner

## Local Setup

```bash
cd backend

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the API

Requires Redis running locally on the default port (or override `REDIS_URL`):

```bash
# Start Redis (one option via Docker)
docker run -d -p 6379:6379 redis:7-alpine

# Start the API server
uvicorn app.main:app --reload
```

API available at: `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection URL |
| `CACHE_TTL_SECONDS` | `60` | Cache TTL in seconds |
| `CORS_ORIGINS` | `http://localhost:5173` | Comma-separated allowed CORS origins |

Copy `.env.example` to `.env` and adjust values before running.

## API Endpoints

### Products

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/products` | List products with optional filter/sort |
| `GET` | `/api/products/{id}` | Get a single product by ID |
| `GET` | `/api/categories` | List all distinct product categories |

**`GET /api/products` query parameters:**

| Param | Type | Description |
|---|---|---|
| `name` | `string` | Case-insensitive substring match on product name |
| `category` | `string` | Exact category match (e.g. `Fiction`, `Programming`) |
| `sort_by` | `price` \| `name` | Field to sort by |
| `sort_order` | `asc` \| `desc` | Sort direction (default: `asc`) |

**Response:**
```json
{
  "items": [
    {
      "id": "atomic-habits",
      "name": "Atomic Habits",
      "price": 16.99,
      "shortDescription": "...",
      "thumbnailUrl": "https://covers.openlibrary.org/...",
      "category": "Self-Help"
    }
  ],
  "total": 1
}
```

### Cart

Cart items are stored in server-side in-memory storage keyed by a `cart_id`. The client generates and stores its own `cart_id` (UUID) in `localStorage` and sends it as the `X-Cart-Id` request header. If the header is absent, a new cart is created and its ID is returned in the response body.

**Note:** The in-memory cart resets when the server restarts. This is intentional given the mock-data scope of this assignment.

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/cart` | Get the current cart |
| `POST` | `/api/cart/items` | Add or increment an item |
| `PUT` | `/api/cart/items/{product_id}` | Set quantity for an item |
| `DELETE` | `/api/cart/items/{product_id}` | Remove an item from the cart |

All cart endpoints accept and return `X-Cart-Id` as a header and respond with the full `Cart` object.

**`POST /api/cart/items` body:**
```json
{ "productId": "1984", "quantity": 2 }
```

**`PUT /api/cart/items/{id}` body:**
```json
{ "quantity": 5 }
```

**Cart response:**
```json
{
  "cartId": "...",
  "items": [
    {
      "productId": "1984",
      "quantity": 2,
      "name": "1984",
      "price": 8.99,
      "thumbnailUrl": "...",
      "lineTotal": 17.98
    }
  ],
  "total": 17.98
}
```

## Running Tests

No live Redis required — tests use `fakeredis` automatically:

```bash
source .venv/bin/activate
pytest -v
```

Expected: **37 tests passing**.

## Caching Architecture

A generic `@cache_ttl(ttl_seconds, key_prefix)` decorator in `app/cache/decorators.py` wraps any pure function returning a JSON-serializable dict or list. The cache key is derived from the key prefix plus the function's sorted keyword arguments. Applied to `list_products(...)` and `get_product_by_id(...)` in `product_service.py`.
