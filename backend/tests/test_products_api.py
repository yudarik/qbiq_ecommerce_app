def test_health(api_client):
    res = api_client.get("/health")
    assert res.status_code == 200


def test_list_all_products(api_client):
    res = api_client.get("/api/products")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 20
    assert len(data["items"]) == 20


def test_filter_by_category(api_client):
    res = api_client.get("/api/products?category=Fiction")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 4
    assert all(item["category"] == "Fiction" for item in data["items"])


def test_sort_by_price_desc(api_client):
    res = api_client.get("/api/products?sort_by=price&sort_order=desc")
    assert res.status_code == 200
    prices = [item["price"] for item in res.json()["items"]]
    assert prices == sorted(prices, reverse=True)


def test_filter_by_name(api_client):
    res = api_client.get("/api/products?name=gatsby")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 1
    assert data["items"][0]["id"] == "the-great-gatsby"


def test_get_product_valid_id(api_client):
    res = api_client.get("/api/products/atomic-habits")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == "atomic-habits"
    assert "longDescription" in data
    assert isinstance(data["reviews"], list)


def test_get_product_invalid_id(api_client):
    res = api_client.get("/api/products/does-not-exist")
    assert res.status_code == 404


def test_get_categories(api_client):
    res = api_client.get("/api/categories")
    assert res.status_code == 200
    cats = res.json()
    assert set(cats) == {"Fiction", "Non-Fiction", "Programming", "Business", "Self-Help"}


def test_cart_add_and_get(api_client):
    cart_id = "test-session-123"
    res = api_client.post(
        "/api/cart/items",
        json={"productId": "1984", "quantity": 1},
        headers={"X-Cart-Id": cart_id},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["cartId"] == cart_id
    assert len(data["items"]) == 1


def test_cart_update_quantity(api_client):
    cart_id = "test-session-456"
    api_client.post(
        "/api/cart/items",
        json={"productId": "sapiens", "quantity": 1},
        headers={"X-Cart-Id": cart_id},
    )
    res = api_client.put(
        "/api/cart/items/sapiens",
        json={"quantity": 3},
        headers={"X-Cart-Id": cart_id},
    )
    assert res.status_code == 200
    assert res.json()["items"][0]["quantity"] == 3


def test_cart_remove_item(api_client):
    cart_id = "test-session-789"
    api_client.post(
        "/api/cart/items",
        json={"productId": "mindset", "quantity": 2},
        headers={"X-Cart-Id": cart_id},
    )
    res = api_client.delete(
        "/api/cart/items/mindset",
        headers={"X-Cart-Id": cart_id},
    )
    assert res.status_code == 200
    assert res.json()["items"] == []
