import pandas as pd
from app.core.agents.tools.types import DataFrameColumnNames, DataFrameColumn, DataFrameColumnList, DataFrameColumnDetailedInformation, CategoricalValue, DataFrameColumnSampleValues, DataFrameColumnSampleValuesList
from app.core.agents.tools.exceptions import EmptyDataFrameError, DataProcessingError, ColumnNotFoundError


def get_column_names(df: pd.DataFrame) -> DataFrameColumnNames:
    if df.empty:
        raise EmptyDataFrameError(operation="get column names")
    return DataFrameColumnNames(column_names=list(df.columns))


def get_categorical_and_continuous_information(df: pd.DataFrame) -> DataFrameColumnList:
    if df.empty:
        raise EmptyDataFrameError(operation="categorical and continuous info analysis")
        
    columns_info = DataFrameColumnList(columns=[])
    num_rows = len(df)

    for col in df.columns:
        try:
            unique_values = df[col].dropna().unique().tolist()
            num_unique = len(unique_values)

            # Heuristic: A column is categorical if it has a low number of unique values
            is_categorical = (num_unique / num_rows < 0.1) if num_rows > 0 else False
            
            if is_categorical:
                columns_info.columns.append(DataFrameColumn(
                    column_name=col,
                    unique_values=unique_values,
                    is_categorical=is_categorical
                ))
            else:
                columns_info.columns.append(DataFrameColumn(
                    column_name=col,
                    is_categorical=is_categorical
                ))
        except Exception as e:
            raise DataProcessingError(operation="column analysis", details=f"Error processing column '{col}': {str(e)}")
    return columns_info


def get_column_detailed_information(df: pd.DataFrame, column_name: str) -> DataFrameColumnDetailedInformation:
    try:
        if df.empty:
            raise EmptyDataFrameError(operation="unique values analysis")
            
        if not column_name:
            raise ColumnNotFoundError(column_name="", available_columns=list(df.columns))
            
        if column_name not in df.columns:
            raise ColumnNotFoundError(column_name, list(df.columns))
        
        value_counts = df[column_name].value_counts(dropna=False)
        total = len(df)
        
        column_detailed_info = DataFrameColumnDetailedInformation(
            column_name=column_name,
            is_categorical=True,
            unique_values=value_counts.index.tolist(),
            value_details=[]
        )
        
        for value, count in value_counts.items():
            value_str = str(value) if pd.notna(value) else "<MISSING>"
            percentage = (count / total) * 100
            column_detailed_info.value_details.append(CategoricalValue(
                value=value_str,
                count=int(count),
                percentage=round(percentage, 1)
            ))
        
        return column_detailed_info
        
    except Exception as e:
        if not isinstance(e, (EmptyDataFrameError, ColumnNotFoundError, DataProcessingError)):
            raise DataProcessingError(operation="unique values analysis", details=str(e))
        raise


def get_column_sample_values(df: pd.DataFrame, num_samples: int = 5) -> DataFrameColumnSampleValuesList:
    try:
        if df.empty:
            raise EmptyDataFrameError(operation="column sample values")
        sample_values = DataFrameColumnSampleValuesList(columns=[])
        for column_name in df.columns:
            sample_values.columns.append(
                DataFrameColumnSampleValues(
                    column_name=column_name,
                    sample_values=df[column_name].sample(num_samples, random_state=42).tolist()
                )
            )
        return sample_values
    except Exception as e:
        if not isinstance(e, (EmptyDataFrameError, DataProcessingError)):
            raise DataProcessingError(operation="column sample values", details=str(e))
        raise
