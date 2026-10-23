from products import Product, validate_quantity


class Store:
    def __init__(self, products: list[Product]):
        self.products = list(products)

    def add_product(self, product: Product):
        self.products.append(product)

    def remove_product(self, product: Product):
        self.products.remove(product)

    @property
    def total_quantity(self) -> int:
        return sum(product.quantity for product in self.products)

    @property
    def all_products(self) -> list[Product]:
        return [product for product in self.products if product.active]

    def __contains__(self, product: object) -> bool:
        return product in self.products

    def __add__(self, other):
        if not isinstance(other, Store):
            return NotImplemented
        return Store(self.products + other.products)

    def find_product_by_name(self, name: str) -> Product:
        for product in self.products:
            if product.name == name:
                return product
        raise AttributeError(f"Product {name} has not been added")

    def order(self, shopping_list: list[tuple[Product, int]]) -> float:
        quantities: dict[Product, int] = {}
        for product, quantity in shopping_list:
            validate_quantity(quantity)
            target = self.find_product_by_name(product.name)
            quantities[target] = quantities.get(target, 0) + quantity

        # Check every line, including its price, before changing any stock.
        for product, quantity in quantities.items():
            product.validate_purchase(quantity)
        total = round(sum(product.get_total_price(quantity)
                          for product, quantity in quantities.items()), 2)
        for product, quantity in quantities.items():
            product.buy(quantity)
        return total
