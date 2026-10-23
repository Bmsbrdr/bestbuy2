import math

from promotions import Promotion


def validate_quantity(quantity: int, *, allow_zero: bool = False) -> None:
    minimum = 0 if allow_zero else 1
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < minimum:
        raise ValueError(f"Quantity must be a whole number of at least {minimum}")


class Product:
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.active = True
        self.quantity = quantity
        self.__promotion: Promotion | None = None

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name cannot be empty")
        self.__name = name

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, price: float):
        try:
            converted_price = float(price)
        except (ValueError, TypeError):
            raise ValueError("Price must be a number") from None
        if isinstance(price, bool) or not math.isfinite(converted_price) or converted_price <= 0:
            raise ValueError("Price must be a positive finite number")
        self.__price = converted_price

    @property
    def quantity(self) -> int:
        return self.__quantity

    @quantity.setter
    def quantity(self, quantity: int):
        validate_quantity(quantity, allow_zero=True)
        self.__quantity = quantity
        if quantity == 0:
            self.deactivate()

    @property
    def promotion(self) -> Promotion | None:
        return self.__promotion

    @promotion.setter
    def promotion(self, promotion: Promotion | None):
        if promotion is not None and not isinstance(promotion, Promotion):
            raise ValueError("Promotion must be a Promotion or None")
        self.__promotion = promotion

    def promotion_text(self) -> str:
        return f"Promotion: {self.promotion.name}\n" if self.promotion else ""

    def get_total_price(self, quantity: int) -> float:
        validate_quantity(quantity)
        total = self.price * quantity
        if self.promotion:
            total -= self.promotion.get_discount(quantity, total)
        return round(total, 2)

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def __str__(self) -> str:
        text = f"{self.name}, Price: ${self.price:g} Quantity:{self.quantity}"
        return text + (f"\n{self.promotion_text().rstrip()}" if self.promotion else "")

    def __lt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price

    def __gt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.price > other.price

    def check_stock(self, desired_quantity: int) -> bool:
        return desired_quantity <= self.quantity

    def validate_purchase(self, quantity: int) -> None:
        validate_quantity(quantity)
        if not self.active:
            raise ValueError(f"Product {self.name} is inactive")
        if not self.check_stock(quantity):
            raise ValueError(f"Not enough {self.name} in stock")

    def buy(self, quantity: int) -> tuple[str, float]:
        self.validate_purchase(quantity)
        total_price = self.get_total_price(quantity)
        self.quantity -= quantity
        return (f"{quantity} items of {self.name} cost {total_price:.2f}\n"
                f"There are still {self.quantity} items left\n"
                "Thanks for your purchase!\n", total_price)


class NonStockedProduct(Product):
    def __init__(self, name: str, price: float):
        super().__init__(name, price, 0)
        self.activate()

    def check_stock(self, desired_quantity: int) -> bool:
        return True

    def buy(self, quantity: int) -> tuple[str, float]:
        self.validate_purchase(quantity)
        total_price = self.get_total_price(quantity)
        return (f"{quantity} items of {self.name} cost {total_price:.2f}\n"
                "Thanks for your purchase!\n", total_price)

    def __str__(self) -> str:
        text = f"{self.name}, Price: ${self.price:g} (Non Stocked Product)"
        return text + (f"\n{self.promotion_text().rstrip()}" if self.promotion else "")


class LimitedProduct(Product):
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        validate_quantity(maximum)
        self.maximum = maximum
        super().__init__(name, price, quantity)

    def validate_purchase(self, quantity: int) -> None:
        super().validate_purchase(quantity)
        if quantity > self.maximum:
            raise ValueError(f"Maximum {self.maximum} {self.name} per order")

    def __str__(self) -> str:
        return f"{super().__str__()} (Max {self.maximum} per order)"
