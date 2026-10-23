from products import Product, NonStockedProduct, LimitedProduct
from promotions import Promotion, SecondHalfPricePromotion, ThirdOneFreePromotion, PercentDiscountPromotion
from store import Store

def start(store: Store):
    while True:
            user_decision = 0
            print("Welcome to Best Buy!\r\n\r\n"
                  "1. List all products in store\r\n"
                  "2. Show total amount in store\r\n"
                  "3. Make an order\r\n"
                  "4. Quit")
            try:
                user_decision = int(float(input("Please enter your choice: ")))
            except ValueError:
                print("Please enter a valid choice.")
            print("\r\n")
            if user_decision == 4:
                break
            all_products = store.get_all_products()

            match user_decision:
                case 1:
                    product_counter = 1
                    for product in all_products:
                        print(product.show())
                        product_counter += 1
                    print("\r\n")
                case 2:
                    print(f"Total Amount of products: {store.get_total_quantity()} pcs.")
                    print("\r\n")
                case 3:
                    list_finished = False
                    shopping_list = []
                    while not list_finished:
                        counter = 1
                        user_desired_product_index = 0
                        user_desired_product_text = ""
                        amount_to_pay = 0
                        limited_product_count = 0

                        for product in all_products:
                            #print(f"{counter}.  Name: {product.name}, Price per unit: {product.price} €,Quantity: {product.quantity} pcs.")
                            print(f"{counter}. {product.show()}")
                            counter += 1
                        print("to finish the order, please send a message without any text.")
                        user_desired_product_text = input("Please enter your choice: ")
                        if user_desired_product_text == "":
                            amount_to_pay = best_buy.order(shopping_list)
                            print("Order complete.\r\n"
                                  f"Your total is: {amount_to_pay} \r\n"
                                  "Thanks for visiting Best Buy!")
                            break
                        try:
                            user_desired_product_index = int(float(user_desired_product_text))
                        except ValueError:

                            print("Please enter a valid number.")
                            continue
                        total_products = len(all_products)
                        if user_desired_product_index < 1 or user_desired_product_index > total_products:
                            print("Please enter a valid choice.")
                            continue
                        target_product = all_products[user_desired_product_index-1]

                        desired_product_amount = int(float(input("Please enter desired amount of product: ")))

                        if isinstance(target_product, LimitedProduct):
                            limited_product_count = sum(quantity for product, quantity in shopping_list if product == target_product)
                            if limited_product_count + desired_product_amount >= target_product.maximum:
                                print(f"\r\nCan't add another {target_product.name}, because it's already in the shopping list and limited to {target_product.maximum} pcs. per order.\r\n")
                                continue

                        shopping_list.append((target_product,desired_product_amount))
                        print(f"\r\nAdded: {target_product.name} x {desired_product_amount} to shopping cart.\r\n")
                        print("\r\n")


# setup initial stock of inventory
product_list = [ Product("MacBook Air M2", price=1450, quantity=100),
                 Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                 Product("Google Pixel 7", price=500, quantity=250),
                 NonStockedProduct("Windows License", price=125),
                 LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
               ]

# Create promotion catalog
second_half_price = SecondHalfPricePromotion("Second Half price!")
third_one_free = ThirdOneFreePromotion("Third One Free!")
thirty_percent = PercentDiscountPromotion("30% off!", percent=30)

# Add promotions to products
product_list[0].promotion = second_half_price
product_list[1].promotion = third_one_free
product_list[3].promotion = thirty_percent


best_buy = Store(product_list)
start(best_buy)
