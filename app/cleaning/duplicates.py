import pandas as pd

from app.utils.logger import get_logger

logger = get_logger(__name__)

def drop_duplicate_default(df: pd.DataFrame) -> pd.DataFrame:
    """
    drop duplicate rows
    Parameters:
        df: entire dataframe

    Returns:
        dataframe without duplicate rows
    """    
    num_dropped = df.duplicated().sum()
    logger.info(f"Number of duplicate rows dropped: {num_dropped}")
    return df.drop_duplicates(keep = "first")

