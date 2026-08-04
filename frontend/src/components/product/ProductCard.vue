<script setup lang="ts">
import type { ProductSummary } from '@/types/product'

defineProps<{
  product: ProductSummary
}>()

function formatPrice(price: number): string {
  return `$${price.toFixed(2)}`
}
</script>

<template>
  <article class="h-full flex flex-col bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow overflow-hidden border border-gray-100">
    <router-link
      :to="`/products/${product.id}`"
      class="flex flex-col flex-1 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
      :aria-label="`View details for ${product.name}`"
    >
      <div class="aspect-[3/4] shrink-0 overflow-hidden bg-gray-100">
        <img
          :src="product.thumbnailUrl"
          :alt="`Cover of ${product.name}`"
          class="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
          loading="lazy"
          @error="($event.target as HTMLImageElement).src = 'https://via.placeholder.com/200x280?text=No+Cover'"
        />
      </div>
      <div class="flex flex-col flex-1 p-4">
        <span class="self-start text-xs font-medium text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded mb-2">
          {{ product.category }}
        </span>
        <h2 class="min-h-[2.5rem] text-sm font-semibold text-gray-900 line-clamp-2 mb-1">{{ product.name }}</h2>
        <p class="min-h-[2rem] text-xs text-gray-500 line-clamp-2 mb-3">{{ product.shortDescription }}</p>
        <p class="mt-auto text-lg font-bold text-indigo-600">{{ formatPrice(product.price) }}</p>
      </div>
    </router-link>
  </article>
</template>
