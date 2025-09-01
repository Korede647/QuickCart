from IQuickCart.User import User
from IQuickCart.Order import Order
from ENUMS import OrderStatus
from ENUMS import RiderStatus
from typing import List 

class Rider(User):
    def __init__(self, username: str, password: str, email: str):
        super().__init__(username, password, email)
        self.status = RiderStatus.OFFLINE

    def set_availability(self, status: RiderStatus) -> None:
        self.status = status
        print(f"Rider {self.username} status updated to {status.value}")

    def view_pending_orders(self, orders: List['Order']) -> None:
        pending_orders = [order for order in orders if order.status == OrderStatus.PENDING]
        if not pending_orders:
            print("No pending orders")
            return
        for order in pending_orders:
            print(order.get_details())

    def accept_order(self, orders: List['Order'], order_id: str) -> bool:
        if self.status != RiderStatus.AVAILABLE:
            print("Rider must be available to accept orders")
            return False
        for order in orders:
            if order.order_id == order_id and order.status == OrderStatus.PENDING:
                order.rider = self
                order.update_status(OrderStatus.ACCEPTED)
                self.status = RiderStatus.BUSY
                print(f"Order {order_id} accepted by {self.username}")
                return True
        print("Invalid order ID or order not pending")
        return False

    def update_delivery_status(self, orders: List['Order'], order_id: str, status: OrderStatus) -> bool:
        valid_transitions = {
            OrderStatus.ACCEPTED: [OrderStatus.IN_PROGRESS, OrderStatus.CANCELLED],
            OrderStatus.IN_PROGRESS: [OrderStatus.DELIVERED, OrderStatus.CANCELLED]
        }
        for order in orders:
            if order.order_id == order_id and order.rider == self:
                if status in valid_transitions.get(order.status, []):
                    order.update_status(status)
                    if status == OrderStatus.DELIVERED:
                        self.status = RiderStatus.AVAILABLE
                    print(f"Order {order_id} status updated to {status.value}")
                    return True
                print("Invalid status transition")
                return False
        print("Invalid order ID or not assigned to rider")
        return False