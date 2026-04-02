import pandas as pd

from app.profiling.detect_types import detect_types

# return correct number of types
def test_detect_types(sample_df):
    result = detect_types(sample_df)
    assert len(result) == 5

# detect numeric types
def test_detect_types_native_numeric(numeric_df):
    result = detect_types(numeric_df)
    assert result["score"] == "numeric"

def test_detect_types_numeric():
    df = pd.DataFrame({
        "score": pd.array(["10.0", "25.0", "one", "30.0", "90.0", "40.0", 
                           "50.0", "10.0", "25.0", "20.0", "25.0"], dtype = "string")
    })
    result = detect_types(df)
    assert result["score"] == "numeric"

def test_detect_types_numeric_less_than_90():
    df = pd.DataFrame({
        "score": pd.array(["10.0", "25.0", "one", "30.0", pd.NA, "40.0", 
                           "50.0", "10.0", "25.0", "20.0", "25.0"], dtype = "string")
    })
    result = detect_types(df)
    assert result["score"] == "string"

# detect datetime types
def test_detect_types_datetime():
    df = pd.DataFrame({
        "order_date": pd.array(["2024-01-01", "2024-06-01", "2024-04-01", "2025-01-01", "Janaray 1st",
                                "2024-06-01", "2024-06-01", "2024-04-01", "2025-01-01", "2024-04-01", "2025-01-01"], dtype = "string")
    })
    result = detect_types(df)
    assert result["order_date"] == "datetime"

def test_detect_types_datetime_less_than_90():
    df = pd.DataFrame({
        "order_date": pd.array(["2024-01-01", "2024-06-01", "2024-04-01", "2025-01-01", "Janaray 1st",
                                pd.NA, "2024-06-01", "2024-04-01", "2025-01-01", "2024-04-01", "2025-01-01"], dtype = "string")
    })
    result = detect_types(df)
    assert result["order_date"] == "string"

# detect boolean types
def test_detect_types_boolean():
    df = pd.DataFrame({
        "active": pd.array(["y", "n", "n", "y", "n", pd.NA], dtype = "string")
    })
    result = detect_types(df)
    assert result["active"] == "boolean"

def test_detect_types_boolean_unknown():
    df = pd.DataFrame({
        "active": pd.array(["y", "n", "n", "y", "m", pd.NA], dtype = "string")
    })
    result = detect_types(df)
    assert result["active"] == "string"

# detect column with only null
def test_detect_types_null():
    df = pd.DataFrame({
        "license": pd.array([pd.NA, pd.NA, pd.NA, pd.NA])
    })
    result = detect_types(df)
    assert result["license"] == "unknown"

# detect empty column 
def test_detect_types_empty():
    df = pd.DataFrame(columns = ["order_id", "amount"])
    result = detect_types(df)

    assert len(result) == 2
    assert result["order_id"] == "unknown"
    assert result["amount"]   == "unknown"

def test_does_not_misclassify_date_as_numeric():
    df = pd.DataFrame({
        "date_added": ["9/25/2021", "9/24/2021", "9/22/2021"]
        })
    result = detect_types(df)
    assert result["date_added"] == "datetime"

def test_does_not_misclassify_numeric_string_mixture_as_numeric():
    df = pd.DataFrame({
        "duration": ["90 min", "1 Season", "91 min", "2 Seasons"]
        })
    result = detect_types(df)
    assert result["duration"] == "string"

def test_does_not_misclassify_id_as_numeric():
    df = pd.DataFrame({
        "show_id": ["s1", "s3", "s6", "s14"]
        })
    result = detect_types(df)
    assert result["show_id"] == "string"

def test_does_not_misclassify_year_as_datetime():
    df = pd.DataFrame({
        "year": ["1990", "2000", "2010", "2020"] # intended to be numeric 
        })
    result = detect_types(df)
    assert result["year"] == "numeric"
