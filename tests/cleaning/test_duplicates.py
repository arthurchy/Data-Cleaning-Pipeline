import pandas as pd
from app.cleaning.duplicates import drop_duplicate_default

def test_drops_duplicate_rows(df_with_duplicates):
    result = drop_duplicate_default(df_with_duplicates)
    assert len(result) == 2

def test_keeps_first_occurrence(df_with_duplicates):
    result = drop_duplicate_default(df_with_duplicates)
    assert result.iloc[0]["name"] == "Alice"  # first Alice kept, not second
    assert result.iloc[1]["name"] == "Bob"
    
def test_no_duplicates_unchanged(sample_df):
    result = drop_duplicate_default(sample_df)
    assert len(result) == len(sample_df)
    pd.testing.assert_frame_equal(result, sample_df)