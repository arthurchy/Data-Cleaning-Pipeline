# main.py
import argparse
import os

from app.data_access.data_io import load_data, output_json, save_data
from app.pipeline import run_pipeline
from app.excel.write_excel import create_worksheet

from app.utils.config import (
    DATA_PATH, INPUT_NAME,
    REPORT_PATH, REPORT_NAME,
    OUTPUT_PATH, OUTPUT_NAME,
    DATE_FORMAT
)
from app.utils.logger import get_logger
logger = get_logger(__name__)

JSON_SUFFIX = ".json"
EXCEL_SUFFIX = ".xlsx"

def main():
    parser = argparse.ArgumentParser(description = "Data Cleaning Pipeline")
    parser.add_argument("--input", default = INPUT_NAME,  help = "Input CSV filename")
    parser.add_argument("--output", default = OUTPUT_NAME, help = "Output CSV filename")
    parser.add_argument("--report", default = REPORT_NAME, help = "Report name (no extension)")
    parser.add_argument("--date-format", default = DATE_FORMAT, help = "Date format e.g. %%Y-%%m-%%d")
    args = parser.parse_args()

    df_raw = load_data(os.path.join(DATA_PATH, args.input))

    df_clean, summary = run_pipeline(df_raw, args.date_format)
    
    output_json(summary, REPORT_PATH,f"{args.report}.json")
    save_data(df_clean, OUTPUT_PATH, args.output)
    create_worksheet(summary, REPORT_PATH, f"{args.report}.xlsx")

if __name__ == "__main__":
    main()



