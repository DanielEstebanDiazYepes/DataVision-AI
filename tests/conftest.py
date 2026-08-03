import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def sample_df():
    """DataFrame pequeño con diferentes tipos y algunos nulos."""
    data = {
        'id': [1, 2, 3, 4, 5],
        'nombre': ['Ana', 'Luis', 'María', None, 'Carlos'],
        'edad': [25, 30, np.nan, 40, 35],
        'salario': [50000, 60000, 75000, 80000, 95000],
        'fecha': pd.to_datetime(['2023-01-01', '2023-02-15', '2023-03-10', '2023-04-20', '2023-05-05']),
        'activo': [True, False, True, False, True]
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_df_duplicates():
    """DataFrame con filas duplicadas."""
    data = {'x': [1, 2, 2, 3], 'y': [10, 20, 20, 30]}
    return pd.DataFrame(data)