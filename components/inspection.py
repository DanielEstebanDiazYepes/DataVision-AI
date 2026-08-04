"""
Componente de inspección de datos.
Muestra análisis de tipos, nulos, duplicados y outliers.
"""

import streamlit as st
import pandas as pd
from core.inspector import DataInspector
from core.visualizer import Visualizer

def render_inspection():
    st.title("🔍 Inspección de Datos")
    st.markdown("---")

    if st.session_state.df is None:
        st.warning("⚠️ Primero carga un archivo en la sección 'Cargar Datos'")
        return

    df = st.session_state.df
    col_types = st.session_state.col_types

    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Tipos de Datos", "🔍 Valores Nulos", "🔄 Duplicados", "📊 Outliers"
    ])

    with tab1:
        st.markdown("### Tipos de Columnas Detectados")
        types_df = pd.DataFrame(list(col_types.items()), columns=['Columna', 'Tipo Detectado'])
        types_df['Valores Únicos'] = [df[col].nunique() for col in types_df['Columna']]
        types_df['Nulos'] = [df[col].isnull().sum() for col in types_df['Columna']]
        st.dataframe(types_df, use_container_width=True)

        st.markdown("### Distribución de Tipos")
        type_counts = types_df['Tipo Detectado'].value_counts()
        col1, col2 = st.columns([1, 2])
        with col1:
            for tipo, count in type_counts.items():
                st.metric(f"📊 {tipo.capitalize()}", count)
        with col2:
            fig = Visualizer.type_distribution_pie(type_counts)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### Análisis de Valores Nulos")
        missing = DataInspector.missing_values(df)
        total_nulls = missing['Nulos'].sum()

        if total_nulls == 0:
            st.success("✅ No se encontraron valores nulos en el dataset")
            st.balloons()
        else:
            st.warning(f"⚠️ Se encontraron {total_nulls:,} valores nulos en {len(missing[missing['Nulos']>0])} columnas")
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("#### Columnas con valores nulos")
                cols_with_nulls = missing[missing['Nulos'] > 0].copy()
                cols_with_nulls['% Nulos'] = cols_with_nulls['% Nulos'].map('{:.2f}%'.format)
                st.dataframe(cols_with_nulls[['Columna', 'Nulos', '% Nulos']], use_container_width=True)
            with col2:
                st.markdown("#### Visualización de nulos")
                fig = Visualizer.missing_values_plot(missing)
                st.plotly_chart(fig, use_container_width=True)

            completitud = (1 - total_nulls / (len(df) * len(df.columns))) * 100
            st.markdown(f"**Completitud general del dataset:** {completitud:.1f}%")
            st.progress(int(completitud))

    with tab3:
        st.markdown("### Análisis de Duplicados")
        duplicates = DataInspector.duplicate_rows(df)
        duplicate_percentage = (duplicates / len(df)) * 100 if len(df) > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Filas Totales", len(df))
        col2.metric("Filas Duplicadas", duplicates)
        col3.metric("% Duplicados", f"{duplicate_percentage:.2f}%")

        if duplicates == 0:
            st.success("✅ No se encontraron filas duplicadas")
        else:
            st.warning(f"⚠️ Se encontraron {duplicates} filas duplicadas")
            if st.button("👁️ Mostrar filas duplicadas"):
                duplicated_mask = df.duplicated(keep=False)
                st.dataframe(df[duplicated_mask], use_container_width=True)

    with tab4:
        st.markdown("### Detección de Outliers (Método IQR)")
        numeric_cols = [col for col, type_ in col_types.items() if type_ == 'numérica']

        if numeric_cols:
            selected_col = st.selectbox("Selecciona una columna numérica para analizar", numeric_cols, key="outlier_col")
            outliers_mask = DataInspector.detect_outliers(df, selected_col)
            n_outliers = outliers_mask.sum()
            outlier_pct = (n_outliers / len(df)) * 100 if len(df) > 0 else 0

            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Registros", len(df))
            col2.metric("Outliers Detectados", n_outliers)
            col3.metric("% Outliers", f"{outlier_pct:.2f}%")

            if n_outliers > 0:
                fig = Visualizer.outlier_plot(df, selected_col, outliers_mask)
                st.plotly_chart(fig, use_container_width=True)
                with st.expander("👁️ Ver registros con outliers"):
                    st.dataframe(df[outliers_mask], use_container_width=True)
            else:
                st.success(f"✅ No se detectaron outliers en '{selected_col}'")
        else:
            st.info("ℹ️ No hay columnas numéricas para analizar outliers")