import pytest
import pandas as pd
import os
from app.data_access.data_io import load_data, output_json, save_data

# load_data
def test_load_data_returns_dataframe(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,score\nAlice,10\nBob,20")

    result = load_data(str(csv_file))

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert list(result.columns) == ["name", "score"]

def test_load_data_correct_values(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,score\nAlice,10\nBob,20")

    result = load_data(str(csv_file))

    assert result.iloc[0]["name"] == "Alice"
    assert result.iloc[1]["score"] == 20    

def test_load_data_rejects_non_csv():
    with pytest.raises(ValueError, match="Only CSV files are supported"):
        load_data("data/file.xlsx")

def test_load_data_raises_on_missing_file():
    with pytest.raises(FileNotFoundError):
        load_data("data/does_not_exist.csv")

# output_json
def test_output_json_creates_file(tmp_path):
    summary = {"dataset": {"row_count": 100}}

    output_json(summary, str(tmp_path), "summary.json")

    assert os.path.exists(tmp_path / "summary.json")

def test_output_json_creates_directory(tmp_path):
    nested_path = str(tmp_path / "new_folder" / "reports")
    summary = {"dataset": {"row_count": 100}}

    output_json(summary, nested_path, "summary.json")

    assert os.path.exists(os.path.join(nested_path, "summary.json"))

def test_output_json_raises_on_non_serialisable(tmp_path):
    import pandas as pd
    summary = {"date": pd.Timestamp("2024-01-01")}

    with pytest.raises(TypeError):
        output_json(summary, str(tmp_path), "summary.json")

def test_save_data_creates_file(tmp_path, sample_df):
    save_data(sample_df, str(tmp_path), "clean.csv")

    assert os.path.exists(tmp_path / "clean.csv")

def test_save_data_creates_directory(tmp_path, sample_df):
    nested_path = str(tmp_path / "new_folder" / "output")

    save_data(sample_df, nested_path, "clean.csv")

    assert os.path.exists(os.path.join(nested_path, "clean.csv"))