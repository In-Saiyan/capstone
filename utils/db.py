import pymysql
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

class DatabaseCon:
    def __init__(self):
        # retrieve database info from loaded dotenv
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        
        # connect to database
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def fetch_row(self, table_name: str, pk_id_name: str, row_id: str,):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name} WHERE {pk_id_name} = %s", (row_id,))
            result = cursor.fetchall()
            return [list(row) for row in result]

    def fetch_column(self, table_name: str, column_names: list) -> list:
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT {','.join(column_names)} FROM {table_name}")
            result = cursor.fetchall()
            return [list(row) for row in result]

    def record_exists(self, table_name: str, column_name: str, value: str) -> bool:
        """Check if a certain record exists in the table."""
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT 1 FROM {table_name} WHERE {column_name} = %s LIMIT 1", (value,))
            return cursor.fetchone() is not None

    def insert_record(self, table_name: str, data: dict):
        """Insert a new record into the table."""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        with self.connection.cursor() as cursor:
            if(self.record_exists(table_name, list(data.keys())[0], list(data.values())[0] )):
                return "Not inserted because record exists"
            else :
                cursor.execute(query, values)
                self.connection.commit()

    def update_record(self, table_name: str, data: dict, pk_column = None, pk_value = None):
        pk_column = list(data.keys())[0] if not pk_column else pk_column
        pk_value = list(data.values())[0] if not pk_value else pk_value
        """Update an existing record in the table."""
        set_clause = ', '.join([f"{col} = %s" for col in data.keys()])
        values = tuple(data.values()) + (pk_value,)
        query = f"UPDATE {table_name} SET {set_clause} WHERE {pk_column} = %s"
        
        with self.connection.cursor() as cursor:
            cursor.execute(query, values)
            self.connection.commit()

    def remove_record(self, table_name, pk_column, pk_value):
        """Removes a recrod from the table."""
        query = f"DELETE * FROM TABLE {table_name} WHERE {pk_column}={pk_value}"

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def close_connection(self):
        self.connection.close()
