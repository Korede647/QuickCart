import uuid
from typing import Dict

class Product:
    def __init__(self, name: str, price: float, stock: int, category: str):
        self.product_id = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category

    def update_stock(self, quantity: int) -> None:
        self.stock += quantity

    def get_details(self) -> Dict:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "category": self.category
        }