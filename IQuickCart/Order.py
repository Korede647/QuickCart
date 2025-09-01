from Impl.Customer import Customer
import uuid
from ENUMS import OrderStatus
from typing import List, Dict
from datetime import datetime

class Order:
    def __init__(self, customer: Customer, cart: List[Dict]):
        self.order_id = str(uuid.uuid4())
        self.customer = customer
        self.rider = None
        self.products = cart
        self.status = OrderStatus.PENDING
        self.order_time = datetime.now()
        self.total_amount = self.calculate_total()

    def calculate_total(self) -> float:
        return sum(item["product"].price * item["quantity"] for item in self.products)

    def update_status(self, status: OrderStatus) -> None:
        self.status = status

    def get_details(self) -> Dict:
        return {
            "order_id": self.order_id,
            "customer": self.customer.username,
            "rider": self.rider.username if self.rider else "Unassigned",
            "products": [{"name": item["product"].name, "quantity": item["quantity"]} for item in self.products],
            "status": self.status.value,
            "total_amount": self.total_amount,
            "order_time": self.order_time.strftime("%Y-%m-%d %H:%M:%S")
        }