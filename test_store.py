import pytest

from main import create_store, start
from products import LimitedProduct, NonStockedProduct, Product
from promotions import SecondHalfPricePromotion, ThirdOneFreePromotion
from store import Store


def test_buy_remaining_stock_and_restock():
    product = Product("Coffee", 10, 2)
    assert product.buy(2)[1] == 20
    assert product.quantity == 0
    assert not product.active
    product.quantity = 3
    product.activate()
    assert product.buy(1)[1] == 10


@pytest.mark.parametrize("quantity", [0, -1, 1.5, True, "2", None])
def test_invalid_order_quantity_leaves_stock_unchanged(quantity):
    product = Product("Coffee", 10, 5)
    with pytest.raises(ValueError):
        Store([product]).order([(product, quantity)])
    assert product.quantity == 5


@pytest.mark.parametrize("price", [float("nan"), float("inf"), None, True])
def test_invalid_price(price):
    with pytest.raises(ValueError):
        Product("Coffee", price, 5)


def test_numeric_string_price_is_converted():
    assert Product("Coffee", "10.50", 5).price == 10.5


def test_non_stocked_direct_purchase_keeps_zero_stock():
    product = NonStockedProduct("License", 125)
    message, total = product.buy(100)
    assert total == 12500
    assert "items left" not in message
    assert product.quantity == 0
    assert product.active


def test_later_invalid_line_does_not_change_earlier_stock():
    coffee = Product("Coffee", 10, 5)
    tea = Product("Tea", 20, 1)
    with pytest.raises(ValueError):
        Store([coffee, tea]).order([(coffee, 2), (tea, 2)])
    assert coffee.quantity == 5
    assert tea.quantity == 1


def test_unknown_product_does_not_change_stock():
    coffee = Product("Coffee", 10, 5)
    tea = Product("Tea", 20, 1)
    with pytest.raises(AttributeError):
        Store([coffee]).order([(coffee, 2), (tea, 1)])
    assert coffee.quantity == 5


def test_limit_applies_to_combined_lines_and_allows_maximum():
    shipping = LimitedProduct("Shipping", 10, 5, maximum=1)
    store = Store([shipping])
    with pytest.raises(ValueError):
        store.order([(shipping, 1), (shipping, 1)])
    assert shipping.quantity == 5
    assert store.order([(shipping, 1)]) == 10


@pytest.mark.parametrize("promotion, expected", [
    (SecondHalfPricePromotion("Second half"), 550),
    (ThirdOneFreePromotion("Third free"), 500),
])
def test_promotion_applies_once_across_split_lines(promotion, expected):
    product = Product("Coffee", 100, 10)
    product.promotion = promotion
    assert Store([product]).order([(product, 3), (product, 3)]) == expected
    assert product.quantity == 4


def test_inactive_product_cannot_be_bought():
    product = Product("Coffee", 10, 5)
    product.deactivate()
    with pytest.raises(ValueError):
        Store([product]).order([(product, 1)])
    assert product.quantity == 5


def test_menu_handles_invalid_input_and_uses_supplied_store(monkeypatch, capsys):
    product = Product("Test", 10, 2)
    answers = iter(["invalid", "3", "1", "bad", "1", "1", "", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    start(Store([product]))
    output = capsys.readouterr().out
    assert "Please enter a valid choice" in output
    assert "Cannot add product" in output
    assert "Your total is: 10.00" in output
    assert product.quantity == 1


def test_example_order():
    store = create_store()
    macbook, earbuds, _, license_product, shipping = store.products
    assert store.order([
        (macbook, 3), (earbuds, 3), (license_product, 100), (shipping, 1),
    ]) == 3625 + 500 + 8750 + 10
