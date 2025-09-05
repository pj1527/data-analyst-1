class DataFrameError(Exception):
    """Base exception for all DataFrame-related errors."""
    pass


class EmptyDataFrameError(DataFrameError):
    """Raised when an operation is performed on an empty DataFrame."""
    def __init__(self, operation: str):
        super().__init__(f"Cannot perform {operation} on an empty DataFrame")


class DataProcessingError(DataFrameError):
    """Raised when there's an error during data processing."""
    def __init__(self, operation: str, details: str):
        super().__init__(f"Error during {operation}: {details}")


class ColumnNotFoundError(DataFrameError):
    """Raised when a specified column is not found in the DataFrame."""
    def __init__(self, column_name: str, available_columns: list):
        available = ", ".join(available_columns)
        super().__init__(
            f"Column '{column_name}' not found. Available columns: {available}"
        )
