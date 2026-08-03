import client from './client'
import type { Cart } from '@/types/cart'

const CART_ID_KEY = 'qbiq_cart_id'

export function getStoredCartId(): string | null {
  return localStorage.getItem(CART_ID_KEY)
}

export function storeCartId(cartId: string): void {
  localStorage.setItem(CART_ID_KEY, cartId)
}

function cartHeaders(): Record<string, string> {
  const cartId = getStoredCartId()
  return cartId ? { 'X-Cart-Id': cartId } : {}
}

export async function getCart(): Promise<Cart> {
  const res = await client.get<Cart>('/cart', { headers: cartHeaders() })
  storeCartId(res.data.cartId)
  return res.data
}

export async function addCartItem(productId: string, quantity = 1): Promise<Cart> {
  const res = await client.post<Cart>(
    '/cart/items',
    { productId, quantity },
    { headers: cartHeaders() },
  )
  storeCartId(res.data.cartId)
  return res.data
}

export async function updateCartItem(productId: string, quantity: number): Promise<Cart> {
  const res = await client.put<Cart>(
    `/cart/items/${productId}`,
    { quantity },
    { headers: cartHeaders() },
  )
  return res.data
}

export async function removeCartItem(productId: string): Promise<Cart> {
  const res = await client.delete<Cart>(`/cart/items/${productId}`, { headers: cartHeaders() })
  return res.data
}
