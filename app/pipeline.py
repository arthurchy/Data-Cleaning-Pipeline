# pipeline.py
import pandas as pd

from app.profiling.detect_types import detect_types

from app.cleaning.standardisation import normalise_column_names, normalise_df, standardise_data
from app.cleaning.duplicates import drop_duplicate_default

from app.reporting.summary_stats import generate_summary

from app.utils.logger import get_logger
from app.utils.cleaning_log import CleaningLog

logger = get_logger(__name__)   

def run_pipeline(df: pd.DataFrame, date_format: str = None) -> tuple[pd.DataFrame, dict]:
    """Construct the data cleaning pipeline"""
    cleaning_log = CleaningLog()
    logger.info("Start data cleaning pipeline")
    df = df.copy()
    df = normalise_column_names(df)
    df = normalise_df(df, cleaning_log)

    df_types = detect_types(df)
    df = standardise_data(df, df_types, date_format, cleaning_log)
    df_pre_drop = df.copy()
    df = drop_duplicate_default(df, cleaning_log)

    summary = generate_summary(df_pre_drop, df)

    if not cleaning_log.is_empty():
        summary["cleaning_log"] = cleaning_log.to_list()

    return df, summary





