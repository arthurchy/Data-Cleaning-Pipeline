# Data Cleaning Engine

A reusable pipeline for cleaning, standardising, and profiling messy CSV data. Outputs a cleaned CSV, a JSON summary, and a formatted Excel report.

---

## Project Structure

```
data_cleaning_engine/
│
├── main.py                   # entry point
│
├── app/
│   ├── pipeline.py           # orchestrates the cleaning steps
│   │
│   ├── cleaning/
│   │   ├── standardisation.py
│   │   └── duplicates.py
│   │
│   ├── profiling/
│   │   └── detect_types.py
│   │
│   ├── reporting/
│   │   └── summary_stats.py
│   │
│   ├── excel/
│   │   └── write_excel.py
│   │
│   ├── data_access/
│   │   └── data_io.py
│   │
│   └── utils/
│       ├── config.py         # default paths and filenames
│       └── logger.py
│
├── data/                     # place your input CSV here
├── reports/                  # JSON and Excel reports output here
├── output_data/              # cleaned CSV output here
├── logs/                     # log files output here
├── tests/
├── requirements.txt
└── README.md
```

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Usage

### Default run

Uses the paths and filenames defined in `app/utils/config.py`:

```bash
python main.py
```

### CLI — override defaults

All arguments are optional. Any argument not provided falls back to the value in `config.py`.

```bash
python main.py [--input FILENAME] [--output FILENAME] [--report NAME] [--date-format FORMAT]
```

| Argument | Description | Default |
|---|---|---|
| `--input` | Input CSV filename (inside `data/`) | `test.csv` |
| `--output` | Output CSV filename (inside `output_data/`) | `clean.csv` |
| `--report` | Report name without extension (inside `reports/`) | `summary` |
| `--date-format` | Expected date format in the CSV | `%Y-%m-%d` |

**Examples:**

```bash
# Run on a different file
python main.py --input q1_orders.csv

# Run with a different date format
python main.py --input eu_sales.csv --date-format "%d/%m/%Y"

# Override all settings
python main.py --input q1_orders.csv --output q1_clean.csv --report q1_summary --date-format "%d/%m/%Y"
```

---

## Pipeline Steps

1. **Load** — reads CSV from `data/`, validates file type
2. **Normalise column names** — strips whitespace, lowercases, replaces spaces with underscores
3. **Normalise strings** — strips whitespace, standardises null-like values (`na`, `none`, `?` etc.) to `NaN`
4. **Detect types** — infers column types: `numeric`, `datetime`, `boolean`, `string`, `unknown`
5. **Standardise** — converts columns to their detected types, handles currency symbols, accounting negatives, scientific notation
6. **Remove duplicates** — drops exact duplicate rows, keeps first occurrence
7. **Generate reports** — outputs JSON summary, Excel report, and cleaned CSV

---

## Outputs

For a run with `--report q1_summary` and `--output q1_clean.csv`:

| File | Location | Description |
|---|---|---|
| `q1_clean.csv` | `output_data/` | Cleaned and standardised dataset |
| `q1_summary.json` | `reports/` | Full statistics summary |
| `q1_summary.xlsx` | `reports/` | Formatted Excel report with dataset overview and column profiles |

The report name (e.g. `q1_summary`) is shared by both the `.json` and `.xlsx` outputs.

---

## Configuration

Default settings live in `app/utils/config.py`:

```python
DATA_PATH    = "data/"
REPORT_PATH  = "reports/"
OUTPUT_PATH  = "output_data/"

INPUT_NAME   = "test.csv"
OUTPUT_NAME  = "clean.csv"
REPORT_NAME  = "summary"     # shared name for .json and .xlsx outputs

DATE_FORMAT  = "%Y-%m-%d"
```

Edit this file to change the defaults without using CLI arguments.

---
