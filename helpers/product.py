from utils.db import DatabaseConnection

class ProductManager:
    def __init__(self, db: DatabaseConnection = None):
        
        self.db = DatabaseConnection() if not db else db

    def add_product(self, pid, pname, cid, price, stock, adate, imgurl = None):
        data = {
            "pid": pid,
            "pname": pname,
            "cid": cid,
            "price": price,
            "stock": stock,
            "adate": adate,
            "imgurl":imgurl,
        }
        return self.db.insert_record("product", data)

    def get_product_by_id(self, pid):
        return self.db.fetch_row("product", "pid", pid)

    def update_product(self, pid, updates):
        return self.db.update_record("product", updates, "pid", pid)

    def delete_product(self, pid):
        return self.db.remove_record("product", "pid", pid)

    def list_all_products(self):
        return self.db.fetch_table("product")


"""Code made by Aryan Singh LIT2024021"""
