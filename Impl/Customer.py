from .User import User
from .Product import Product
from typing import List, Optional
from Order import Order

class Customer(User):
    def __init__(self, username: str, password: str, email: str):
        super().__init__(username, password, email)
        self.cart = []

    def browse_products(self, products: List['Product']) -> None:
        if not products:
            print("No products available")
            return
        for product in products:
            print(product.get_details())

    def add_to_cart(self, products: List['Product'], product_id: str, quantity: int) -> bool:
        for product in products:
            if product.product_id == product_id and product.stock >= quantity and quantity > 0:
                self.cart.append({"product": product, "quantity": quantity})
                product.update_stock(-quantity)
                print(f"Added {quantity} x {product.name} to cart")
                return True
        print("Invalid product ID or insufficient stock")
        return False

    def place_order(self, orders: List['Order']) -> Optional['Order']:
        if not self.cart:
            print("Cart is empty")
            return None
        order = Order(self, self.cart)
        orders.append(order)
        self.cart = []  # Clear cart after order
        print(f"Order placed: {order.order_id}")
        return order

    def view_order_history(self, orders: List['Order']) -> None:
        user_orders = [order for order in orders if order.customer.user_id == self.user_id]
        if not user_orders:
            print("No orders found")
            return
        for order in user_orders:
            print(order.get_details())