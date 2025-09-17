
from Admin import Admin
from models import Customer
from Rider import Rider
from Manager import PersistenceManager
from OrderStatus import OrderStatus
from RiderStatus import RiderStatus
from User import User

class QuickCartApp:
    def __init__(self):
        self.products = PersistenceManager.load_products()
        self.orders = []
        self.users = {
            "admin": Admin("adminKorede", "admin123", "admin@quickcart.com"),
            "customer1": Customer("customer1", "customer123", "customer1@quickcart.com"),
            "rider1": Rider("rider1", "rider123", "rider1@quickcart.com")
        }

    def run(self):
        while True:
            print("\n================================================ QuickCart =========================================================")
            print("Welcome to QuickCart!\nPlease Login to Continue")
            print("1. Admin?")
            print("2. Customer?")
            print("3. Rider?")
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

if __name__ == "__main__":
    app = QuickCartApp()
    app.run()