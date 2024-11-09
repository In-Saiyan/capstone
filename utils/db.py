import pymysql
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

class DatabaseConnection:
    """
    A class to handle MySQL/MariaDB database connections and operations.
    Uses environment variables for database configuration from python-dotenv.
    """
    
    def __init__(self):
        """
        Initialize database connection using environment variables.
        Required environment variables: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
        """
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

    def fetch_table(self, table_name: str) -> list:
        """
        Fetch all records from a specified table.

        Args:
            table_name (str): Name of the table to query

        Returns:
            list: List of lists where each inner list represents a row from the table
        """
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            result = cursor.fetchall()
            return [list(row) for row in result]

    def fetch_row(self, table_name: str, pk_id_name: str, row_id: str) -> list:
        """
        Fetch a specific row from a table using primary key.

        Args:
            table_name (str): Name of the table to query
            pk_id_name (str): Name of the primary key column
            row_id (str): Value of the primary key to search for

        Returns:
            list: List containing the requested row data
        """
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name} WHERE {pk_id_name} = %s", (row_id,))
            result = cursor.fetchall()
            return [list(row) for row in result]

    def fetch_column(self, table_name: str, column_names: list) -> list:
        """
        Fetch specific columns from a table.

        Args:
            table_name (str): Name of the table to query
            column_names (list): List of column names to retrieve

        Returns:
            list: List of lists where each inner list contains the specified column values
        """
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT {','.join(column_names)} FROM {table_name}")
            result = cursor.fetchall()
            return [list(row) for row in result]

    def record_exists(self, table_name: str, column_name: str, value: str) -> bool:
        """
        Check if a record exists in the specified table.

        Args:
            table_name (str): Name of the table to check
            column_name (str): Name of the column to check
            value (str): Value to search for in the specified column

        Returns:
            bool: True if record exists, False otherwise
        """
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT 1 FROM {table_name} WHERE {column_name} = %s LIMIT 1", (value,))
            return cursor.fetchone() is not None

    def insert_record(self, table_name: str, data: dict) -> str:
        """
        Insert a new record into the table if it doesn't already exist.

        Args:
            table_name (str): Name of the table to insert into
            data (dict): Dictionary containing column names as keys and values to insert

        Returns:
            str: Message indicating success or if record already exists
        
        Example:
            insert_record('users', {'id': '1', 'name': 'John', 'email': 'john@example.com'})
        """
        if self.record_exists(table_name, list(data.keys())[0], list(data.values())[0]):
            return "Not inserted because record already exists"
            
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        with self.connection.cursor() as cursor:
            print(query)
            cursor.execute(query, values)
            self.connection.commit()
            return "Record inserted successfully"

    def update_record(self, table_name: str, data: dict, pk_column: str = None, pk_value: str = None) -> str:
        """
        Update an existing record in the table.

        Args:
            table_name (str): Name of the table to update
            data (dict): Dictionary containing column names and new values
            pk_column (str, optional): Primary key column name. Defaults to first key in data dict
            pk_value (str, optional): Primary key value. Defaults to first value in data dict

        Returns:
            str: Message indicating success or failure of update operation
        
        Example:
            update_record('users', {'name': 'John Doe'}, 'id', '1')
        """
        pk_column = list(data.keys())[0] if not pk_column else pk_column
        pk_value = list(data.values())[0] if not pk_value else pk_value

        if not self.record_exists(table_name, pk_column, pk_value):
            return "Update failed: Record does not exist"
            
        set_clause = ', '.join([f"{col} = %s" for col in data.keys()])
        values = tuple(data.values()) + (pk_value,)
        query = f"UPDATE {table_name} SET {set_clause} WHERE {pk_column} = %s"
        
        with self.connection.cursor() as cursor:
            cursor.execute(query, values)
            self.connection.commit()
            return "Record updated successfully"

    def remove_record(self, table_name: str, pk_column: str, pk_value: any) -> str:
        """
        Remove a record from the table if it exists.

        Args:
            table_name (str): Name of the table to delete from
            pk_column (str): Name of the primary key column
            pk_value (any): Value of the primary key for the record to delete

        Returns:
            str: Message indicating success or failure of deletion

        Raises:
            Exception: If database operation fails
        
        Example:
            remove_record('users', 'id', '1')
        """
        if not self.record_exists(table_name, pk_column, pk_value):
            return "Delete failed: Record does not exist"
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM {table_name} WHERE {pk_column}=%s",
                    (pk_value,)
                )
                self.connection.commit()
                return "Record deleted successfully"
        except pymysql.Error as e:
            self.connection.rollback()
            raise Exception(f"Failed to delete record: {e}")

    def close_connection(self):
        """
        Close the database connection.
        Should be called when done with database operations.
        """
        self.connection.close()



"""
Code by Aryan Singh LIT2024021.
"""