<script setup lang="ts">
import type { CartItem } from '@/types/cart'
import { useCartStore } from '@/stores/cart'

defineProps<{ item: CartItem }>()

const cartStore = useCartStore()

async function onQtyChange(item: CartItem, event: Event) {
  const qty = parseInt((event.target as HTMLInputElement).value)
  if (!isNaN(qty) && qty >= 1) {
    await cartStore.updateQuantity(item.productId, qty)
  }
}

async function onRemove(productId: string) {
  await cartStore.removeItem(productId)
}
</script>

<template>
  <li class="flex items-center gap-4 py-4 border-b border-gray-100 last:border-0">
    <img
      :src="item.thumbnailUrl"
      :alt="`Cover of ${item.name}`"
      class="w-16 h-20 object-cover rounded-lg flex-shrink-0 shadow-sm"
      @error="($event.target as HTMLImageElement).src = 'https://via.placeholder.com/64x80?text=Book'"
    />

    <div class="flex-1 min-w-0">
      <router-link
        :to="`/products/${item.productId}`"
        class="text-sm font-semibold text-gray-900 hover:text-indigo-600 line-clamp-2 transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 rounded"
      >
        {{ item.name }}
      </router-link>
      <p class="text-sm text-gray-500 mt-0.5">${{ item.price.toFixed(2) }} each</p>
    </div>

    <div class="flex items-center gap-3 flex-shrink-0">
      <div class="flex items-center gap-1">
        <label :for="`qty-${item.productId}`" class="sr-only">Quantity for {{ item.name }}</label>
        <input
          :id="`qty-${item.productId}`"
          type="number"
          :value="item.quantity"
          min="1"
          max="99"
          class="w-16 border border-gray-300 rounded-lg px-2 py-1.5 text-sm text-center focus:outline-none focus:ring-2 focus:ring-indigo-500"
          @change="onQtyChange(item, $event)"
        />
      </div>

      <span class="text-sm font-bold text-indigo-600 w-16 text-right">
        ${{ item.lineTotal.toFixed(2) }}
      </span>

      <button
        class="text-gray-400 hover:text-red-500 transition-colors p-1 rounded focus:outline-none focus:ring-2 focus:ring-red-400"
        :aria-label="`Remove ${item.name} from cart`"
        @click="onRemove(item.productId)"
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
    </div>
  </li>
</template>
