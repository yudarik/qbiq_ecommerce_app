from pydantic import Field

from app.models.common import CamelModel


class ProductReview(CamelModel):
    reviewer_name: str
    rating: int = Field(ge=1, le=5)
    comment: str
    date: str | None = None


class ProductSummary(CamelModel):
    id: str
    name: str
    price: float
    short_description: str
    thumbnail_url: str
    category: str


class Product(ProductSummary):
    long_description: str
    reviews: list[ProductReview] = []


class ProductListResponse(CamelModel):
    items: list[ProductSummary]
    total: int
