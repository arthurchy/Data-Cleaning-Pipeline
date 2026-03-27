# tests/cleaning/test_standardisation.py
import pytest
import pandas as pd
from app.cleaning.standardisation import (
    clean_column_names,
    normalise_column_names,
    normalise_string,
    normalise_df,
    standardise_date,
    clean_numeric_series,
    standardise_numeric,
    standardise_boolean,
    standardise_data
)

def test_clean_column_names_basic():
    assert clean_column_names("First Name") == "first_name"
    assert clean_column_names("  Order-ID  ") == "order_id"
    assert clean_column_names("Price ($)") == "price"

def test_normalise_column_names_raises_on_duplicates():
    df = pd.DataFrame(columns=["First Name", "first_name"])
    with pytest.raises(ValueError, match = "Duplicate"):
        normalise_column_names(df)

def test_normalise_string_null_words():
    s = pd.Series(["Alice", "na", "null", "?", "none", "Bob"])
    result = normalise_string(s)
    assert result.isna().sum() == 4      # na, null, ?, none → NaN
    assert result[0] == "Alice"
    assert result[5] == "Bob"

def test_normalise_df():
    df = pd.DataFrame({
        "name": ["  Alice  ", "na", "Bob"],
        "score": ["1", "null", "3"]
    })
    result = normalise_df(df)
    assert result["name"][0] == "Alice"
    assert result["name"].isna().sum() == 1
    assert result["score"].isna().sum() == 1

# test datetime
def test_standardise_date():
    s = pd.Series(["2024-01-01", "2024-06-01"])
    result = standardise_date(s)
    assert pd.api.types.is_datetime64_any_dtype(result)
    assert result.isna().sum() == 0

def test_standardise_date_invalid():
    s = pd.Series(["2024-01-01", "Bad_Day"])
    result = standardise_date(s)
    assert result.isna().sum() == 1

def test_standardise_date_null():
    s = pd.Series(["2024-01-01", pd.NA])
    result = standardise_date(s)
    assert result.isna().sum() == 1

def test_standardise_date_skips_already_datetime_with_tz(datetime_df):
    result = standardise_date(datetime_df["order_date"])
    pd.testing.assert_series_equal(result, datetime_df["order_date"])

def test_standardise_date_adds_utc():
    s = pd.Series(pd.to_datetime(["2024-01-01", "2024-06-01"]))
    result = standardise_date(s)
    assert result.dt.tz is not None    

# test numeric
def test_clean_numeric_currency():
    s = pd.Series(["$1,200.00", "£750.50", "€300"])
    result = clean_numeric_series(s)
    assert result[0] == 1200.0
    assert result[1] == 750.5
    assert result[2] == 300.0

def test_clean_numeric_accounting_negatives():
    s = pd.Series(["(500)", "(1,200.00)"])
    result = clean_numeric_series(s)
    assert result[0] == -500.0
    assert result[1] == -1200.0

def test_clean_numeric_series_real_case():
    """Test if the function works as intend, i.e only keep the first decimal place"""
    s = pd.Series(["1,200.50.00", "3.141.5", ".34"])
    result = clean_numeric_series(s)
    assert result[0] == 1200.5000
    assert result[1] == 3.1415
    assert result[2] == .34

def test_clean_numeric_scientific_notation():
    s = pd.Series(["1.5e10", "2.3e-4", "-3.5e-5"])
    result = clean_numeric_series(s)
    assert result[0] == 1.5e10
    assert result[1] == 2.3e-4
    assert result[2] == -3.5e-5

def test_clean_numeric_comma_separated():
    s = pd.Series(["1,200.50", "600", "7,000"])
    result = clean_numeric_series(s)
    assert result[0] == 1200.50
    assert result[1] == 600
    assert result[2] == 7000

def test_standardise_native_numeric(numeric_df):
    result = standardise_numeric(numeric_df["score"])
    pd.testing.assert_series_equal(result, numeric_df["score"])

# test boolean
def test_standardise_boolean_true_values():
    s = pd.Series(["yes", "true", "1", "y", "on", "t"])
    result = standardise_boolean(s)
    assert result.all() # all should be True

def test_standardise_boolean_false_values():
    s = pd.Series(["no", "false", "0", "n", "off", "f"])
    result = standardise_boolean(s)
    assert (~result).all() # all should be False

def test_standardise_boolean_unknown_is_na():
    s = pd.Series(["maybe", "perhaps"])
    result = standardise_boolean(s)
    assert result.isna().all()

def test_standardise_native_boolean(boolean_df):
    result = standardise_boolean(boolean_df["active"])
    pd.testing.assert_series_equal(result, boolean_df["active"])

# test standardise_data 
def test_standardise_data_routes_numeric():
    df = pd.DataFrame({"amount": ["100", "200"]})
    result = standardise_data(df, {"amount": "numeric"})
    assert pd.api.types.is_numeric_dtype(result["amount"])

def test_standardise_data_routes_datetime():
    df = pd.DataFrame({"order_date": ["2024-01-01", "2024-06-01"]})
    result = standardise_data(df, {"order_date": "datetime"})
    assert pd.api.types.is_datetime64_any_dtype(result["order_date"])

def test_standardise_data_routes_boolean():
    df = pd.DataFrame({"active": ["yes", "no"]})
    result = standardise_data(df, {"active": "boolean"})
    assert result["active"].dtype == "boolean"

def test_standardise_data_skips_missing_column():
    df = pd.DataFrame({"amount": ["100", "200"]})
    result = standardise_data(df, {"amount": "numeric", "missing_col": "numeric"})
    assert list(result.columns) == ["amount"]

