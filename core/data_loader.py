"""
Módulo de carga de datos.
Soporta CSV, Excel y JSON con detección automática de tipos y coerción inteligente.
"""

import pandas as pd
import streamlit as st
from typing import Tuple, Dict

class DataLoader:
    """Maneja la carga de archivos y detección de tipos de datos."""

    # Patrones de nombre que fuerzan clasificación como categórica aunque sean numéricos
    CATEGORICAL_NAME_PATTERNS = [
        'id', 'year', 'año', 'codigo', 'code', 'numero', 'nro', 'zip', 'postal'
    ]

    @staticmethod
    @st.cache_data(show_spinner=False, ttl=3600)
    def load_file(uploaded_file) -> Tuple[pd.DataFrame, str]:
        """
        Carga el archivo subido y devuelve el DataFrame y nombre.
        Aplica coerción numérica automática antes de cualquier análisis.
        """
        filename = uploaded_file.name

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
            # Reintentar con encoding Latin-1
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='latin1')

        # Convertir columnas con números disfrazados de texto
        df = DataLoader._auto_coerce_numeric_columns(df)
        return df, filename

    @staticmethod
    def _auto_coerce_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Convierte columnas object a numéricas si la mayoría de los valores son convertibles.
        Los errores (letras) se convierten en NaN.
        """
        df = df.copy()
        for col in df.select_dtypes(include=['object']).columns:
            converted = pd.to_numeric(df[col], errors='coerce')
            valid_ratio = converted.notna().sum() / len(df)
            if valid_ratio > 0.5:   # al menos el 50 % son números
                df[col] = converted
        return df

    @staticmethod
    def detect_column_types(df: pd.DataFrame) -> Dict[str, str]:
        """Detecta el tipo de cada columna en el DataFrame."""
        col_types = {}
        for col in df.columns:
            col_types[col] = DataLoader._detect_single_column_type(df[col], col)
        return col_types

    @staticmethod
    def _detect_single_column_type(series: pd.Series, col_name: str = "") -> str:
        """Detecta el tipo de una columna individual, considerando el nombre."""

        # Si el nombre coincide con patrones de ID/año -> forzar categórica
        if any(pattern in col_name.lower() for pattern in DataLoader.CATEGORICAL_NAME_PATTERNS):
            return 'categórica'

        # Booleana
        if pd.api.types.is_bool_dtype(series):
            return 'booleana'

        # Numérica (ya incluye las coercionadas)
        if pd.api.types.is_numeric_dtype(series):
            # Si tiene muy pocos valores únicos, podría ser categórica disfrazada
            if series.nunique() / len(series) < 0.01 and len(series) > 20:
                return 'categórica'
            return 'numérica'

        # Fecha
        if pd.api.types.is_datetime64_any_dtype(series):
            return 'fecha'
        try:
            pd.to_datetime(series, errors='raise')
            return 'fecha'
        except (ValueError, TypeError):
            pass

        # Categórica vs Texto
        if len(series) > 0:
            unique_ratio = series.nunique() / len(series)
            if unique_ratio < 0.05 and len(series) > 10:
                return 'categórica'

        return 'texto'

    @staticmethod
    def get_column_types_dataframe(col_types: Dict[str, str]) -> pd.DataFrame:
        """Convierte el diccionario de tipos a DataFrame para visualización."""
        return pd.DataFrame(
            list(col_types.items()),
            columns=['Columna', 'Tipo Detectado']
        )