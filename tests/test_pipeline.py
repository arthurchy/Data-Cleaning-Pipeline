import pandas as pd
import pytest
from app.pipeline import run_pipeline

def test_run_pipeline():
    df = pd.DataFrame({
        "First Name": ["Alice", "Bob", "Alice"],
        "Amount": ["$1,200.00", "($500)", "$1,200.00"],
        "Order Date": ["2024-01-01", "2024-02-01", "2024-01-01"],
        "Active": ["yes", "no", "yes"]
    })
    result_df, summary = run_pipeline(df, "%Y-%m-%d")

    # test normalise column name
    assert list(result_df.columns) == ["first_name", "amount", "order_date", "active"]

    # test removing duplciate row
    assert len(result_df) == 2

    # test if the standisation work for each types
    assert pd.api.types.is_numeric_dtype(result_df["amount"])
    assert pd.api.types.is_datetime64_any_dtype(result_df["order_date"])
    assert result_df["active"].dtype == "boolean"

    # test summary is created 
    assert summary["dataset"]["row_count"] == 2
    assert summary["dataset"]["duplicate_row_removed"] == 1