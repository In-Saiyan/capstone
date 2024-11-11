from utils.db import DatabaseConnection
from utils.errors import RecordNotFoundError

class SearchManager:
    def __init__(self, db: DatabaseConnection = None):
        
        self.db = DatabaseConnection() if not db else db

    def search_products_by_name(self, name):
        query = "SELECT * FROM product WHERE pname LIKE %s"
        with self.db.connection.cursor() as cursor:
            cursor.execute(query, (f"%{name}%",))
            result = cursor.fetchall()
            return [list(row) for row in result]

    def search_products_by_category(self, cid):
        return self.db.fetch_column("product", ["cid"])

    def search_products_by_price_range(self, min_price, max_price):
        return self.db.filtered_search_record("product", "price", min_price, max_price)
