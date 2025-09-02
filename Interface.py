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


# Run the application
if __name__ == "__main__":
    app = QuickCartApp()
    app.run()