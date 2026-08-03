export interface ProductReview {
  reviewerName: string
  rating: number
  comment: string
  date?: string
}

export interface ProductSummary {
  id: string
  name: string
  price: number
  shortDescription: string
  thumbnailUrl: string
  category: string
}

export interface Product extends ProductSummary {
  longDescription: string
  reviews: ProductReview[]
}

export interface ProductListResponse {
  items: ProductSummary[]
  total: number
}

export type SortBy = 'price' | 'name'
export type SortOrder = 'asc' | 'desc'

export interface ProductFilters {
  name: string
  category: string
  sortBy: SortBy | ''
  sortOrder: SortOrder
}
