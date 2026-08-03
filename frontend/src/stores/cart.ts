import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { CartItem } from '@/types/cart'
import * as cartApi from '@/api/cart'

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])
  const cartId = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const itemCount = computed(() => items.value.reduce((sum, item) => sum + item.quantity, 0))
  const total = computed(() =>
    Math.round(items.value.reduce((sum, item) => sum + item.lineTotal, 0) * 100) / 100,
  )

  function _applyCart(cart: { cartId: string; items: CartItem[] }) {
    cartId.value = cart.cartId
    items.value = cart.items
  }

  async function initCart() {
    try {
      const cart = await cartApi.getCart()
      _applyCart(cart)
    } catch {
      // silently ignore on init — cart will be created on first add
    }
  }

  async function addToCart(productId: string, quantity = 1) {
    loading.value = true
    error.value = null
    try {
      const cart = await cartApi.addCartItem(productId, quantity)
      _applyCart(cart)
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Failed to add item'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateQuantity(productId: string, quantity: number) {
    loading.value = true
    error.value = null
    try {
      const cart = await cartApi.updateCartItem(productId, quantity)
      _applyCart(cart)
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Failed to update item'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function removeItem(productId: string) {
    loading.value = true
    error.value = null
    try {
      const cart = await cartApi.removeCartItem(productId)
      _applyCart(cart)
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Failed to remove item'
      throw e
    } finally {
      loading.value = false
    }
  }

  return { items, cartId, loading, error, itemCount, total, initCart, addToCart, updateQuantity, removeItem }
})
