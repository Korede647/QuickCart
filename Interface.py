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


# Customer class


# Rider class


# Product class


# Order class


# Persistence Manager


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