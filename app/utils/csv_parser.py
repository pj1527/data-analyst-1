import pandas as pd


def read_csv_into_df(file_path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise Exception(f"Error reading file: {e}")


def save_df_to_csv(df: pd.DataFrame, file_path: str) -> None:
    try:
        df.to_csv(file_path, index=False)
    except Exception as e:
        raise Exception(f"Error saving DataFrame to CSV: {e}")
