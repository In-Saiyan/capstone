from utils.db import DatabaseConnection
from utils.errors import OutOfStockError, OrderError

class OrderManager:
    def __init__(self):
        self.db = DatabaseConnection()

    def place_order(self, oid, uid, pid, odate, qty, tprice):
        
        try:
            # Check stock availability for the product
            product = self.db.fetch_row("product", "pid", pid)
            if not product:
                raise OrderError("Product not found")

            current_stock = product[0][4]  

            if qty > current_stock:
                raise OutOfStockError("Insufficient stock available")

            # Insert the order
            order_data = {
                "oid": oid,
                "uid": uid,
                "pid": pid,
                "odate": odate,
                "qty": qty,
                "tprice": tprice
            }
            order_result = self.db.insert_record("orders", order_data)

            # Update product stock
            updated_stock = current_stock - qty
            self.db.update_record("product", {"stock": updated_stock}, "pid", pid)
            
            return order_result
        except OutOfStockError as e:
            return f"Order failed: {e}"
        except Exception as e:
            raise OrderError(f"Order processing error: {e}")

    def get_order_by_id(self, oid):
        return self.db.fetch_row("orders", "oid", oid)

    def update_order(self, oid, updates):
        return self.db.update_record("orders", updates, "oid", oid)

    def delete_order(self, oid):
        return self.db.remove_record("orders", "oid", oid)

    def list_user_orders(self, uid):
        return self.db.fetch_column("orders", ["oid", "pid", "odate", "qty", "tprice"], uid)
