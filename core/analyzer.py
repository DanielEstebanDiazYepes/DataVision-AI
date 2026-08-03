import pandas as pd
import numpy as np

class Analyzer:
    """Cálculo de estadísticas y KPIs."""
    
    @staticmethod
    def basic_stats(df):
        """Estadísticas descriptivas básicas."""
        return df.describe(include='all').transpose()
    
    @staticmethod
    def correlation_matrix(df):
        """Matriz de correlación para columnas numéricas."""
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