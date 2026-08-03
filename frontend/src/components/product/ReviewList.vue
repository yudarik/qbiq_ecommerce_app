<script setup lang="ts">
import type { ProductReview } from '@/types/product'

defineProps<{
  reviews: ProductReview[]
}>()

function stars(rating: number): string {
  return '★'.repeat(rating) + '☆'.repeat(5 - rating)
}
</script>

<template>
  <section aria-labelledby="reviews-heading">
    <h2 id="reviews-heading" class="text-xl font-bold text-gray-900 mb-4">
      Customer Reviews ({{ reviews.length }})
    </h2>

    <div v-if="reviews.length === 0" class="text-gray-500 italic">No reviews yet.</div>

    <ul class="space-y-4" aria-label="Customer reviews list">
      <li
        v-for="(review, i) in reviews"
        :key="i"
        class="bg-gray-50 rounded-lg p-4 border border-gray-100"
      >
        <div class="flex items-center justify-between mb-2">
          <span class="font-semibold text-gray-900 text-sm">{{ review.reviewerName }}</span>
          <div class="flex items-center gap-2">
            <span
              class="text-yellow-400 text-base"
              :aria-label="`Rating: ${review.rating} out of 5 stars`"
            >
              {{ stars(review.rating) }}
            </span>
            <span v-if="review.date" class="text-xs text-gray-400">{{ review.date }}</span>
          </div>
        </div>
        <p class="text-sm text-gray-700">{{ review.comment }}</p>
      </li>
    </ul>
  </section>
</template>
