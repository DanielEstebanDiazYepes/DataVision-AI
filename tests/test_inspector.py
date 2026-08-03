from core.inspector import DataInspector

def test_missing_values(sample_df):
    missing = DataInspector.missing_values(sample_df)
    assert missing.loc[missing['Columna']=='nombre', 'Nulos'].values[0] == 1
    assert missing.loc[missing['Columna']=='edad', 'Nulos'].values[0] == 1

def test_duplicate_rows(sample_df_duplicates):
    assert DataInspector.duplicate_rows(sample_df_duplicates) == 1