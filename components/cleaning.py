"""
Componente de limpieza de datos.
Permite eliminar duplicados, imputar nulos y cambiar tipos.
"""

import streamlit as st
import pandas as pd
from core.cleaner import DataCleaner
from core.data_loader import DataLoader
from config import IMPUTATION_STRATEGIES

def render_cleaning():
    """Renderiza la página de limpieza de datos."""
    
    st.title("🧹 Limpieza de Datos")
    st.markdown("---")
    
    if st.session_state.df is None:
        st.warning("⚠️ Primero carga un archivo en la sección 'Cargar Datos'")
        return
    
    # Trabajar con una copia
    df = st.session_state.df.copy()
    
    # Layout principal
    col_main, col_info = st.columns([2, 1])
    
    with col_info:
        st.markdown("### 📊 Estado Actual")
        st.metric("Filas", len(df))
        st.metric("Columnas", len(df.columns))
        st.metric("Valores Nulos", df.isnull().sum().sum())
        st.metric("Duplicados", df.duplicated().sum())
        
        st.markdown("---")
        st.markdown("### 🔄 Vista Previa")
        st.dataframe(df.head(5), use_container_width=True)
        
        if st.button("🔄 Restaurar datos originales", type="secondary"):
            # Recargar desde session state original
            st.rerun()
    
    with col_main:
        # Sección 1: Eliminar duplicados
        st.markdown("### 🗑️ Eliminar Duplicados")
        
        duplicates = df.duplicated().sum()
        
        if duplicates > 0:
            st.warning(f"Hay {duplicates} filas duplicadas en el dataset")
            
            if st.button("🗑️ Eliminar todas las filas duplicadas", type="primary"):
                df = DataCleaner.remove_duplicates(df)
                st.session_state.df = df
                st.success(f"✅ Se eliminaron {duplicates} filas duplicadas")
                st.rerun()
        else:
            st.success("✅ No hay filas duplicadas")
        
        st.markdown("---")
        
        # Sección 2: Manejar valores nulos
        st.markdown("### 🔧 Manejar Valores Nulos")
        
        cols_with_nulls = df.columns[df.isnull().any()].tolist()
        
        if cols_with_nulls:
            selected_col = st.selectbox(
                "Selecciona una columna con valores nulos",
                cols_with_nulls,
                key="null_col"
            )
            
            null_count = df[selected_col].isnull().sum()
            st.info(f"La columna '{selected_col}' tiene {null_count} valores nulos ({null_count/len(df)*100:.1f}%)")
            
            strategy = st.radio(
                "Estrategia de imputación",
                list(IMPUTATION_STRATEGIES.keys()),
                horizontal=True,
                key="impute_strategy"
            )
            
            if st.button("✅ Aplicar limpieza a esta columna", type="primary"):
                df = DataCleaner.fill_missing(
                    df, selected_col,
                    IMPUTATION_STRATEGIES[strategy]
                )
                st.session_state.df = df
                st.success(f"✅ Valores nulos procesados en '{selected_col}'")
                st.rerun()
            
            # Opción de aplicar a todas las columnas
            st.markdown("---")
            st.markdown("#### 🚀 Limpieza rápida")
            
            if st.button("⚡ Aplicar a TODAS las columnas con nulos", type="secondary"):
                for col in cols_with_nulls:
                    df = DataCleaner.fill_missing(df, col, IMPUTATION_STRATEGIES[strategy])
                st.session_state.df = df
                st.success(f"✅ Limpieza aplicada a {len(cols_with_nulls)} columnas")
                st.rerun()
        else:
            st.success("✅ No hay columnas con valores nulos")
        
        st.markdown("---")
        
        # Sección 3: Cambiar tipos de datos
        st.markdown("### 🔄 Convertir Tipos de Datos")
        
        col_to_change = st.selectbox(
            "Seleccionar columna para convertir",
            df.columns.tolist(),
            key="convert_col"
        )
        
        current_type = st.session_state.col_types.get(col_to_change, "desconocido")
        st.info(f"Tipo actual detectado: **{current_type}**")
        
        new_type = st.selectbox(
            "Convertir a",
            ["numérica", "texto", "fecha", "categórica"],
            key="new_type"
        )
        
        if st.button("🔄 Convertir tipo", type="primary"):
            try:
                if new_type == "numérica":
                    df[col_to_change] = pd.to_numeric(df[col_to_change], errors='coerce')
                elif new_type == "fecha":
                    df[col_to_change] = pd.to_datetime(df[col_to_change], errors='coerce')
                elif new_type == "texto":
                    df[col_to_change] = df[col_to_change].astype(str)
                elif new_type == "categórica":
                    df[col_to_change] = df[col_to_change].astype('category')
                
                st.session_state.df = df
                st.session_state.col_types = DataLoader.detect_column_types(df)
                st.success(f"✅ '{col_to_change}' convertido a {new_type}")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error en la conversión: {str(e)}")
        
        st.markdown("---")
        
        # Sección 4: Guardar cambios
        st.markdown("### 💾 Confirmar cambios")
        
        if st.button("💾 Guardar todos los cambios y continuar", type="primary", use_container_width=True):
            st.session_state.df = df
            st.success("✅ Cambios guardados exitosamente!")
            st.balloons()