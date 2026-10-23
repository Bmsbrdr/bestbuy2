from promotions import Promotion
class Product:
    def __init__(self, name: str, price: float, quantity: int):
        if name == "":
            raise ValueError("Name cannot be empty")
        try :
            self.price = float(price)
        except ValueError:
            raise ValueError("Price must be a number")
        try:
            self.quantity = int(quantity)
        except ValueError:
            raise ValueError("Quantity must be a number")
        if price <= 0:
            raise ValueError("Price cannot be less than 0")
        if quantity < 0:
            raise ValueError("Quantity cannot be less than 0")
        self.name :str = name
        self.price :float= price
        self.quantity :int = quantity
        self.active :bool = True
        self.__promotion: Promotion | None = None
    @property
    def promotion(self) -> Promotion | None:
        return self.__promotion

    @promotion.setter
    def promotion(self, promotion : Promotion):
        self.__promotion = promotion

    def promotion_text(self) -> str:
        return f"Promotion: {self.promotion.name}\r\n" if self.promotion else ""

    def get_total_price(self, quantity: int) -> float:
        total = self.price * quantity
        if self.promotion:
            total -= self.promotion.get_discount(quantity, total)
        return round(total, 2)

    def get_quantity(self) -> int:
        return self.quantity
    def set_quantity(self, quantity):
        self.quantity = quantity

    def activate(self):
        self.active = True
    def deactivate(self):
        self.active = False
    def is_active(self) -> bool:
        return self.active
    # Show's all important data about the product, including name, price and quantity.
    def show(self) -> str:
        return f"Product: {self.name}\r\nPrice per unit: {self.price}\r\nQuantity:{self.quantity}\r\n" + self.promotion_text()

    def check_stock(self, desired_quantity):
        current_quantity = self.get_quantity()
        return (current_quantity - desired_quantity) > 0

    # function which handles the buying process, including substraction of the total amount. It also prints out the
    # amount left and the total price of this transaction.
    def buy(self, quantity: float) -> tuple[str,float]:
        if quantity <= 0:
            raise ValueError("Quantity is less than 0")
        if not self.check_stock(quantity):
            raise ValueError("Cannot buy more than quantity")

        total_left = self.quantity - quantity
        self.set_quantity(total_left)
        total_price = self.get_total_price(quantity)
        return_text = (f"{quantity} items of {self.name} cost {total_price}"
                        f"\r\nCompleting the deal..."
                        f"\r\nThere are still {total_left} items left"
                        f"\r\nThanks for your purchase!\r\n")
        return return_text, total_price
class NonStockedProduct(Product):
    def __init__(self, name: str,price: float):
        super().__init__(name, price,0)
    def show(self) -> str:
        return f"**** Non Stocked Product ****\r\nProduct: {self.name}\r\nPrice per unit: {self.price}\r\n" + self.promotion_text()

class LimitedProduct(Product):
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        self.maximum = maximum
        super().__init__(name, price, quantity)
    def show(self) -> str:
        return f"**** Limited Product (Max 1 per order) ****\r\nProduct: {self.name}\r\nPrice per unit: {self.price}\r\nQuantity:{self.quantity}\r\n" + self.promotion_text()
