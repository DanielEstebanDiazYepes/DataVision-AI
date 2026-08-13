import pandas as pd
import numpy as np
import logging
from utils.logging_config import setup_logging

logger = setup_logging()

class DataInspector:
    @staticmethod
    def missing_values(df):
        logger.info("Calculando valores nulos...")
        missing = df.isnull().sum().reset_index()
        missing.columns = ['Columna', 'Nulos']
        missing['% Nulos'] = (missing['Nulos'] / len(df)) * 100
        result = missing.sort_values('% Nulos', ascending=False)
        logger.info("Nulos totales: %s", result['Nulos'].sum())
        return result

    @staticmethod
    def duplicate_rows(df):
        dups = df.duplicated().sum()
        logger.info("Filas duplicadas: %s", dups)
        return dups

    @staticmethod
    def detect_outliers(df, column):
        logger.info("Detectando outliers en columna '%s'", column)
        serie = df[column]
        if not pd.api.types.is_numeric_dtype(serie):
            serie = pd.to_numeric(serie, errors='coerce')
        Q1 = serie.quantile(0.25)
        Q3 = serie.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = (serie < lower) | (serie > upper)
        logger.info("Outliers en '%s': %s", column, outliers.sum())
        return outliers