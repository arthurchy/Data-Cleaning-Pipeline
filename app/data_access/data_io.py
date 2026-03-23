# data_io.py
import pandas as pd
import os
import json

from app.utils.logger import get_logger

logger = get_logger(__name__)

def load_data(file_path: str) -> pd.DataFrame:
    """Load data, currently only takes csv as input"""    
    if not file_path.endswith(".csv"):
        raise ValueError(f"Only CSV files are supported, got: {file_path}")
    
    logger.info(f"Loading data from {file_path}")
    try:
        data = pd.read_csv(file_path)
        logger.info(f"Loaded {len(data)} rows, {len(data.columns)} columns")
        return data
    except FileNotFoundError:
        logger.error("No file found")
        raise

def output_json(summary: dict, output_path: str, filename: str) -> None:
    """output summary as json"""    
    os.makedirs(output_path, exist_ok=True)
    full_path = os.path.join(output_path, filename)

    try:
        with open(full_path, "w") as f:
            json.dump(summary, f, indent=4)
        logger.info(f"Saved summary to {full_path}")
    except PermissionError:
        logger.error(f"Permission denied writing to {full_path}")
        raise
    except OSError as e:
        logger.error(f"Failed to save summary to {full_path}: {e}")
        raise
    except TypeError as e:
        logger.error(f"Summary contains non-serialisable values: {e}")
        raise

def save_data(df: pd.DataFrame, output_path: str, filename: str) -> None:
    """save cleaned dataframe"""   
    os.makedirs(output_path, exist_ok=True)  
    full_path = os.path.join(output_path, filename)

    try:
        df.to_csv(full_path, index=False)
        logger.info(f"Saved cleaned data to {full_path}")
    except PermissionError:
        logger.error(f"Permission denied writing to {full_path}")
        raise
    except OSError as e:
        logger.error(f"Failed to save data to {full_path}: {e}")
        raise
