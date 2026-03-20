# main.py
import argparse

from app.data_access.data_io import load_data, output_json, save_data
from app.pipeline import run_pipeline
from app.excel.write_excel import create_worksheet

from app.utils.config import DATA_PATH, REPORT_PATH, DATE_FORMAT, OUTPUT_PATH

from app.utils.logger import get_logger
logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Data Cleaning Pipeline")
    parser.add_argument("--input", default=DATA_PATH)
    parser.add_argument("--reports", default=REPORT_PATH)
    parser.add_argument("--output", default=OUTPUT_PATH)
    parser.add_argument("--date_format", default=DATE_FORMAT)
    args = parser.parse_args()

    df_raw = load_data(args.input)
    df_clean, summary = run_pipeline(df_raw, args.date_format)
    
    output_json(summary, args.reports, "summary.json")
    save_data(df_clean, args.output, "clean.csv")
    create_worksheet(summary, args.reports, "summary.xlsx")
    

if __name__ == "__main__":
    main()



