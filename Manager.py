from typing import List
import json
from Impl.Product import Product
from IQuickCart.Order import Order
import os
# import Order

class PersistenceManager:
    @staticmethod
    def save_data(products: List[Product], orders: List[Order], filename: str = "quickcart_data.json") -> None:
        data = {
            "products": [product.get_details() for product in products],
            "orders": [order.get_details() for order in orders]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load_products(filename: str = "quickcart_data.json") -> List[Product]:
        if not os.path.exists(filename):
            return []
        with open(filename, 'r') as f:
            data = json.load(f)
            return [Product(p["name"], p["price"], p["stock"], p["category"]) for p in data.get("products", [])]