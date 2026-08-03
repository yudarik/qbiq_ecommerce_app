<template>
  <main class="flex flex-col items-center justify-center min-h-[60vh] px-4 text-center">
    <div class="text-8xl font-black text-indigo-200 mb-4" aria-hidden="true">404</div>
    <h1 class="text-3xl font-bold text-gray-900 mb-3">Page not found</h1>
    <p class="text-gray-600 mb-8 max-w-md">
      The page you're looking for doesn't exist or may have been moved.
    </p>
    <router-link
      to="/"
      class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2.5 rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
    >
      Back to home
    </router-link>
  </main>
</template>
