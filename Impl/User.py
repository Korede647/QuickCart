import uuid
from datetime import datetime

class User:
    def __init__(self, username: str, password: str, email: str):
        self.user_id = str(uuid.uuid4())
        self.username = username
        self._password = password  # Encapsulation
        self.email = email
        self.created_at = datetime.now()

    def login(self, username: str, password: str) -> bool:
        return self.username == username and self._password == password

    def update_profile(self, email: str) -> None:
        self.email = email
        print(f"Profile updated for {self.username}: new email {email}")