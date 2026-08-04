import pandas as pd
import numpy as np

class Analyzer:
    """Cálculo de estadísticas y KPIs."""

    @staticmethod
    def basic_stats(df):
        """
        Devuelve estadísticas descriptivas separadas para variables numéricas y categóricas.
        """
        num_df = df.select_dtypes(include=[np.number])
        cat_df = df.select_dtypes(include=['object', 'category'])
        return {
            'num_stats': num_df.describe() if not num_df.empty else None,
            'cat_stats': cat_df.describe() if not cat_df.empty else None
        }

    @staticmethod
    def correlation_matrix(df):
        """Matriz de correlación solo para columnas numéricas."""
        return df.select_dtypes(include=np.number).corr()

    @staticmethod
    def column_summary(df, col):
        """Resumen detallado de una columna."""
        summary = {
            'Tipo': str(df[col].dtype),
            'Nulos': df[col].isnull().sum(),
            'Únicos': df[col].nunique(),
            'Nulos %': f"{(df[col].isnull().sum()/len(df))*100:.2f}%"
        }
        return summary