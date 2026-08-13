import pandas as pd
import logging
from utils.logging_config import setup_logging

logger = setup_logging()

class DataCleaner:
    @staticmethod
    def remove_duplicates(df):
        antes = len(df)
        result = df.drop_duplicates().copy()
        despues = len(result)
        logger.info("Eliminadas %s filas duplicadas (de %s a %s)", antes - despues, antes, despues)
        return result

    @staticmethod
    def fill_missing(df, column, strategy='mean'):
        logger.info("Imputando nulos en '%s' con estrategia '%s'", column, strategy)
        df_clean = df.copy()
        if strategy in ['mean', 'median']:
            df_clean[column] = pd.to_numeric(df_clean[column], errors='coerce')

        if strategy == 'mean':
            fill_value = df_clean[column].mean()
        elif strategy == 'median':
            fill_value = df_clean[column].median()
        elif strategy == 'mode':
            fill_value = df_clean[column].mode()[0] if not df_clean[column].mode().empty else None
        elif strategy == 'drop':
            antes = len(df_clean)
            df_clean = df_clean.dropna(subset=[column])
            despues = len(df_clean)
            logger.info("Filas eliminadas por nulos en '%s': %s", column, antes - despues)
            return df_clean
        else:
            logger.error("Estrategia no soportada: %s", strategy)
            raise ValueError(f"Estrategia no soportada: {strategy}")

        if fill_value is not None and not pd.isna(fill_value):
            df_clean[column] = df_clean[column].fillna(fill_value)
            logger.info("Se rellenaron %s nulos en '%s'", df[column].isnull().sum(), column)
        return df_clean