import pandas as pd

from app.utils.logger import get_logger
from app.utils.cleaning_log import CleaningLog

logger = get_logger(__name__)

def drop_duplicate_default(df: pd.DataFrame, cleaning_log: CleaningLog = None) -> pd.DataFrame:
    """
    drop duplicate rows
    Parameters:
        df: entire dataframe

    Returns:
        dataframe without duplicate rows
    """    
    num_dropped = df.duplicated().sum()
    logger.info(f"Number of duplicate rows dropped: {num_dropped}")

    if cleaning_log and num_dropped > 0:
        cleaning_log.log(
            column = "all columns",
            change_type = "drop_duplicate_rows",
            detail = "number of duplicate rows removed",
            count = int(num_dropped)
        )

    return df.drop_duplicates(keep = "first")

