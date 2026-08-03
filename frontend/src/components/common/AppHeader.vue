<script setup lang="ts">
import { useCartStore } from '@/stores/cart'
import { useRouter } from 'vue-router'

const cartStore = useCartStore()
const router = useRouter()
</script>

<template>
  <header class="sticky top-0 z-50 bg-white shadow-sm border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <router-link
          to="/"
          class="text-xl font-bold text-indigo-600 hover:text-indigo-700 transition-colors"
          aria-label="Go to home page"
        >
          📚 BookStore
        </router-link>

        <nav class="flex items-center gap-4" aria-label="Main navigation">
          <router-link
            to="/"
            class="text-gray-600 hover:text-indigo-600 transition-colors text-sm font-medium"
          >
            Products
          </router-link>

          <button
            class="relative flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            aria-label="`Go to shopping cart, ${cartStore.itemCount} items`"
            @click="router.push('/cart')"
          >
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            Cart
            <span
              v-if="cartStore.itemCount > 0"
              class="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold"
              aria-live="polite"
              :aria-label="`${cartStore.itemCount} items in cart`"
            >
              {{ cartStore.itemCount }}
            </span>
          </button>
        </nav>
      </div>
    </div>
  </header>
</template>
