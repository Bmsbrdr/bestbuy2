import pytest

from products import LimitedProduct, NonStockedProduct, Product
from store import Store


@pytest.mark.parametrize("price", [-100, 0, float("nan"), float("inf"), None, True])
def test_price_property_rejects_invalid_update(price):
    mac = Product("MacBook Air M2", 1450, 100)
    with pytest.raises(ValueError):
        mac.price = price
    assert mac.price == 1450


def test_properties_validate_assignments():
    mac = Product("MacBook Air M2", 1450, 100)
    mac.price = 1200
    assert mac.price == 1200
    with pytest.raises(ValueError):
        mac.quantity = -1
    assert mac.quantity == 100
    with pytest.raises(ValueError):
        mac.name = " "
    assert mac.name == "MacBook Air M2"
    mac.quantity = 0
    assert not mac.active


def test_print_product(capsys):
    mac = Product("MacBook Air M2", 1450, 100)
    print(mac)
    assert capsys.readouterr().out == "MacBook Air M2, Price: $1450 Quantity:100\n"
    assert "Max 1 per order" in str(LimitedProduct("Pixel", 500, 250, 1))
    assert "Non Stocked Product" in str(NonStockedProduct("License", 125))


def test_comparison_uses_price_without_changing_identity():
    mac = Product("MacBook", 1450, 100)
    bose = Product("Bose", 250, 500)
    same_price = Product("Other", 1450, 1)
    assert mac > bose
    assert bose < mac
    assert not mac < same_price
    assert not mac > same_price
    assert mac != same_price
    with pytest.raises(TypeError):
        mac > 100


def test_contains_checks_actual_product_even_if_inactive():
    mac = Product("MacBook", 1450, 100)
    other_mac = Product("MacBook", 1450, 100)
    store = Store([mac])
    mac.deactivate()
    assert mac in store
    assert other_mac not in store
    assert "MacBook" not in store
    assert store.all_products == []
    assert store.total_quantity == 100


def test_add_stores_creates_independent_list_with_original_products():
    mac = Product("MacBook", 1450, 100)
    bose = Product("Bose", 250, 500)
    first, second = Store([mac]), Store([bose])
    combined = first + second
    assert combined is not first and combined is not second
    assert combined.products == [mac, bose]
    assert combined.products[0] is mac
    combined.remove_product(mac)
    assert first.products == [mac]
    assert second.products == [bose]
    with pytest.raises(TypeError):
        first + [bose]
