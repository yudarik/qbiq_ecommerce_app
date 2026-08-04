<script setup lang="ts">
import { useCartStore } from '@/stores/cart'
import CartItemRow from '@/components/cart/CartItemRow.vue'

const cartStore = useCartStore()
</script>

<template>
  <main class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Shopping Cart</h1>

    <!-- Empty state -->
    <div v-if="cartStore.items.length === 0" class="text-center py-20">
      <div class="text-6xl mb-4" aria-hidden="true">🛒</div>
      <h2 class="text-xl font-semibold text-gray-900 mb-2">Your cart is empty</h2>
      <p class="text-gray-500 mb-6">Looks like you haven't added any books yet.</p>
      <router-link
        to="/"
        class="inline-block bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2.5 rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
      >
        Browse books
      </router-link>
    </div>

    <!-- Cart items -->
    <div v-else>
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
        <ul aria-label="Cart items" class="divide-y divide-gray-100">
          <CartItemRow
            v-for="item in cartStore.items"
            :key="item.productId"
            :item="item"
          />
        </ul>
      </div>

      <!-- Summary -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <div class="flex items-center justify-between mb-4">
          <span class="text-gray-600">
            {{ cartStore.itemCount }} item{{ cartStore.itemCount === 1 ? '' : 's' }}
          </span>
          <span class="text-2xl font-bold text-indigo-600" aria-live="polite">
            ${{ cartStore.total.toFixed(2) }}
          </span>
        </div>

        <button
          class="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-lg font-medium text-lg transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          aria-label="Proceed to checkout"
        >
          Proceed to Checkout
        </button>
        <p class="text-center text-xs text-gray-400 mt-3">
          This is a demo checkout — no payment will be processed.
        </p>
      </div>
    </div>
  </main>
</template>
