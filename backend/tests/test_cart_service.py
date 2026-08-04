import pytest

from app.services import cart_service


@pytest.fixture(autouse=True)
def clear_carts():
    """Reset in-memory cart state between tests."""
    cart_service._carts.clear()
    yield
    cart_service._carts.clear()


def test_get_empty_cart():
    cart = cart_service.get_cart("test-cart")
    assert cart["cartId"] == "test-cart"
    assert cart["items"] == []
    assert cart["total"] == 0.0


def test_add_item():
    cart = cart_service.add_item("cart1", "atomic-habits", 1)
    assert len(cart["items"]) == 1
    assert cart["items"][0]["productId"] == "atomic-habits"
    assert cart["items"][0]["quantity"] == 1
    assert cart["total"] > 0


def test_add_item_increments_existing():
    cart_service.add_item("cart1", "1984", 1)
    cart = cart_service.add_item("cart1", "1984", 2)
    assert cart["items"][0]["quantity"] == 3


def test_add_item_product_not_found():
    with pytest.raises(KeyError):
        cart_service.add_item("cart1", "nonexistent-book", 1)


def test_update_item_quantity():
    cart_service.add_item("cart1", "sapiens", 1)
    cart = cart_service.update_item("cart1", "sapiens", 5)
    assert cart["items"][0]["quantity"] == 5
    assert cart["items"][0]["lineTotal"] == round(cart["items"][0]["price"] * 5, 2)


def test_update_item_not_in_cart():
    with pytest.raises(KeyError):
        cart_service.update_item("cart1", "deep-work", 1)


def test_remove_item():
    cart_service.add_item("cart1", "mindset", 2)
    cart = cart_service.remove_item("cart1", "mindset")
    assert cart["items"] == []
    assert cart["total"] == 0.0


def test_remove_nonexistent_item_is_idempotent():
    cart = cart_service.remove_item("cart1", "does-not-exist")
    assert cart["items"] == []


def test_total_calculated_correctly():
    cart_service.add_item("cart1", "1984", 2)        # 8.99 * 2 = 17.98
    cart_service.add_item("cart1", "deep-work", 1)    # 15.99 * 1 = 15.99
    cart = cart_service.get_cart("cart1")
    expected = round(8.99 * 2 + 15.99, 2)
    assert cart["total"] == expected
