# standardisation.py
import pandas as pd
import re

from app.utils.logger import get_logger
logger = get_logger(__name__)

NULL_WORDS = {
    "",
    "na",
    "n/a",
    "null",
    "none",
    "nan",
    "-",
    "nil",
    "unknown",
    "?"
}

TRUE_LIST = {"true", "yes", "1", "y", "on", "t"}
FALSE_LIST = {"false", "no", "0", "n", "off", "f"}

def clean_column_names(col: str) -> str:
    """Clean column names"""
    col = col.strip().lower()
    col = re.sub(r"[^\w\s-]", "", col)   # remove special chars
    col = re.sub(r"[\s-]+", "_", col)    # space & dash to underscore
    col = re.sub(r"_+", "_", col)        # collapse multiple _
    col = col.strip("_")
    return col

def normalise_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalise column names

    Parameters:
        df: Entire dataframe

    Returns:
        Dataframe with normalised column names
    """
    df = df.copy()
    df.columns = [clean_column_names(col) for col in df.columns]
    duplicates = df.columns[df.columns.duplicated()].tolist()
    if duplicates:
        raise ValueError(f"Duplicate colum names after normalisation: {duplicates}")
    return df

def normalise_string(series: pd.Series) -> pd.Series:
    """
    Normalise string object by vectorise operation (space stripping, normalise null values)

    Parameters:
        series: a column pd.series 

    Returns:
        normalised column 
    """
    if not (pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series)):
        return series
    logger.debug(series.dtype)
    
    series = series.astype("string").str.strip()

    mask = series.str.lower().isin(NULL_WORDS)
    series = series.where(~mask, other = pd.NA)

    return series

def normalise_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to normalise entire dataframe

    Parameters:
        df: entire dataframe

    Returns:
        dataframe with normalised string 
    """
    df = df.copy()
    for col in df.columns:
        df[col] = normalise_string(df[col])
    return df

def standardise_date(series: pd.Series, date_format = None) -> pd.Series:
    """
    Convert to pandas datetime varible

    Parameters:
        series: data column
        date_format: control the display date format

    Returns:
        datetime column
    """
    if isinstance(series.dtype, pd.DatetimeTZDtype):
        return series
    
    before_na = series.isna()
    series = pd.to_datetime(series, format = date_format, errors="coerce", utc = True)
    after_na = (~before_na) & series.isna()

    if after_na.any():
        logger.warning(f"Failed to parse {after_na.sum()} items to datetime")
    return series

def keep_one_decimal(num: str) -> str:
    """handle multiple decimal"""
    num_parts = num.split(".")
    if len(num_parts) > 2: # more than 1 decimal, only keep the first one
        return num_parts[0] + "." + "".join(num_parts[1:])
    return num

def clean_numeric_series(series: pd.Series) -> pd.Series:
    """
    clean numeric string and convert column object to numeric

    Parameters:
        series: data column

    Returns:
        numeric column
    """    
    before_na = series.isna()
    series = series.astype(str).str.strip()
    series = series.str.replace(r"\((.*?)\)", r"-\1", regex=True)
    series = series.str.replace(r"[^\d\.\-eE+]", "", regex=True)

    series = series.apply(keep_one_decimal)

    series = pd.to_numeric(series, errors="coerce")

    after_na = (~before_na) & series.isna()

    if after_na.any():
        logger.warning(f"Failed to parse {after_na.sum()} items to numeric")

    return series

def standardise_numeric(series: pd.Series) -> pd.Series:
    """convert numeric string column to numeric"""
    if pd.api.types.is_numeric_dtype(series):
        return series

    return clean_numeric_series(series)

def standardise_boolean(series: pd.Series) -> pd.Series:
    """
    convert bool string to True/False

    Parameters:
        series: data column

    Returns:
        boolean column
    """   
    if str(series.dtype) == "boolean":
        return series

    series = series.astype(str).str.strip().str.lower()

    result = pd.Series(pd.NA, index = series.index, dtype="boolean")
    result[series.isin(TRUE_LIST)] = True
    result[series.isin(FALSE_LIST)] = False

    return result

    
def standardise_data(df: pd.DataFrame, column_types: dict, date_format: str = None) -> pd.DataFrame:
    """
    Process the whole dataframe according to the data type

    Parameters:
        df: entire dataframe
        column_types: dictionary object with key: column names, values: data types 
            detected from app.profiling.detect_types
        date_format: control the display date format
    
    Returns:
        standardised dataframe
    """
    logger.info("Start standardising data")
    df = df.copy()

    for col, col_type in column_types.items():
        if col not in df.columns: 
            continue

        if col_type == "numeric":
            df[col] = standardise_numeric(df[col])

        elif col_type == "datetime":
            df[col] = standardise_date(df[col], date_format)

        elif col_type == "boolean":
            df[col] = standardise_boolean(df[col])

    return df
    
