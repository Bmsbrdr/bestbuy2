class Product:
    def __init__(self, name: str, price: float, quantity: int):
        if name is "":
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
    def show(self):
        print(f"Product: {self.name}\r\nPrice per unit: {self.price}\r\nQuantity:{self.quantity}\r\n")

    def check_stock(self, desired_quantity):
        current_quantity = self.get_quantity()
        return (current_quantity - desired_quantity) > 0

    # function which handles the buying process, including substraction of the total amount. It also prints out the
    # amount left and the total price of this transaction.
    def buy(self, quantity: float) -> float:
        if quantity <= 0:
            raise ValueError("Quantity is less than 0")
        if not self.check_stock(quantity):
            raise ValueError("Cannot buy more than quantity")

        total_left = self.quantity - quantity
        self.set_quantity(total_left)
        total_price = self.price * quantity
        print (f"{quantity} items of {self.name} cost {total_price}"
               f"\r\nCompleting the deal..."
               f"\r\nThere are still {total_left} items left"
               f"\r\nThanks for your purchase!\r\n")
        return total_price
