# qbiq eCommerce — Full Stack Assignment

A mini e-commerce platform for browsing and purchasing digital books. Built as a full-stack home assignment demonstrating Vue 3 + FastAPI + Redis.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vue 3 · TypeScript · Vite · Pinia · Vue Router · Tailwind CSS v4 · PrimeVue v4 |
| Backend | Python 3.11 · FastAPI · Pydantic v2 |
| Caching | Redis (TTL cache on product endpoints) |
| Testing | pytest (backend) · Vitest + @vue/test-utils (frontend) |
| Infra | Docker · Docker Compose |

## Project Structure

```
qbiq_ecommerce/
├── docker-compose.yml       # Starts all 3 services
├── .env.example             # All configurable env vars
├── backend/                 # FastAPI Python app
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/          # Pydantic models (Product, Cart, ...)
│   │   ├── data/            # 20-book seed dataset + loader
│   │   ├── routers/         # products.py + cart.py
│   │   ├── services/        # Business logic (filter/sort, cart ops)
│   │   └── cache/           # Redis client + @cache_ttl decorator
│   └── tests/               # pytest suite (37 tests)
└── frontend/                # Vue 3 app
    └── src/
        ├── types/           # TypeScript interfaces
        ├── api/             # Typed axios wrappers
        ├── stores/          # Pinia cart + products stores
        ├── router/          # Vue Router with 404 catch-all
        ├── views/           # ProductList, ProductDetails, Cart, NotFound
        └── components/      # Reusable UI components
```

## Quick Start (Docker)

```bash
# Build and start all services
docker-compose up --build
```

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`

## Local Development (without Docker)

**Backend:**
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Start Redis (requires Docker or a local Redis install)
docker run -d -p 6379:6379 redis:7-alpine

uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Running Tests

**Backend** (no live Redis required — uses fakeredis):
```bash
cd backend
source .venv/bin/activate
pytest -v
# Expected: 37 passed
```

**Frontend:**
```bash
cd frontend
npm run test
# Expected: 8 passed
```

## Pages

| Page | Route | Description |
|---|---|---|
| Product List | `/` | Browse all books with name/category filter and price/title sort |
| Product Details | `/products/:id` | Full description, reviews, Add to Cart |
| Cart | `/cart` | Update quantities, remove items, see running total |
| 404 | `/*` | Catch-all not-found page |

## Architecture Decisions

**Server-backed cart with Pinia mirroring**: The backend owns cart state (in-memory, keyed by a UUID `cart_id` stored in `localStorage`). Every cart mutation (`addToCart`, `updateQuantity`, `removeItem`) calls the backend API and replaces the Pinia store state from the response. Pinia is the reactive source of truth for the UI; the backend is the persistence layer. In-memory only — resets on server restart (intentional given mock-data scope).

**Generic Redis TTL cache decorator**: A `@cache_ttl(ttl_seconds, key_prefix)` decorator in `backend/app/cache/decorators.py` wraps any pure function returning a JSON-serializable dict/list. Applied to `list_products(...)` and `get_product_by_id(...)`. Cache key = `prefix + sorted-kwargs-json`. TTL = 60s by default. Completely decoupled from FastAPI and Pydantic — tests use `fakeredis.FakeStrictRedis` via an autouse conftest fixture.

**Curated book dataset**: 20 real, recognizable books across 5 genre categories (Fiction, Non-Fiction, Programming, Business, Self-Help). Cover images from the public Open Library Covers API (`https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg`).

## Known Limitations

- Cart state is in-memory and resets on backend restart (no database persistence — intentional for assignment scope).
- Redis cache also resets on restart.
- No authentication or user accounts.
- Checkout button is a UI mock — no payment processing.
