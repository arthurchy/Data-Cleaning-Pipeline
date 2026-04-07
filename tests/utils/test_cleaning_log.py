# test_cleaning_log.py
from app.utils.cleaning_log import CleaningLog

def test_cleaning_log_empty():
    log = CleaningLog()
    assert log.is_empty()

def test_cleaning_log_to_list():
    log = CleaningLog()
    assert log.to_list() == []


def test_logs_adds_entry():
    log = CleaningLog()
    log.log("name", "null_word_replaced", '"Not Given" -> "NaN"', 1000)
    assert not log.is_empty()

def test_logs_adds_entry():
    log = CleaningLog()
    log.log("name", "null_word_replaced", '"Not Given" -> "NaN"', 1000)
    
    entry = log.to_list()[0]
    assert entry["column"] == "name"
    assert entry["change_type"] == "null_word_replaced"
    assert entry["detail"] == '"Not Given" -> "NaN"'
    assert entry["detail"] == '"Not Given" -> "NaN"'
    assert entry["count"] == 1000

def test_multiple_entries():
    log = CleaningLog()
    log.log("name", "null_word_replaced", '"Not Given" -> "NaN"', 1000)
    log.log("country", "null_word_replaced", '"" -> "NaN"', 500)
    log.log("datetime", "datetime_parse_failed", 'coerced to NaT', 20)

    assert len(log.to_list()) == 3

def test_log_same_column_multiple_times():
    log = CleaningLog()
    log.log("name", "null_word_replaced", '"Not Given" -> "NaN"', 1000)
    log.log("name", "null_word_replaced", '"" -> "NaN"', 40)

    entries = log.to_list()
    assert len(entries) == 2
    assert entries[0]["detail"] == '"Not Given" -> "NaN"'
    assert entries[1]["detail"] == '"" -> "NaN"'

def test_to_list_does_not_mutate():
    log = CleaningLog()
    log.log("name", "null_word_replaced", '"Not Given" -> "NaN"', 1000)

    result = log.to_list()
    result.append({"column": "injected", "change_type": "x", "detail": "x", "count": 0})

    assert len(log.to_list()) == 1
    
def test_full_pipeline_clean_log():
    log = CleaningLog()

    log.log("name", "null_word_replaced", '"Not Given" -> "NaN"', 1000)
    log.log("country", "null_word_replaced", '"" -> "NaN"', 500)

    log.log("datetime", "datetime_parse_failed", 'coerced to NaT', 20)
    log.log("quantity", "numeric_parse_failed", "coerced to NaN", 1)

    log.log("all columns", "drop_duplicate_rows", "number of duplicate rows removed", 10)

    entries = log.to_list()

    assert len(entries) == 5
    assert not log.is_empty()

    change_types = [e["change_type"] for e in entries]
    assert "null_word_replaced"    in change_types
    assert "datetime_parse_failed" in change_types
    assert "numeric_parse_failed"  in change_types
    assert "drop_duplicate_rows" in change_types

    for entry in entries:
        assert isinstance(entry["count"], int)






