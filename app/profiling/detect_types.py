# detect_types.py
import pandas as pd
import warnings
from app.utils.logger import get_logger

logger = get_logger(__name__)

TYPE_THRESHOLD = 0.9

TRUE_LIST = {"true", "yes", "1", "y", "on", "t"}
FALSE_LIST = {"false", "no", "0", "n", "off", "f"}

def attempt_numeric_convert(series: pd.Series) -> pd.Series:
    """convert string to numeric"""
    series = series.astype(str)
    series = series.str.replace(r"\((.*?)\)", r"-\1", regex=True)
    series = series.str.replace(r"[^\d\.-]", "", regex=True)
    return pd.to_numeric(series, errors="coerce")

def numeric_looking(series: pd.Series) -> bool:
    has_non_numeric_letters = series.astype(str).str.contains(
        r"[a-df-zA-DF-Z]",   # all letters except e and E
        regex=True
    )

    has_date_chars = series.astype(str).str.contains(
        r"[/:-]",
        regex=True
    )

    is_numeric_looking = ~has_non_numeric_letters & ~has_date_chars
    return is_numeric_looking.mean() > TYPE_THRESHOLD

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
    
    if isinstance(non_null.dtype, pd.DatetimeTZDtype):
        return "datetime"
    
    if str(non_null.dtype) == "boolean":
        return "boolean"
    
    # try to convert to datetime
    if not numeric_looking(non_null):
        with warnings.catch_warnings(action="ignore"):
            date_cov = pd.to_datetime(non_null, errors = "coerce")
            date_ratio = date_cov.notna().mean()
        if date_ratio > TYPE_THRESHOLD:
            return "datetime"
    
    if numeric_looking(non_null):
        with warnings.catch_warnings(action="ignore"):
            num_cov = attempt_numeric_convert(non_null)
            num_ratio = num_cov.notna().mean()
        if num_ratio > TYPE_THRESHOLD:
            return "numeric"
    
    unique_vals = set(non_null.astype(str).str.lower().unique())
    if unique_vals.issubset(TRUE_LIST | FALSE_LIST):
        return "boolean"
    
    return "string"

def detect_types(df: pd.DataFrame) -> dict:
    """process the detection for entire dataframe"""
    logger.info("Start detecting columns types")
    result = {}
    for col in df.columns:
        result[col] = detect_column_type(df[col])
    return result