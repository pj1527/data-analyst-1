from typing import List, Optional, Any
from pydantic import BaseModel


class DataFrameColumn(BaseModel):
    column_name: str
    is_categorical: bool
    unique_values: Optional[List[Any]] = None


class DataFrameColumnList(BaseModel):
    columns: List[DataFrameColumn]


class CategoricalValue(BaseModel):
    value: str
    count: int
    percentage: float


class DataFrameColumnDetailedInformation(DataFrameColumn):
    value_details: Optional[List[CategoricalValue]] = None


class DataFrameColumnNames(BaseModel):
    column_names: List[str]


class DataFrameColumnSampleValues(BaseModel):
    column_name: str
    sample_values: List[Any]


class DataFrameColumnSampleValuesList(BaseModel):
    columns: List[DataFrameColumnSampleValues]
