<script setup lang="ts">
import { watch, ref } from 'vue'
import type { ProductFilters } from '@/types/product'

const props = defineProps<{
  filters: ProductFilters
  categories: string[]
}>()

const emit = defineEmits<{
  change: [filters: ProductFilters]
}>()

const localName = ref(props.filters.name)
let debounceTimer: ReturnType<typeof setTimeout> | null = null

function onNameInput(value: string) {
  localName.value = value
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    emit('change', { ...props.filters, name: value })
  }, 300)
}

function onCategoryChange(value: string) {
  emit('change', { ...props.filters, category: value })
}

function onSortByChange(value: string) {
  emit('change', { ...props.filters, sortBy: value as ProductFilters['sortBy'] })
}

function onSortOrderChange(value: string) {
  emit('change', { ...props.filters, sortOrder: value as 'asc' | 'desc' })
}

function clearFilters() {
  localName.value = ''
  emit('change', { name: '', category: '', sortBy: '', sortOrder: 'asc' })
}

watch(() => props.filters.name, (v) => {
  localName.value = v
})
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-6">
    <div class="flex flex-wrap gap-3 items-end">
      <div class="flex-1 min-w-[200px]">
        <label for="search-name" class="block text-xs font-medium text-gray-700 mb-1">Search by title</label>
        <input
          id="search-name"
          type="search"
          :value="localName"
          placeholder="e.g. Atomic Habits"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          aria-label="Search by product title"
          @input="onNameInput(($event.target as HTMLInputElement).value)"
        />
      </div>

      <div class="min-w-[160px]">
        <label for="filter-category" class="block text-xs font-medium text-gray-700 mb-1">Category</label>
        <select
          id="filter-category"
          :value="filters.category"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white"
          aria-label="Filter by category"
          @change="onCategoryChange(($event.target as HTMLSelectElement).value)"
        >
          <option value="">All categories</option>
          <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>

      <div class="min-w-[140px]">
        <label for="sort-by" class="block text-xs font-medium text-gray-700 mb-1">Sort by</label>
        <select
          id="sort-by"
          :value="filters.sortBy"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white"
          aria-label="Sort products by"
          @change="onSortByChange(($event.target as HTMLSelectElement).value)"
        >
          <option value="">Default</option>
          <option value="name">Title</option>
          <option value="price">Price</option>
        </select>
      </div>

      <div class="min-w-[120px]">
        <label for="sort-order" class="block text-xs font-medium text-gray-700 mb-1">Order</label>
        <select
          id="sort-order"
          :value="filters.sortOrder"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white"
          aria-label="Sort order"
          @change="onSortOrderChange(($event.target as HTMLSelectElement).value)"
        >
          <option value="asc">Ascending</option>
          <option value="desc">Descending</option>
        </select>
      </div>

      <button
        class="px-4 py-2 text-sm text-gray-600 hover:text-red-600 border border-gray-300 rounded-lg hover:border-red-300 transition-colors focus:outline-none focus:ring-2 focus:ring-red-400"
        aria-label="Clear all filters"
        @click="clearFilters"
      >
        Clear
      </button>
    </div>
  </div>
</template>
