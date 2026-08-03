import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'
import type { ProductSummary, ProductFilters } from '@/types/product'
import { fetchProducts, fetchCategories } from '@/api/products'

export const useProductsStore = defineStore('products', () => {
  const items = ref<ProductSummary[]>([])
  const total = ref(0)
  const categories = ref<string[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const filters = reactive<ProductFilters>({
    name: '',
    category: '',
    sortBy: '',
    sortOrder: 'asc',
  })

  async function loadProducts() {
    loading.value = true
    error.value = null
    try {
      const data = await fetchProducts({
        name: filters.name || undefined,
        category: filters.category || undefined,
        sort_by: filters.sortBy || undefined,
        sort_order: filters.sortOrder,
      })
      items.value = data.items
      total.value = data.total
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Failed to load products'
    } finally {
      loading.value = false
    }
  }

  async function loadCategories() {
    try {
      categories.value = await fetchCategories()
    } catch {
      // non-critical, FilterBar will just show no options
    }
  }

  return { items, total, categories, loading, error, filters, loadProducts, loadCategories }
})
