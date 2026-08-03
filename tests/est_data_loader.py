import pytest
import pandas as pd
from core.data_loader import DataLoader
from io import BytesIO

def test_detect_column_types(sample_df):
    types = DataLoader.detect_column_types(sample_df)
    assert types['id'] == 'numérica'
    assert types['edad'] == 'numérica'
    assert types['nombre'] == 'categórica'  # por heurística (pocos únicos)
    assert types['fecha'] == 'fecha'
    assert types['activo'] == 'booleana'

def test_load_file_csv():
    csv_content = b"col1,col2\n1,2\n3,4"
    file = BytesIO(csv_content)
    file.name = "test.csv"
    df, name = DataLoader.load_file(file)
    assert name == "test.csv"
    assert df.shape == (2, 2)