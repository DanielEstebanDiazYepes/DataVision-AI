"""
Componente de Machine Learning.
Entrenamiento automático de modelos de regresión y clasificación.
"""

import streamlit as st
import pandas as pd
import numpy as np
from core.ml_engine import MLEngine
from core.visualizer import Visualizer
from config import ML_MODELS, ML_PROBLEM_TYPES
import logging
from utils.logging_config import setup_logging

logger = setup_logging()

def render_ml_training():
    st.title("Machine Learning Automático")
    st.markdown("---")

    if st.session_state.df is None:
        st.warning("Primero carga un archivo en la sección 'Cargar Datos'")
        return

    df = st.session_state.df
    logger.info("Renderizando ML Training")

    st.markdown("### Configuración del Modelo")
    col1, col2, col3 = st.columns(3)

    with col1:
        target = st.selectbox("Variable Objetivo (Target)", df.columns.tolist(), key="ml_target")
    with col2:
        problem_type = st.selectbox("Tipo de Problema", list(ML_PROBLEM_TYPES.keys()), key="ml_problem_type")
    with col3:
        model_name = st.selectbox("Algoritmo", list(ML_MODELS.keys()), key="ml_model")

    st.markdown("### Información de la variable objetivo")
    col1, col2, col3 = st.columns(3)
    col1.metric("Tipo de dato", str(df[target].dtype))
    col2.metric("Valores únicos", df[target].nunique())
    nulls = df[target].isnull().sum()
    col3.metric("Valores nulos", nulls)
    if nulls > 0:
        st.warning(f"La variable objetivo tiene {nulls} valores nulos. Serán eliminados automáticamente.")

    with st.expander("Opciones avanzadas"):
        test_size = st.slider("Tamaño del conjunto de prueba (%)", 10, 40, 20, key="test_size")
        random_state = st.number_input("Semilla aleatoria", 0, 100, 42, key="random_state")

    st.markdown("---")
    if st.button("Entrenar Modelo", type="primary", width='stretch'):
        with st.spinner("Entrenando modelo..."):
            try:
                engine = MLEngine(df, target, problem_type=ML_PROBLEM_TYPES[problem_type])
                engine.test_size = test_size / 100
                engine.random_state = random_state
                engine.train(model_name=ML_MODELS[model_name])
                metrics = engine.evaluate()
                st.session_state.ml_engine = engine
                st.session_state.ml_metrics = metrics
                st.session_state.ml_trained = True
                st.success("Modelo entrenado exitosamente")
            except Exception as e:
                logger.error(f"Error entrenando modelo: {e}")
                st.error(f"Error en el entrenamiento: {str(e)}")
                st.info("Verifica que los datos estén limpios y la variable objetivo sea adecuada.")
                return

    if st.session_state.get('ml_trained', False):
        st.markdown("---")
        st.markdown("## Resultados del Modelo")
        metrics = st.session_state.ml_metrics
        engine = st.session_state.ml_engine

        st.markdown("### Métricas de Rendimiento")
        if engine.problem_type == 'regression':
            col1, col2, col3 = st.columns(3)
            r2 = metrics.get('R2', 0)
            col1.metric("R² Score", f"{r2:.4f}")
            col2.metric("MAE", f"{metrics.get('MAE', 0):.4f}")
            col3.metric("RMSE", f"{metrics.get('RMSE', 0):.4f}")
            with st.expander("Interpretación de métricas"):
                st.markdown(f"R²: {r2:.4f} - {'Excelente' if r2>0.9 else 'Bueno' if r2>0.7 else 'Regular' if r2>0.5 else 'Bajo'}")
        else:
            accuracy = metrics.get('Accuracy', 0)
            st.metric("Accuracy", f"{accuracy:.2%}")
            if 'Report' in metrics:
                with st.expander("Reporte detallado de clasificación"):
                    report_df = pd.DataFrame(metrics['Report']).transpose()
                    st.dataframe(report_df, width='stretch')

        st.markdown("### Visualizaciones del Modelo")
        tab1, tab2 = st.tabs(["Predicciones vs Reales", "Importancia de Características"])
        with tab1:
            fig = Visualizer.predictions_plot(engine)
            st.plotly_chart(fig, width='stretch')
        with tab2:
            importance = engine.get_feature_importance()
            if importance:
                fig = Visualizer.feature_importance_plot(importance)
                st.plotly_chart(fig, width='stretch')
            else:
                st.info("La importancia de características solo está disponible para modelos basados en árboles.")

        st.markdown("### Exportar")
        if st.button("Descargar métricas del modelo"):
            metrics_df = pd.DataFrame([metrics])
            csv = metrics_df.to_csv(index=False)
            st.download_button("Descargar métricas (CSV)", csv, "metricas_modelo.csv", "text/csv")