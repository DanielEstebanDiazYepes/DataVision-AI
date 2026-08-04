import pandas as pd
import numpy as np

class DataInspector:
    @staticmethod
    def missing_values(df):
        missing = df.isnull().sum().reset_index()
        missing.columns = ['Columna', 'Nulos']
        missing['% Nulos'] = (missing['Nulos'] / len(df)) * 100
        return missing.sort_values('% Nulos', ascending=False)

    @staticmethod
    def duplicate_rows(df):
        return df.duplicated().sum()

    @staticmethod
    def detect_outliers(df, column):
        serie = df[column]
        # Convertir a numérico si no lo es
        if not pd.api.types.is_numeric_dtype(serie):
            serie = pd.to_numeric(serie, errors='coerce')
        Q1 = serie.quantile(0.25)
        Q3 = serie.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        return (serie < lower) | (serie > upper)