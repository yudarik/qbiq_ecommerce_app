import client from './client'
import type { Product, ProductListResponse } from '@/types/product'

export async function fetchProducts(params: {
  name?: string
  category?: string
  sort_by?: string
  sort_order?: string
}): Promise<ProductListResponse> {
  const cleanParams: Record<string, string> = {}
  if (params.name) cleanParams.name = params.name
  if (params.category) cleanParams.category = params.category
  if (params.sort_by) cleanParams.sort_by = params.sort_by
  if (params.sort_order) cleanParams.sort_order = params.sort_order

  const res = await client.get<ProductListResponse>('/products', { params: cleanParams })
  return res.data
}

export async function fetchProductById(id: string): Promise<Product> {
  const res = await client.get<Product>(`/products/${id}`)
  return res.data
}

export async function fetchCategories(): Promise<string[]> {
  const res = await client.get<string[]>('/categories')
  return res.data
}
