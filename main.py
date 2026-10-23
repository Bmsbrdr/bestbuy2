from products import Product, NonStockedProduct, LimitedProduct
from promotions import SecondHalfPricePromotion, ThirdOneFreePromotion, PercentDiscountPromotion
from store import Store


def make_order(store: Store) -> None:
    products = store.all_products
    if not products:
        print("No products available.")
        return
    shopping_list = []
    while True:
        for index, product in enumerate(products, start=1):
            print(f"{index}. {product}")
        choice = input("Choose a product, or press Enter to finish: ").strip()
        if not choice:
            if not shopping_list:
                print("Shopping cart is empty.")
                return
            try:
                total = store.order(shopping_list)
            except (ValueError, AttributeError) as error:
                print(f"Order failed: {error}")
                return
            print(f"Order complete. Your total is: {total:.2f}\nThanks for visiting Best Buy!")
            return
        try:
            index = int(choice)
            if not 1 <= index <= len(products):
                raise ValueError("Please choose a product from the list")
            product = products[index - 1]
            quantity = int(input("Please enter desired amount of product: "))
            already_added = sum(amount for item, amount in shopping_list if item is product)
            if quantity <= 0:
                raise ValueError("Please enter a positive whole number")
            product.validate_purchase(already_added + quantity)
        except ValueError as error:
            print(f"Cannot add product: {error}")
            continue
        shopping_list.append((product, quantity))
        print(f"Added: {product.name} x {quantity} to shopping cart.\n")


def start(store: Store) -> None:
    while True:
        print("Welcome to Best Buy!\n\n"
              "1. List all products in store\n"
              "2. Show total amount in store\n"
              "3. Make an order\n"
              "4. Quit")
        choice = input("Please enter your choice: ").strip()
        if choice == "1":
            for product in store.all_products:
                print(product)
        elif choice == "2":
            print(f"Total amount of products: {store.total_quantity} pcs.")
        elif choice == "3":
            make_order(store)
        elif choice == "4":
            return
        else:
            print("Please enter a valid choice.")


def create_store() -> Store:
    products = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1),
    ]
    products[0].promotion = SecondHalfPricePromotion("Second Half price!")
    products[1].promotion = ThirdOneFreePromotion("Third One Free!")
    products[3].promotion = PercentDiscountPromotion("30% off!", percent=30)
    return Store(products)


if __name__ == "__main__":
    start(create_store())
