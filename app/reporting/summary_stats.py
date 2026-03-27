# summary_stats.py
import pandas as pd
from app.utils.logger import get_logger

logger = get_logger(__name__)

DECIMAL_PLACES = 4

def generate_summary(pre_drop_df: pd.DataFrame, df: pd.DataFrame) -> dict:
    """
    create the summary dictionary for the dataframe

    Parameters:
        pre_drop_df: dataframe after normalisation, before drop duplicates
        df: after dropping duplication, cleaned dataframe
    
    Returns:
        Statistics summary dictioary 
    """
    logger.info("Start generating summary")
    summary = {
        "dataset": {},
        "columns": {}
    }

    summary["dataset"]["row_count"] = int(df.shape[0])
    summary["dataset"]["column_count"] = int(df.shape[1])
    summary["dataset"]["duplicate_row_removed"] = pre_drop_df.shape[0] - summary["dataset"]["row_count"]

    for col in df.columns:
        col_data = df[col]

        col_summary = {
            "dtype": str(col_data.dtype),
            "missing_count": int(col_data.isna().sum()),
            "missing_pct": round(float(col_data.isna().mean()), DECIMAL_PLACES),
            "unique_count": int(col_data.nunique()),
            "memory": int(col_data.memory_usage(deep = True))
        }

        if pd.api.types.is_numeric_dtype(col_data):
            col_summary.update({
                "min": round(float(col_data.min()), DECIMAL_PLACES),
                "max": round(float(col_data.max()), DECIMAL_PLACES),
                "mean": round(float(col_data.mean()), DECIMAL_PLACES),
                "median": round(float(col_data.median()), DECIMAL_PLACES),
                "std_dev": round(float(col_data.std()), DECIMAL_PLACES)
            })
        
        if pd.api.types.is_string_dtype(col_data):
            col_summary.update({
                "Top3": col_data.value_counts().head(3).to_dict()
                })
        
        if str(col_data.dtype) == "boolean":
            col_summary.update({
                "Distribution": col_data.value_counts().to_dict()
            })

        if isinstance(col_data.dtype, pd.DatetimeTZDtype):
            col_summary.update({
                "min_day": col_data.min().isoformat(),
                "max_day": col_data.max().isoformat(),
                "day_range": int((col_data.max() - col_data.min()).days)
            })

        summary["columns"][col] = col_summary

    # debug print
    logger.debug(f"Dataset summary: {summary['dataset']}")
    for col, col_data in summary["columns"].items():
        logger.debug(f"{col}: {col_data}")
        
    return summary



    


