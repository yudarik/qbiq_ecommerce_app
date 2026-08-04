from app.services.product_service import list_products, list_categories


def test_list_all_products():
    result = list_products()
    assert result["total"] == 20
    assert len(result["items"]) == 20


def test_filter_by_name_case_insensitive():
    result = list_products(name="atomic")
    assert result["total"] == 1
    assert result["items"][0]["name"] == "Atomic Habits"


def test_filter_by_name_no_match():
    result = list_products(name="zzznomatch")
    assert result["total"] == 0


def test_filter_by_category():
    result = list_products(category="Fiction")
    assert result["total"] == 4
    assert all(item["category"] == "Fiction" for item in result["items"])


def test_filter_by_category_no_match():
    result = list_products(category="Cooking")
    assert result["total"] == 0


def test_combined_filter_name_and_category():
    result = list_products(name="1984", category="Fiction")
    assert result["total"] == 1
    assert result["items"][0]["id"] == "1984"


def test_combined_filter_name_and_wrong_category():
    result = list_products(name="1984", category="Business")
    assert result["total"] == 0


def test_sort_by_price_asc():
    result = list_products(sort_by="price", sort_order="asc")
    prices = [item["price"] for item in result["items"]]
    assert prices == sorted(prices)


def test_sort_by_price_desc():
    result = list_products(sort_by="price", sort_order="desc")
    prices = [item["price"] for item in result["items"]]
    assert prices == sorted(prices, reverse=True)


def test_sort_by_name_asc():
    result = list_products(sort_by="name", sort_order="asc")
    names = [item["name"] for item in result["items"]]
    assert names == sorted(names)


def test_sort_by_name_desc():
    result = list_products(sort_by="name", sort_order="desc")
    names = [item["name"] for item in result["items"]]
    assert names == sorted(names, reverse=True)


def test_filter_and_sort_combined():
    result = list_products(category="Programming", sort_by="price", sort_order="asc")
    assert result["total"] == 4
    prices = [item["price"] for item in result["items"]]
    assert prices == sorted(prices)


def test_list_categories():
    cats = list_categories()
    assert set(cats) == {"Fiction", "Non-Fiction", "Programming", "Business", "Self-Help"}
    assert cats == sorted(cats)
