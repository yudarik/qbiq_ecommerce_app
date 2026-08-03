<script setup lang="ts">
defineProps<{
  message?: string
  showRetry?: boolean
}>()

const emit = defineEmits<{
  retry: []
}>()
</script>

<template>
  <div class="flex flex-col items-center justify-center py-16 px-4 text-center" role="alert">
    <div class="text-6xl mb-4" aria-hidden="true">⚠️</div>
    <h2 class="text-xl font-semibold text-gray-900 mb-2">Something went wrong</h2>
    <p class="text-gray-600 mb-6 max-w-md">{{ message || 'An unexpected error occurred. Please try again.' }}</p>
    <button
      v-if="showRetry"
      class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
      @click="emit('retry')"
    >
      Try again
    </button>
    <router-link
      to="/"
      class="mt-3 text-indigo-600 hover:text-indigo-800 underline text-sm"
    >
      Back to products
    </router-link>
  </div>
</template>
