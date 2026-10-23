import pytest

from products import Product, NonStockedProduct
from promotions import (
    SecondHalfPricePromotion, ThirdOneFreePromotion, PercentDiscountPromotion,
)
from store import Store


@pytest.mark.parametrize("quantity, expected", [(1, 100), (2, 150), (3, 250), (4, 350), (100, 9950)])
def test_second_half_price(quantity, expected):
    product = Product("Coffee", 100, 101)
    product.promotion = SecondHalfPricePromotion("Second half price")
    assert product.buy(quantity)[1] == expected
    assert product.quantity == 101 - quantity


@pytest.mark.parametrize("quantity, expected", [(1, 100), (2, 200), (3, 200), (4, 300), (6, 500), (100, 9900)])
def test_third_free(quantity, expected):
    product = Product("Coffee", 100, 101)
    product.promotion = ThirdOneFreePromotion("Third free")
    assert Store([product]).order([(product, quantity)]) == expected


def test_second_half_price_macbook_example():
    product = Product("MacBook", 1450, 100)
    product.promotion = SecondHalfPricePromotion("Second half price")
    assert Store([product]).order([(product, 50)]) == 71775


def test_non_stocked_discount_and_repeated_orders():
    product = NonStockedProduct("License", 125)
    product.promotion = PercentDiscountPromotion("30% off", 30)
    store = Store([product])
    assert store.order([(product, 2)]) == 175
    assert store.order([(product, 1)]) == 87.5
    assert product.quantity == 0
    assert product.active
    assert "30% off" in str(product)


@pytest.mark.parametrize("percent", [-1, 101])
def test_invalid_percentage(percent):
    with pytest.raises(ValueError):
        PercentDiscountPromotion("Invalid", percent)


def test_product_without_promotion():
    product = Product("Coffee", 50, 10)
    assert product.promotion is None
    assert "Promotion:" not in str(product)
    assert Store([product]).order([(product, 2)]) == 100
