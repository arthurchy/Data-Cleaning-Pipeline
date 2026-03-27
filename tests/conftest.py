# tests/conftest.py
import pytest
import pandas as pd

@pytest.fixture
def sample_df():
    """Clean, already normalised DataFrame for testing"""
    return pd.DataFrame({
        "order_id":  ["001", "002", "003"],
        "amount":    ["$1,200.00", "($500)", "750.50"],
        "order_date":["2024-01-01", "2024-02-01", "2024-03-01"],
        "active":    ["yes", "no", "true"],
        "user_name": ["Alice", "Bob", "Tom"]
    })

@pytest.fixture
def df_with_duplicates():
    return pd.DataFrame({
        "name":  ["Alice", "Bob", "Alice"],
        "score": [10, 20, 10]
    })

# summary stats
@pytest.fixture
def numeric_df():
    return pd.DataFrame({
        "score": pd.array([10.0, 20.0, 60.0, 30.0], dtype = "float64")
    })

@pytest.fixture
def string_df():
    return pd.DataFrame({
        "name": pd.array(["Alice", "Bob", "Tom", "Alice"], dtype = "string")
    })

@pytest.fixture
def boolean_df():
    return pd.DataFrame({
        "active": pd.array([True, False, False, True], dtype = "boolean")
    })

@pytest.fixture
def datetime_df():
    return pd.DataFrame({
        "order_date": pd.to_datetime(
            ["2024-01-01", "2024-06-01", "2024-04-01", "2025-01-01"], utc=True
        )
    })

@pytest.fixture
def df_with_duplicates_summary():
    before = pd.DataFrame({"name": ["Alice", "Bob", "Alice", "Carol"]})
    after = pd.DataFrame({"name": ["Alice", "Bob", "Carol"]})
    return before, after

