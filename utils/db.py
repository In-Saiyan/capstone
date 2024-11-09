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

    def fetch_row(self, table_name:str, row_id:str, pk_id_name:str):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name} WHERE {pk_id_name} = %s", (row_id,))
            result = cursor.fetchall()
            return [list(row) for row in result]
        
    # # table specific fetch [deprecated]
    # def fetch_user_row(self, table_name: str, row_id: str):
    #     with self.connection.cursor() as cursor:
    #         cursor.execute(f"SELECT * FROM {table_name} WHERE uid = %s", (row_id,))
    #         result = cursor.fetchall()
    #         return [list(row) for row in result]

    def fetch_column(self, table_name: str, column_names: list) -> list:
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT {",".join(column_names)} FROM {table_name}")
            result = cursor.fetchall()
            return [list(row) for row in result]

    def close_connection(self):
        self.connection.close()
