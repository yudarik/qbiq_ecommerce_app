# Frontend — qbiq eCommerce

Vue 3 + TypeScript + Vite frontend for the qbiq eCommerce platform.

## Tech Stack

- **Vue 3** with Composition API
- **TypeScript** — full type coverage throughout
- **Vite** — build tool
- **Pinia** — global state management (cart store)
- **Vue Router** — client-side routing
- **Tailwind CSS v4** — utility-first styling
- **PrimeVue v4** — UI component library (Aura theme)
- **axios** — HTTP client
- **Vitest** + **@vue/test-utils** — unit testing

## Local Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy env file and adjust if needed
cp .env.example .env
```

## Running in Development

Requires the backend API running on port 8000 (see `backend/README.md`):

```bash
npm run dev
```

App available at `http://localhost:5173`

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `VITE_API_BASE_URL` | `http://localhost:8000/api` | Backend API base URL (no trailing slash) |

## Build for Production

```bash
npm run build
```

Output goes to `dist/`. The built app requires an nginx (or similar) server that handles SPA routing by returning `index.html` for all 404s (see the Docker section in the root README for a ready-made nginx config).

## Running Tests

```bash
npm run test
```

Runs the Vitest unit test suite (no browser needed). Expected: **8 tests passing**.

To run in watch mode during development:

```bash
npm run test:watch
```

## Pages

| Route | Description |
|---|---|
| `/` | Product list with filtering and sorting |
| `/products/:id` | Product detail page |
| `/cart` | Shopping cart |
| `/*` | 404 page |

## Architecture Notes

- **Cart state**: The cart store (`src/stores/cart.ts`) calls the backend REST API on every mutation (`addToCart`, `updateQuantity`, `removeItem`) and replaces local state from the full response. The Pinia store is the reactive source of truth the UI reads from; the backend is the persistence layer. The `cartId` is stored in `localStorage` and sent as the `X-Cart-Id` header.
- **API client**: A single axios instance in `src/api/client.ts` with a response interceptor that normalizes all errors to `Error(message)` before they reach component code.
- **Type aliases**: All source imports use `@/` for the `src/` directory, configured in both `vite.config.ts` and `tsconfig.app.json`.
