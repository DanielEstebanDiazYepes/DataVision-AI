import pandas as pd
import streamlit as st
from typing import Tuple

class DataLoader:
    """Maneja la carga de archivos CSV, Excel, JSON con detección de tipos."""
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def load_file(uploaded_file) -> Tuple[pd.DataFrame, str]:
        """
        Carga el archivo subido y devuelve el DataFrame y el nombre del archivo.
        Usa caché de Streamlit para no recargar el mismo archivo dos veces.
        """
        filename = uploaded_file.name
        if filename.endswith('.csv'):
            # Para archivos grandes: leer en chunks y concatenar
            try:
                df = pd.read_csv(uploaded_file, low_memory=False)
            except UnicodeDecodeError:
                # Intentar con encoding común
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='latin1')
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        elif filename.endswith('.json'):
            df = pd.read_json(uploaded_file)
        else:
            raise ValueError("Formato no soportado. Use CSV, Excel o JSON.")
        return df, filename

    @staticmethod
    def detect_column_types(df: pd.DataFrame) -> dict:
        """
        Clasifica cada columna en: numérica, categórica, fecha, booleana, texto.
        Escalable: utiliza inferencia de Pandas y heurísticas.
        """
        col_types = {}
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                col_types[col] = 'numérica'
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                col_types[col] = 'fecha'
            elif pd.api.types.is_bool_dtype(df[col]):
                col_types[col] = 'booleana'
            else:
                # Intentar convertir a datetime
                try:
                    pd.to_datetime(df[col], errors='raise')
                    col_types[col] = 'fecha'
                except:
                    # Si tiene pocos valores únicos vs tamaño, considerar categórica
                    if df[col].nunique() / len(df) < 0.05 and len(df) > 10:
                        col_types[col] = 'categórica'
                    else:
                        col_types[col] = 'texto'
        return col_types