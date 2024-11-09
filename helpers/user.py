from ..utils.db import DatabaseConnection

class UserManager:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_profile(self, user_data: dict) -> str:
        """Create new user profile"""
        pass

    def update_profile(self, user_id: str, data: dict) -> str:
        """Update user information"""
        pass

    def get_order_history(self, user_id: str) -> list:
        """Get user's order history"""
        pass