import pandas as pd
import pytest
from app.reporting.summary_stats import generate_summary

# dataset statistic testing
def test_row_count(numeric_df):
    summary = generate_summary(numeric_df, numeric_df)
    assert summary["dataset"]["row_count"] == 4

def test_column_count(numeric_df):
    summary = generate_summary(numeric_df, numeric_df)
    assert summary["dataset"]["column_count"] == 1

def test_no_duplicate_row_removed(numeric_df):
    summary = generate_summary(numeric_df, numeric_df)
    assert summary["dataset"]["duplicate_row_removed"] == 0

def test_duplicate_row_removed(df_with_duplicates_summary):
    before, after = df_with_duplicates_summary
    summary = generate_summary(before, after)
    assert summary["dataset"]["duplicate_row_removed"] == 1

# column statistc basic testing
def test_column_base_stats_present(numeric_df):
    summary = generate_summary(numeric_df, numeric_df)
    col = summary["columns"]["score"]
    for key in ["dtype", "missing_count", "missing_pct", "unique_count", "memory"]:
        assert key in col

def test_missing_count(string_df):
    df = string_df.copy()
    df.loc[0, "name"] = pd.NA
    summary = generate_summary(df, df)
    assert summary["columns"]["name"]["missing_count"] == 1

def test_missing_pct(string_df):
    df = string_df.copy()
    df.loc[0, "name"] = pd.NA
    summary = generate_summary(df, df)
    assert summary["columns"]["name"]["missing_pct"] == pytest.approx(0.25)

def test_unique_count(string_df):
    summary = generate_summary(string_df, string_df)
    assert summary["columns"]["name"]["unique_count"] == 3  

# numeric column testing
def test_numeric_stats_present(numeric_df):
    summary = generate_summary(numeric_df, numeric_df)
    col = summary["columns"]["score"]
    for key in ["min", "max", "mean", "median", "std_dev"]:
        assert key in col

def test_numeric_stats_calculations(numeric_df):
    summary = generate_summary(numeric_df, numeric_df)
    col = summary["columns"]["score"]
    assert col["min"] == pytest.approx(10.0)
    assert col["max"] == pytest.approx(60.0)
    assert col["mean"] == pytest.approx(30.0)
    assert col["median"] == pytest.approx(25.0)
    assert col["std_dev"] == pytest.approx(21.6025)

def test_numeric_stats_not_present_for_string(string_df):
    summary = generate_summary(string_df, string_df)
    col = summary["columns"]["name"]
    assert "min" not in col
    assert "mean" not in col

# string column testing
def test_top3_present_for_string(string_df):
    summary = generate_summary(string_df, string_df)
    assert "Top3" in summary["columns"]["name"]

def test_top3_correct_values(string_df):
    summary = generate_summary(string_df, string_df)
    top3 = summary["columns"]["name"]["Top3"]
    assert top3["Alice"] == 2   
    assert "Bob" in top3
    assert "Tom" in top3

def test_top3_not_present_for_numeric(numeric_df):
    summary = generate_summary(numeric_df, numeric_df)
    assert "Top3" not in summary["columns"]["score"]

# boolean column testing
def test_boolean_stats_present(boolean_df):
    summary = generate_summary(boolean_df, boolean_df)
    assert "Distribution" in summary["columns"]["active"]

def test_distribution_correct_values(boolean_df):
    summary = generate_summary(boolean_df, boolean_df)
    dist = summary["columns"]["active"]["Distribution"]
    assert dist[True]  == 2
    assert dist[False] == 2

def test_distribution_not_present_for_numeric(numeric_df):
    summary = generate_summary(numeric_df, numeric_df)
    assert "Distribution" not in summary["columns"]["score"]

# datetime column testing
def test_datetime_stats_present(datetime_df):
    summary = generate_summary(datetime_df, datetime_df)
    col = summary["columns"]["order_date"]
    for key in ["min_day", "max_day", "day_range"]:
        assert key in col

def test_datetime_range(datetime_df):
    summary = generate_summary(datetime_df, datetime_df)
    col = summary["columns"]["order_date"]
    assert col["day_range"] == 366

def test_datetime_min_max_are_strings(datetime_df):
    summary = generate_summary(datetime_df, datetime_df)
    col = summary["columns"]["order_date"]
    assert isinstance(col["min_day"], str)
    assert isinstance(col["max_day"], str)

def test_datetime_stats_not_present_for_numeric(numeric_df):
    summary = generate_summary(numeric_df, numeric_df)
    assert "min_day" not in summary["columns"]["score"]
