
import pandas as pd
import streamlit as st
import logging
from utils.logging_config import setup_logging
from typing import Tuple, Dict
import warnings

logger = setup_logging()

class DataLoader:

    CATEGORICAL_NAME_PATTERNS = [
        'id', 'year', 'año', 'codigo', 'code', 'numero', 'nro', 'zip', 'postal'
    ]

    @staticmethod
    @st.cache_data(show_spinner=False, ttl=3600)
    def load_file(uploaded_file) -> Tuple[pd.DataFrame, str]:
        filename = uploaded_file.name
        logger.info("Iniciando carga de archivo: %s", filename)

        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(uploaded_file, low_memory=False)
            elif filename.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            elif filename.endswith('.json'):
                df = pd.read_json(uploaded_file)
            else:
                raise ValueError(f"Formato no soportado: {filename}")
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='latin1')

        df = DataLoader._auto_coerce_numeric_columns(df)
        logger.info("Archivo cargado: %s | Filas: %s | Columnas: %s", filename, df.shape[0], df.shape[1])
        return df, filename

    @staticmethod
    def _auto_coerce_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        converted_cols = []
        for col in df.select_dtypes(include=['object']).columns:
            converted = pd.to_numeric(df[col], errors='coerce')
            valid_ratio = converted.notna().sum() / len(df)
            if valid_ratio > 0.5:
                df[col] = converted
                converted_cols.append(col)
        if converted_cols:
            logger.info("Columnas convertidas a numéricas: %s", converted_cols)
        return df

    @staticmethod
    def detect_column_types(df: pd.DataFrame) -> Dict[str, str]:
        logger.info("Detectando tipos de columnas...")
        col_types = {}
        for col in df.columns:
            col_types[col] = DataLoader._detect_single_column_type(df[col], col)
        logger.info("Tipos detectados: %s", col_types)
        return col_types

    @staticmethod
    def _detect_single_column_type(series: pd.Series, col_name: str = "") -> str:
        if any(pattern in col_name.lower() for pattern in DataLoader.CATEGORICAL_NAME_PATTERNS):
            return 'categórica'
        if pd.api.types.is_bool_dtype(series):
            return 'booleana'
        if pd.api.types.is_numeric_dtype(series):
            if series.nunique() / len(series) < 0.01 and len(series) > 20:
                return 'categórica'
            return 'numérica'
        if pd.api.types.is_datetime64_any_dtype(series):
            return 'fecha'
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                pd.to_datetime(series, errors='raise')
            return 'fecha'
        except (ValueError, TypeError):
            pass
        if len(series) > 0:
            unique_ratio = series.nunique() / len(series)
            if unique_ratio < 0.05 and len(series) > 10:
                return 'categórica'
        return 'texto'

    @staticmethod
    def get_column_types_dataframe(col_types: Dict[str, str]) -> pd.DataFrame:
        return pd.DataFrame(list(col_types.items()), columns=['Columna', 'Tipo Detectado'])
