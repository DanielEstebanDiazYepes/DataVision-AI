"""
Componente de dashboard interactivo.
Muestra KPIs, gráficos y análisis visual de los datos.
"""

import streamlit as st
import pandas as pd
import numpy as np
from core.analyzer import Analyzer
from core.visualizer import Visualizer
import logging
from utils.logging_config import setup_logging
import warnings


logger = setup_logging()

def render_dashboard():
    st.title("Dashboard Interactivo")
    st.markdown("---")

    if st.session_state.df is None:
        st.warning("Primero carga un archivo en la sección 'Cargar Datos'")
        return

    df = st.session_state.df
    col_types = st.session_state.col_types
    logger.info("Renderizando Dashboard")

    # KPIs principales
    st.markdown("### Indicadores Clave (KPIs)")
    stats = Analyzer.basic_stats(df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Registros", f"{len(df):,}")
    col2.metric("Total Columnas", len(df.columns))
    num_cols = len(df.select_dtypes(include=[np.number]).columns)
    col3.metric("Columnas Numéricas", num_cols)
    cat_cols = len(df.select_dtypes(include=['object', 'category']).columns)
    col4.metric("Columnas Texto", cat_cols)
    st.markdown("---")

    st.markdown("### Visualizaciones")
    viz_type = st.selectbox(
        "Selecciona el tipo de análisis",
        ["Distribución de variables", "Matriz de correlación",
         "Comparación categórica", "Serie temporal",
         "Composición", "Estadísticas descriptivas"],
        key="viz_type"
    )

    if viz_type == "Distribución de variables":
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            col = st.selectbox("Selecciona una variable numérica", num_cols, key="dist_col")
            chart_type = st.radio("Tipo de gráfico", ["Histograma", "Box Plot", "Violin Plot"], horizontal=True, key="dist_chart_type")
            if chart_type == "Histograma":
                bins = st.slider("Número de bins", 10, 100, 30)
                fig = Visualizer.distribution_plot(df, col, 'histogram', bins=bins)
            elif chart_type == "Box Plot":
                fig = Visualizer.distribution_plot(df, col, 'box')
            else:
                fig = Visualizer.distribution_plot(df, col, 'violin')
            st.plotly_chart(fig, width='stretch')
            with st.expander("Ver estadísticas detalladas"):
                st.dataframe(df[col].describe(), width='stretch')
        else:
            st.warning("No hay columnas numéricas disponibles")

    elif viz_type == "Matriz de correlación":
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(num_cols) > 1:
            st.markdown("### Relación entre variables numéricas")
            selected_cols = st.multiselect("Selecciona columnas para la matriz (mínimo 2)", num_cols,
                                           default=num_cols[:min(5, len(num_cols))], key="corr_cols")
            if len(selected_cols) >= 2:
                fig = Visualizer.correlation_heatmap(df[selected_cols])
                st.plotly_chart(fig, width='stretch')
                st.markdown("### Matriz de dispersión")
                fig_scatter = Visualizer.scatter_matrix(df[selected_cols])
                st.plotly_chart(fig_scatter, width='stretch')
            else:
                st.warning("Selecciona al menos 2 columnas")
        else:
            st.warning("Se necesitan al menos 2 columnas numéricas")

    elif viz_type == "Comparación categórica":
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if cat_cols and num_cols:
            col1, col2 = st.columns(2)
            cat_col = col1.selectbox("Variable categórica", cat_cols, key="comp_cat")
            num_col = col2.selectbox("Variable numérica", num_cols, key="comp_num")
            agg_func = st.selectbox("Función de agregación", ["mean", "sum", "count", "min", "max", "std"], key="agg_func")
            fig = Visualizer.comparison_plot(df, cat_col, num_col, agg_func)
            st.plotly_chart(fig, width='stretch')
        else:
            st.warning("Se necesitan columnas categóricas y numéricas")

    elif viz_type == "Serie temporal":
        date_cols = [col for col, type_ in col_types.items() if type_ == 'fecha']
        if not date_cols:
            potential_dates = df.select_dtypes(include=['object']).columns.tolist()
            date_cols = []
            for col in potential_dates:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    try:
                        pd.to_datetime(df[col])
                        date_cols.append(col)
                    except:
                        pass
        if date_cols:
            date_col = st.selectbox("Columna de fecha", date_cols, key="ts_date")
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if num_cols:
                value_col = st.selectbox("Columna de valores", num_cols, key="ts_value")
                freq = st.selectbox("Frecuencia de agregación", ["D", "W", "M", "Q", "Y"],
                                    format_func=lambda x: {"D":"Diaria","W":"Semanal","M":"Mensual","Q":"Trimestral","Y":"Anual"}[x],
                                    key="ts_freq")
                fig = Visualizer.time_series_plot(df, date_col, value_col, freq)
                st.plotly_chart(fig, width='stretch')
            else:
                st.warning("No hay columnas numéricas para el eje Y")
        else:
            st.warning("No se detectaron columnas de fecha")

    elif viz_type == "Composición":
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if cat_cols:
            cat_col = st.selectbox("Variable para composición", cat_cols, key="pie_cat")
            top_n = st.slider("Número de categorías a mostrar", 5, 20, 10)
            fig = Visualizer.pie_chart(df, cat_col, top_n)
            st.plotly_chart(fig, width='stretch')
        else:
            st.warning("No hay columnas categóricas disponibles")

    elif viz_type == "Estadísticas descriptivas":
        st.markdown("### Resumen estadístico completo")
        stats = Analyzer.basic_stats(df)
        if stats['num_stats'] is not None:
            st.markdown("#### Variables Numéricas")
            st.dataframe(stats['num_stats'], width='stretch')
        if stats['cat_stats'] is not None:
            st.markdown("#### Variables Categóricas")
            # Convertir todo a string para evitar problemas de tipos mixtos
            cat_stats_str = stats['cat_stats'].astype(str)
            st.dataframe(cat_stats_str, width='stretch')
        if stats['num_stats'] is not None:
            csv = stats['num_stats'].to_csv()
            st.download_button("Descargar estadísticas (CSV)", csv, "estadisticas.csv", "text/csv")