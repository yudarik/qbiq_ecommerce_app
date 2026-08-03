<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useProductsStore } from '@/stores/products'
import FilterBar from '@/components/product/FilterBar.vue'
import ProductGrid from '@/components/product/ProductGrid.vue'
import ProductSkeleton from '@/components/product/ProductSkeleton.vue'
import ErrorState from '@/components/common/ErrorState.vue'
import type { ProductFilters } from '@/types/product'

const store = useProductsStore()

onMounted(async () => {
  await Promise.all([store.loadProducts(), store.loadCategories()])
})

function onFiltersChange(newFilters: ProductFilters) {
  store.filters.name = newFilters.name
  store.filters.category = newFilters.category
  store.filters.sortBy = newFilters.sortBy
  store.filters.sortOrder = newFilters.sortOrder
}

watch(
  () => [store.filters.category, store.filters.sortBy, store.filters.sortOrder],
  () => store.loadProducts(),
)

watch(
  () => store.filters.name,
  () => store.loadProducts(),
)
</script>

<template>
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Browse Books</h1>
      <p v-if="!store.loading && !store.error" class="text-sm text-gray-500 mt-1">
        {{ store.total }} book{{ store.total === 1 ? '' : 's' }} available
      </p>
    </div>

    <FilterBar
      :filters="store.filters"
      :categories="store.categories"
      @change="onFiltersChange"
    />

    <ErrorState
      v-if="store.error"
      :message="store.error"
      show-retry
      @retry="store.loadProducts()"
    />
    <ProductSkeleton v-else-if="store.loading" />
    <ProductGrid v-else :products="store.items" />
  </main>
</template>
