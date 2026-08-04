export interface CartItem {
  productId: string
  quantity: number
  name: string
  price: number
  thumbnailUrl: string
  lineTotal: number
}

export interface Cart {
  cartId: string
  items: CartItem[]
  total: number
}
