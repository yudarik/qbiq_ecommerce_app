<template>
  <div
    class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4"
    aria-busy="true"
    aria-label="Loading products"
  >
    <div
      v-for="i in 10"
      :key="i"
      class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100 animate-pulse"
      aria-hidden="true"
    >
      <div class="aspect-[3/4] bg-gray-200" />
      <div class="p-4 space-y-2">
        <div class="h-3 bg-gray-200 rounded w-1/3" />
        <div class="h-4 bg-gray-200 rounded w-full" />
        <div class="h-4 bg-gray-200 rounded w-3/4" />
        <div class="h-5 bg-gray-200 rounded w-1/4 mt-2" />
      </div>
    </div>
  </div>
</template>
