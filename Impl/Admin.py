from .User import User
from .Product import Product
from IQuickCart.Order import Order
from typing import List

class Admin(User):
    def add_product(self, products: List['Product'], name: str, price: float, stock: int, category: str) -> 'Product':
        product = Product(name, price, stock, category)
        products.append(product)
        print(f"Added product: {name}")
        return product

    def restock_product(self, products: List['Product'], product_id: str, quantity: int) -> bool:
        for product in products:
            if product.product_id == product_id and quantity > 0:
                product.update_stock(quantity)
                print(f"Restocked {product.name} with {quantity} units")
                return True
        print("Invalid product ID or quantity")
        return False

    def view_all_orders(self, orders: List['Order']) -> None:
        if not orders:
            print("No orders found")
            return
        for order in orders:
            print(order.get_details())