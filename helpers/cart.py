from utils.db import DatabaseConnection
from utils.errors import RecordNotFoundError, ValidationError

class CartManager:
    def __init__(self):
        self.db = DatabaseConnection()

    def add_to_cart(self, crt_id, uid, pid, qty, price, adate):
        if not self.db.record_exists("user", "uid", uid):
            raise RecordNotFoundError("User not found")
        if not self.db.record_exists("product", "pid", pid):
            raise RecordNotFoundError("Product not found")
        
        cart_data = {
            "crt_id": crt_id,
            "uid": uid,
            "pid": pid,
            "qty": qty,
            "price": price,
            "adate": adate
        }
        return self.db.insert_record("cart", cart_data)

    def update_cart_item(self, crt_id, updates):
        return self.db.update_record("cart", updates, "crt_id", crt_id)

    def remove_from_cart(self, crt_id):
        return self.db.remove_record("cart", "crt_id", crt_id)

    def view_cart(self, uid):
        return self.db.fetch_column("cart", ["crt_id", "pid", "qty", "price", "adate"])
