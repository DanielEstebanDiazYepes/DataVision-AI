import pandas as pd
import numpy as np

class DataInspector:
    """Detecta nulos, duplicados, columnas vacías, outliers (IQR) y errores de formato."""
    
    @staticmethod
    def missing_values(df: pd.DataFrame) -> pd.DataFrame:
        missing = df.isnull().sum().reset_index()
        missing.columns = ['Columna', 'Nulos']
        missing['% Nulos'] = (missing['Nulos'] / len(df)) * 100
        return missing.sort_values('% Nulos', ascending=False)
    
    @staticmethod
    def duplicate_rows(df: pd.DataFrame) -> int:
        return df.duplicated().sum()
    
    @staticmethod
    def empty_columns(df: pd.DataFrame) -> list:
        return [col for col in df.columns if df[col].dropna().empty]
    
    @staticmethod
    def detect_outliers(df: pd.DataFrame, column: str) -> pd.Series:
        """Outliers usando IQR. Solo para columnas numéricas."""
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        return (df[column] < lower) | (df[column] > upper)