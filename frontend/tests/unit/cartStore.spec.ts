import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCartStore } from '@/stores/cart'
import type { Cart } from '@/types/cart'

// Mock the cart API module
vi.mock('@/api/cart', () => ({
  getCart: vi.fn(),
  addCartItem: vi.fn(),
  updateCartItem: vi.fn(),
  removeCartItem: vi.fn(),
  getStoredCartId: vi.fn(() => 'test-cart-id'),
  storeCartId: vi.fn(),
}))

import * as cartApi from '@/api/cart'

function makeCart(overrides: Partial<Cart> = {}): Cart {
  return {
    cartId: 'test-cart-id',
    items: [],
    total: 0,
    ...overrides,
  }
}

describe('cartStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('starts with an empty cart', () => {
    const store = useCartStore()
    expect(store.items).toEqual([])
    expect(store.itemCount).toBe(0)
    expect(store.total).toBe(0)
  })

  it('addToCart updates items from API response', async () => {
    const cart = makeCart({
      items: [
        { productId: 'atomic-habits', quantity: 1, name: 'Atomic Habits', price: 16.99, thumbnailUrl: '', lineTotal: 16.99 },
      ],
      total: 16.99,
    })
    vi.mocked(cartApi.addCartItem).mockResolvedValueOnce(cart)

    const store = useCartStore()
    await store.addToCart('atomic-habits', 1)

    expect(store.items).toHaveLength(1)
    expect(store.items[0].productId).toBe('atomic-habits')
    expect(store.items[0].quantity).toBe(1)
  })

  it('itemCount sums quantities across items', async () => {
    const cart = makeCart({
      items: [
        { productId: 'book-1', quantity: 2, name: 'Book 1', price: 10, thumbnailUrl: '', lineTotal: 20 },
        { productId: 'book-2', quantity: 3, name: 'Book 2', price: 8, thumbnailUrl: '', lineTotal: 24 },
      ],
      total: 44,
    })
    vi.mocked(cartApi.addCartItem).mockResolvedValueOnce(cart)

    const store = useCartStore()
    await store.addToCart('book-1', 2)

    expect(store.itemCount).toBe(5)
  })

  it('total getter sums lineTotals', async () => {
    const cart = makeCart({
      items: [
        { productId: 'book-1', quantity: 2, name: 'Book 1', price: 8.99, thumbnailUrl: '', lineTotal: 17.98 },
        { productId: 'book-2', quantity: 1, name: 'Book 2', price: 15.99, thumbnailUrl: '', lineTotal: 15.99 },
      ],
      total: 33.97,
    })
    vi.mocked(cartApi.addCartItem).mockResolvedValueOnce(cart)

    const store = useCartStore()
    await store.addToCart('book-1', 2)

    expect(store.total).toBe(33.97)
  })

  it('updateQuantity replaces item quantity from API response', async () => {
    const cartBefore = makeCart({
      items: [{ productId: '1984', quantity: 1, name: '1984', price: 8.99, thumbnailUrl: '', lineTotal: 8.99 }],
      total: 8.99,
    })
    vi.mocked(cartApi.addCartItem).mockResolvedValueOnce(cartBefore)

    const cartAfter = makeCart({
      items: [{ productId: '1984', quantity: 3, name: '1984', price: 8.99, thumbnailUrl: '', lineTotal: 26.97 }],
      total: 26.97,
    })
    vi.mocked(cartApi.updateCartItem).mockResolvedValueOnce(cartAfter)

    const store = useCartStore()
    await store.addToCart('1984', 1)
    await store.updateQuantity('1984', 3)

    expect(store.items[0].quantity).toBe(3)
    expect(store.items[0].lineTotal).toBe(26.97)
    expect(store.total).toBe(26.97)
  })

  it('removeItem empties cart on last item removal', async () => {
    const cartWithItem = makeCart({
      items: [{ productId: 'sapiens', quantity: 1, name: 'Sapiens', price: 18.99, thumbnailUrl: '', lineTotal: 18.99 }],
      total: 18.99,
    })
    vi.mocked(cartApi.addCartItem).mockResolvedValueOnce(cartWithItem)

    const emptyCart = makeCart()
    vi.mocked(cartApi.removeCartItem).mockResolvedValueOnce(emptyCart)

    const store = useCartStore()
    await store.addToCart('sapiens', 1)
    await store.removeItem('sapiens')

    expect(store.items).toEqual([])
    expect(store.itemCount).toBe(0)
    expect(store.total).toBe(0)
  })

  it('addToCart sets loading to false after success', async () => {
    vi.mocked(cartApi.addCartItem).mockResolvedValueOnce(makeCart())
    const store = useCartStore()
    await store.addToCart('book-1')
    expect(store.loading).toBe(false)
  })

  it('addToCart sets error and rethrows on API failure', async () => {
    vi.mocked(cartApi.addCartItem).mockRejectedValueOnce(new Error('Network error'))
    const store = useCartStore()
    await expect(store.addToCart('book-1')).rejects.toThrow('Network error')
    expect(store.error).toBe('Network error')
    expect(store.loading).toBe(false)
  })
})
