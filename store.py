from products import Product, NonStockedProduct
class Store:

    #products = [Product]

    def __init__(self, products: list[Product]):
        self.products = products

    def add_product(self, product: Product):
        self.products.append(product)
    def remove_product(self, product: Product):
        self.products.remove(product)

    def get_total_quantity(self):
        total = 0
        for product in self.products:
            total += product.get_quantity()
        return total

    def get_all_products(self) -> list[Product]:
        result = []
        for product in self.products:
            if product.active:
                result.append(product)
        return result

    def find_product_by_name(self, name: str):
        for product in self.products:
            if product.name == name:
                return product
        raise AttributeError(f"Product {name} has not been added")

    def order(self,shopping_list) -> float:
        stored_enough :bool = False
        total_price :float = 0

        for product, quantity in shopping_list:
            if not any(item.name == product.name for item in self.products):
                raise AttributeError(f"Product {product.name} has not been added")
            target_product = self.find_product_by_name(product.name)
            if isinstance(target_product, NonStockedProduct):
                total_price += target_product.get_total_price(quantity)
                continue
            stored_enough = target_product.quantity > quantity
            if not stored_enough:
                raise ValueError(f"Not Enough {product.name} in stock!")
            total_price += target_product.get_total_price(quantity)
            target_product.quantity -= quantity
        return total_price
