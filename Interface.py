#  QuickCart is a console-based Minimum Viable Product (MVP) for an ultra-fast micro-delivery
#  platform. It simulates a simplified version of services like GoPuff or Glovo, with three roles: Admin,
#  User, Rider. This MVP allows customers to register and place orders, riders to accept and deliver
#  orders, and admins to manage products and monitor activity.
#  2. Purpose & Scope
#  The project consolidates Python knowledge in OOP, file handling, and data structures. Scope:
#  authentication, product management, order placement, rider workflow, and admin oversight.
#  3. Users & Roles- Admin: Add products, restock, view orders. - User: Register, login, browse products, place orders,
#  view history. - Rider: Accept pending orders, update delivery status.
#  4. Functional Requirements
#  Key modules include: - User authentication & registration. - Product catalog management (add,
#  restock, list). - Order creation and validation. - Rider assignment and status updates. - Admin order
#  monitoring.
#  5. Non-Functional Requirements
#  Menus must be user-friendly, with error handling for invalid inputs. OOP design with encapsulation,
#  inheritance, and enums is required. Optional persistence via JSON can be added as an advanced
#  feature.
#  6. Acceptance Criteria
#  Role-specific menus, safe stock handling, valid order status transitions, users see only their own
#  orders, riders manage only their assigned orders, admins have full oversight. The app must not
#  crash on invalid input


import uuid
import json
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional
import os

# Enums for order and rider status




# Abstract base class for users


# Admin class
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

# Customer class
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

# Rider class
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

# Product class
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

# Order class
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

# Persistence Manager
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

# Main console application
class QuickCartApp:
    def __init__(self):
        self.products = PersistenceManager.load_products()
        self.orders = []
        self.users = {
            "admin": Admin("admin", "admin123", "admin@quickcart.com"),
            "customer1": Customer("customer1", "pass123", "customer1@quickcart.com"),
            "rider1": Rider("rider1", "pass123", "rider1@quickcart.com")
        }

    def run(self):
        while True:
            print("\n=== QuickCart ===")
            print("1. Admin Login")
            print("2. Customer Login")
            print("3. Rider Login")
            print("4. Exit")
            choice = input("Select option: ")

            if choice == "1":
                self.admin_menu()
            elif choice == "2":
                self.customer_menu()
            elif choice == "3":
                self.rider_menu()
            elif choice == "4":
                PersistenceManager.save_data(self.products, self.orders)
                print("Exiting QuickCart...")
                break
            else:
                print("Invalid choice")

    def admin_menu(self):
        admin = self.users.get("admin")
        if not self.authenticate(admin):
            return
        while True:
            print("\n=== Admin Menu ===")
            print("1. Add Product")
            print("2. Restock Product")
            print("3. View All Orders")
            print("4. Logout")
            choice = input("Select option: ")

            if choice == "1":
                name = input("Product name: ")
                try:
                    price = float(input("Price: "))
                    stock = int(input("Stock: "))
                    category = input("Category: ")
                    admin.add_product(self.products, name, price, stock, category)
                except ValueError:
                    print("Invalid price or stock")
            elif choice == "2":
                product_id = input("Product ID: ")
                try:
                    quantity = int(input("Quantity to restock: "))
                    admin.restock_product(self.products, product_id, quantity)
                except ValueError:
                    print("Invalid quantity")
            elif choice == "3":
                admin.view_all_orders(self.orders)
            elif choice == "4":
                break
            else:
                print("Invalid choice")

    def customer_menu(self):
        customer = self.users.get("customer1")
        if not self.authenticate(customer):
            return
        while True:
            print("\n=== Customer Menu ===")
            print("1. Browse Products")
            print("2. Add to Cart")
            print("3. Place Order")
            print("4. View Order History")
            print("5. Logout")
            choice = input("Select option: ")

            if choice == "1":
                customer.browse_products(self.products)
            elif choice == "2":
                product_id = input("Product ID: ")
                try:
                    quantity = int(input("Quantity: "))
                    customer.add_to_cart(self.products, product_id, quantity)
                except ValueError:
                    print("Invalid quantity")
            elif choice == "3":
                customer.place_order(self.orders)
            elif choice == "4":
                customer.view_order_history(self.orders)
            elif choice == "5":
                break
            else:
                print("Invalid choice")

    def rider_menu(self):
        rider = self.users.get("rider1")
        if not self.authenticate(rider):
            return
        while True:
            print("\n=== Rider Menu ===")
            print("1. Set Availability")
            print("2. View Pending Orders")
            print("3. Accept Order")
            print("4. Update Delivery Status")
            print("5. Logout")
            choice = input("Select option: ")

            if choice == "1":
                print("Available statuses: available, busy, offline")
                status = input("Enter status: ")
                try:
                    rider.set_availability(RiderStatus(status))
                except ValueError:
                    print("Invalid status")
            elif choice == "2":
                rider.view_pending_orders(self.orders)
            elif choice == "3":
                order_id = input("Order ID: ")
                rider.accept_order(self.orders, order_id)
            elif choice == "4":
                order_id = input("Order ID: ")
                print("Valid statuses: in_progress, delivered, cancelled")
                status = input("Enter status: ")
                try:
                    rider.update_delivery_status(self.orders, order_id, OrderStatus(status))
                except ValueError:
                    print("Invalid status")
            elif choice == "5":
                break
            else:
                print("Invalid choice")

    def authenticate(self, user: User) -> bool:
        username = input("Username: ")
        password = input("Password: ")
        if user.login(username, password):
            print(f"Welcome, {username}!")
            return True
        print("Invalid credentials")
        return False

# Run the application
if __name__ == "__main__":
    app = QuickCartApp()
    app.run()