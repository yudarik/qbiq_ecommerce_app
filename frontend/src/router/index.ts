import { createRouter, createWebHistory } from 'vue-router'
import ProductListView from '@/views/ProductListView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'products',
      component: ProductListView,
    },
    {
      path: '/products/:id',
      name: 'product-details',
      component: () => import('@/views/ProductDetailsView.vue'),
      props: true,
    },
    {
      path: '/cart',
      name: 'cart',
      component: () => import('@/views/CartView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue'),
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
