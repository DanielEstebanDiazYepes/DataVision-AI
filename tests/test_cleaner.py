from core.cleaner import DataCleaner

def test_remove_duplicates(sample_df_duplicates):
    cleaned = DataCleaner.remove_duplicates(sample_df_duplicates)
    assert len(cleaned) == 3