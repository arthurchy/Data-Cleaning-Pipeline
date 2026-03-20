# detect_types.py
import pandas as pd
import warnings
from app.utils.logger import get_logger

logger = get_logger(__name__)

TYPE_THRESHOLD = 0.9

def attempt_numeric_convert(series: pd.Series) -> pd.Series:
    """convert string to numeric"""
    series = series.astype(str)
    series = series.str.replace(r"\((.*?)\)", r"-\1", regex=True)
    series = series.str.replace(r"[^\d\.-]", "", regex=True)
    return pd.to_numeric(series, errors="coerce")

def detect_column_type(column: pd.Series) -> str:
    """
    Detect input column data type

    Parameters:
        column: input column
    
    Returns:
        a string defines the column data type:
        numeric / datetime / boolean / string / unknown
    """
    non_null = column.dropna()

    if non_null.empty:
        return "unknown"    

    if pd.api.types.is_numeric_dtype(column):
        return "numeric"
    
    with warnings.catch_warnings(action="ignore"):
        num_cov = attempt_numeric_convert(non_null)
    num_ratio = num_cov.notna().mean()

    if num_ratio > TYPE_THRESHOLD:
        return "numeric"
    
    # try to convert to datetime
    with warnings.catch_warnings(action="ignore"):
        date_cov = pd.to_datetime(non_null, errors = "coerce")
    date_ratio = date_cov.notna().mean()

    if date_ratio > TYPE_THRESHOLD:
        return "datetime"
    
    unique_vals = set(non_null.astype(str).str.lower().unique())
    if unique_vals.issubset({"true", "false", "yes", "no", "0", "1", "on", "off", "y", "n"}):
        return "boolean"
    
    return "string"

def detect_types(df: pd.DataFrame) -> dict:
    """process the detection for entire dataframe"""
    logger.info("Start detecting columns types")
    result = {}
    for col in df.columns:
        result[col] = detect_column_type(df[col])
    return result