# Data Cleaning Engine

A reusable pipeline for cleaning, standardising, and profiling messy CSV data. Outputs a cleaned CSV, a JSON summary, and a formatted Excel report.

---

## Project Structure

```
data_cleaning_engine/
│
├── main.py                   # entry point
├── config.py                 # default paths and settings
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
│       ├── config.py
│       └── logger.py
│
├── data/                     # place your input CSV here 
├── reports/                  # JSON and Excel reports output here 
├── output_data/              # cleaned CSV output here 
├── test/
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

Uses the paths and settings defined in `config.py`:

```bash
python main.py
```

### CLI — override defaults

All arguments are optional. Any argument not provided falls back to the value in `config.py`.

```bash
python main.py [--input PATH] [--reports PATH] [--output PATH] [--date_format FORMAT]
```

| Argument | Description | Default |
|---|---|---|
| `--input` | Path to input CSV file | `data/messy_sales.csv` |
| `--reports` | Directory for JSON and Excel reports | `reports/` |
| `--output` | Directory for cleaned CSV output | `output_data/` |
| `--date-format` | Expected date format in the CSV | `%Y-%m-%d` |

**Examples:**

```bash
# Run on a different file
python main.py --data data/q1_orders.csv

# Run with a different date format
python main.py --data data/eu_sales.csv --date-format "%d/%m/%Y"

# Override all settings
python main.py --data data/q1_orders.csv --reports results/ --output clean/ --date-format "%d/%m/%Y"
```

---

## Pipeline Steps

1. **Load** — reads CSV, validates file type
2. **Normalise column names** — strips whitespace, lowercases, replaces spaces with underscores
3. **Normalise strings** — strips whitespace, standardises null-like values (`na`, `none`, `?` etc.) to `NaN`
4. **Detect types** — infers column types: `numeric`, `datetime`, `boolean`, `string`, `unknown`
5. **Standardise** — converts columns to their detected types, handles currency symbols, accounting negatives, scientific notation
6. **Remove duplicates** — drops exact duplicate rows, keeps first occurrence
7. **Generate reports** — outputs JSON summary, Excel report, and cleaned CSV

---

## Outputs

| File | Location | Description |
|---|---|---|
| `clean.csv` | `output_data/` | Cleaned and standardised dataset |
| `summary.json` | `reports/` | Full statistics summary |
| `summary.xlsx` | `reports/` | Formatted Excel report with dataset overview and column profiles |

---

## Configuration

Default settings live in `config.py`:

```python
DATA_PATH   = "data/messy_sales.csv"
REPORT_PATH = "reports/"
OUTPUT_PATH = "output_data/"
DATE_FORMAT = "%Y-%m-%d"
```

Edit this file to change the defaults without using CLI arguments.

---