<script setup lang="ts">
import { onMounted } from 'vue'
import Toast from 'primevue/toast'
import AppHeader from '@/components/common/AppHeader.vue'
import { useCartStore } from '@/stores/cart'

const cartStore = useCartStore()
onMounted(() => cartStore.initCart())
</script>

<template>
  <div id="app-root" class="min-h-screen bg-gray-50">
    <AppHeader />
    <router-view />
    <Toast position="bottom-right" />
  </div>
</template>
