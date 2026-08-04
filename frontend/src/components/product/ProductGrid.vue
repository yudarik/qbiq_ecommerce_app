<script setup lang="ts">
import type { ProductSummary } from '@/types/product'
import ProductCard from './ProductCard.vue'

defineProps<{
  products: ProductSummary[]
}>()
</script>

<template>
  <div
    v-if="products.length > 0"
    class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4"
    role="list"
    aria-label="Products"
  >
    <div v-for="product in products" :key="product.id" role="listitem" class="h-full">
      <ProductCard :product="product" />
    </div>
  </div>

  <div v-else class="flex flex-col items-center justify-center py-20 text-center">
    <div class="text-6xl mb-4" aria-hidden="true">📭</div>
    <h2 class="text-xl font-semibold text-gray-900 mb-2">No products found</h2>
    <p class="text-gray-500">Try adjusting your filters to see more results.</p>
  </div>
</template>
