import pandas as pd
from typing import List
from app.core.agents.tools.exceptions import EmptyDataFrameError, DataProcessingError, ColumnNotFoundError


def rename_column(df: pd.DataFrame, old_column_name: str, new_column_name: str) -> pd.DataFrame:
    try:
        if df.empty:
            raise EmptyDataFrameError(operation="column rename")
            
        if not old_column_name:
            raise ColumnNotFoundError(old_column_name, list(df.columns))
        if not new_column_name:
            raise ColumnNotFoundError(new_column_name, list(df.columns))
        if old_column_name not in df.columns:
            raise ColumnNotFoundError(old_column_name, list(df.columns))
            
        if new_column_name in df.columns and new_column_name != old_column_name:
            raise DataProcessingError(
                operation="column rename",
                details="new column name already exists"
            )
            
        df.rename(columns={old_column_name: new_column_name}, inplace=True)
        return df
    except Exception as e:
        if not isinstance(e, (EmptyDataFrameError, DataProcessingError, ColumnNotFoundError)):
            raise DataProcessingError(
                operation="column rename",
                details=f"unexpected error: {str(e)}"
            )
        raise


def replace_value(df: pd.DataFrame, column_name: str, old_value: str, new_value: str) -> pd.DataFrame:
    try:
        if not column_name or not old_value or not new_value:
            raise DataProcessingError(operation="replace value", details="Missing required parameters. Please provide 'column_name', 'old_value', and 'new_value'.")
        
        if column_name not in df.columns:
            raise ColumnNotFoundError(column_name, list(df.columns))
        
        if str(old_value).lower() in ['nan', 'none']:
            mask = df[column_name].isna()
            df.loc[mask, column_name] = new_value
            return df
        
        mask = df[column_name] == old_value
        if not mask.any():
            return df
        df[column_name] = df[column_name].replace(old_value, new_value)
        return df
    except Exception as e:
        if not isinstance(e, (EmptyDataFrameError, DataProcessingError, ColumnNotFoundError)):
            raise DataProcessingError(operation="replace value", details=str(e))
        raise


def add_new_column_from_math_operation(df: pd.DataFrame, column_name: str, operation_type: str, source_columns: List[str]) -> pd.DataFrame:
    if not isinstance(column_name, str) or not column_name:
        raise DataProcessingError(operation="add new column from math operation", details="`column_name` must be a non-empty string.")
    if not isinstance(source_columns, list) or len(source_columns) < 2:
        raise DataProcessingError(operation="add new column from math operation", details="`source_columns` must be a list with at least two columns.")
    
    for col in source_columns:
        if col not in df.columns:
            raise ColumnNotFoundError(col, list(df.columns))

    try:
        if operation_type == "sum":
            df[column_name] = df[source_columns].sum(axis=1)
        elif operation_type == "difference":
            if len(source_columns) != 2:
                raise DataProcessingError(operation="add new column from math operation", details="'difference' operation requires exactly two source columns.")
            df[column_name] = df[source_columns[0]] - df[source_columns[1]]
        elif operation_type == "product":
            df[column_name] = df[source_columns[0]]
            for col in source_columns[1:]:
                df[column_name] *= df[col]
        elif operation_type == "quotient":
            if len(source_columns) != 2:
                raise DataProcessingError(operation="add new column from math operation", details="'quotient' operation requires exactly two source columns.")
            df[column_name] = df[source_columns[0]] / df[source_columns[1]]
        elif operation_type == "mean":
            df[column_name] = df[source_columns].mean(axis=1)
        else:
            raise DataProcessingError(operation="add new column from math operation", details=f"Unsupported operation_type '{operation_type}'. Please use 'sum', 'difference', 'product', 'quotient', or 'mean'.")
    except Exception as e:
        if not isinstance(e, (EmptyDataFrameError, DataProcessingError, ColumnNotFoundError)):
            raise DataProcessingError(operation="add new column from math operation", details=f"An unexpected error occurred during the operation: {e}")
        raise
    return df
