import pytest
from products import Product

@pytest.fixture
def generate_coffee() -> Product:
    return Product("Coffee", 50,100)
def test_product_successful(generate_coffee):
    #Arrange
    target_name = "Coffee"
    target_price = 50
    target_quantity = 100
    #Act
    #Assert
    assert (generate_coffee.price == target_price)
    assert (generate_coffee.quantity == target_quantity)
    assert (generate_coffee.name == target_name)

def test_product_fail():
    with pytest.raises(ValueError):

        Product("Coffee", "abc","cde")
def test_product_empty_fail():
    with pytest.raises(ValueError):
        Product("", 10,100)

def test_product_get_quantity_wrong_type_fail(generate_coffee):
    with pytest.raises(ValueError):
        Product("Coffee", 50,"abc")

def test_product_get_quantity_negative_fail(generate_coffee):
    with pytest.raises(ValueError):
        Product("Coffee", 50, -100)

def test_product_get_price_wrong_type_fail(generate_coffee):
    with pytest.raises(ValueError):
        Product("Coffee", "abc", 100)

def test_product_get_price_negative_fail(generate_coffee):
    with pytest.raises(ValueError):
        Product("Coffee", -50, 100)

def test_product_get_price_zero_fail(generate_coffee):
    with pytest.raises(ValueError):
        Product("Coffee", 0, 100)

def test_product_get_quantity_success(generate_coffee):
    coffee = Product("Coffee", 50, 50)
    target_quantity = 50
    result = coffee.quantity
    assert result == target_quantity

def test_product_get_active_state_success(generate_coffee):
    coffee = Product("Coffee", 50, 100)
    state = True
    result = coffee.active
    assert result == state

def test_product_deactivate_reactivate_success(generate_coffee):
    coffee = Product("Coffee", 50, 100)
    state = False
    coffee.deactivate()
    result = coffee.active
    assert result == state
    state = True
    coffee.activate()
    result = coffee.active
    assert result == state

def test_product_buy_change_quantity(generate_coffee):
    coffee = Product("Coffee", 50, 100)
    assert coffee.quantity == 100
    coffee.buy(50)
    assert coffee.quantity == 50

def test_product_buy_too_much(generate_coffee):
    coffee = Product("Coffee", 50, 100)
    with pytest.raises(ValueError):
        coffee.buy(150)