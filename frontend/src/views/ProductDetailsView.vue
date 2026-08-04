<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import type { Product } from '@/types/product'
import { fetchProductById } from '@/api/products'
import { useCartStore } from '@/stores/cart'
import ReviewList from '@/components/product/ReviewList.vue'
import ErrorState from '@/components/common/ErrorState.vue'

const props = defineProps<{ id: string }>()
const router = useRouter()
const toast = useToast()
const cartStore = useCartStore()

const product = ref<Product | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)
const addingToCart = ref(false)
const quantity = ref(1)

onMounted(async () => {
  try {
    product.value = await fetchProductById(props.id)
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : 'Product not found'
  } finally {
    loading.value = false
  }
})

async function addToCart() {
  if (!product.value) return
  addingToCart.value = true
  try {
    await cartStore.addToCart(product.value.id, quantity.value)
    toast.add({
      severity: 'success',
      summary: 'Added to cart',
      detail: `${product.value.name} × ${quantity.value}`,
      life: 3000,
    })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to add item to cart',
      life: 4000,
    })
  } finally {
    addingToCart.value = false
  }
}

function formatPrice(price: number): string {
  return `$${price.toFixed(2)}`
}
</script>

<template>
  <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <button
      class="flex items-center gap-2 text-sm text-gray-600 hover:text-indigo-600 mb-6 transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 rounded"
      aria-label="Back to product list"
      @click="router.push({ name: 'products' })"
    >
      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
      Back to Products
    </button>

    <!-- Loading skeleton -->
    <div v-if="loading" class="animate-pulse" aria-busy="true" aria-label="Loading product">
      <div class="flex flex-col md:flex-row gap-8">
        <div class="w-full md:w-64 flex-shrink-0">
          <div class="aspect-[3/4] bg-gray-200 rounded-xl" />
        </div>
        <div class="flex-1 space-y-4">
          <div class="h-8 bg-gray-200 rounded w-3/4" />
          <div class="h-5 bg-gray-200 rounded w-1/4" />
          <div class="h-4 bg-gray-200 rounded w-full" />
          <div class="h-4 bg-gray-200 rounded w-5/6" />
          <div class="h-10 bg-gray-200 rounded w-1/3 mt-4" />
        </div>
      </div>
    </div>

    <!-- Error state -->
    <ErrorState
      v-else-if="error"
      :message="error"
    />

    <!-- Product content -->
    <article v-else-if="product">
      <div class="flex flex-col md:flex-row gap-8 mb-10">
        <div class="w-full md:w-64 flex-shrink-0">
          <img
            :src="product.thumbnailUrl"
            :alt="`Cover of ${product.name}`"
            class="w-full rounded-xl shadow-md object-cover"
            @error="($event.target as HTMLImageElement).src = 'https://via.placeholder.com/300x400?text=No+Cover'"
          />
        </div>

        <div class="flex-1">
          <span class="inline-block text-sm font-medium text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full mb-3">
            {{ product.category }}
          </span>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ product.name }}</h1>
          <p class="text-3xl font-bold text-indigo-600 mb-4">{{ formatPrice(product.price) }}</p>
          <p class="text-gray-700 mb-4 leading-relaxed">{{ product.shortDescription }}</p>
          <p class="text-gray-600 leading-relaxed mb-6">{{ product.longDescription }}</p>

          <div class="flex items-center gap-4">
            <div class="flex items-center gap-2">
              <label for="quantity" class="text-sm font-medium text-gray-700">Qty:</label>
              <input
                id="quantity"
                v-model.number="quantity"
                type="number"
                min="1"
                max="99"
                class="w-16 border border-gray-300 rounded-lg px-2 py-1.5 text-sm text-center focus:outline-none focus:ring-2 focus:ring-indigo-500"
                aria-label="Quantity"
              />
            </div>

            <button
              :disabled="addingToCart"
              class="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white px-6 py-2.5 rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
              aria-label="Add to cart"
              @click="addToCart"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              {{ addingToCart ? 'Adding...' : 'Add to Cart' }}
            </button>
          </div>
        </div>
      </div>

      <ReviewList :reviews="product.reviews" />
    </article>
  </main>
</template>
