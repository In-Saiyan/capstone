from ..utils.db import DatabaseConnection

class CartManager:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def add_to_cart(self, user_id: str, product_id: str, quantity: int) -> str:
        """Add product to user's cart"""
        pass

    def remove_from_cart(self, user_id: str, product_id: str) -> str:
        """Remove product from cart"""
        pass

    def get_cart_total(self, user_id: str) -> float:
        """Calculate cart total"""
        pass