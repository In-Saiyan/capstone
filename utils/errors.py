class DatabaseError(Exception):
    def __init__(self, message="A database error occurred"):
        super().__init__(message)


class OutOfStockError(Exception):
    def __init__(self, message="The requested quantity exceeds available stock"):
        super().__init__(message)


class OrderError(Exception):
    def __init__(self, message="An error occurred while processing the order"):
        super().__init__(message)


class RecordNotFoundError(DatabaseError):
    def __init__(self, message="The requested record was not found in the database"):
        super().__init__(message)


class ValidationError(Exception):
    def __init__(self, message="Data validation failed"):
        super().__init__(message)
