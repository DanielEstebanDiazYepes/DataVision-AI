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

def render_ml_training():
    """Renderiza la página de entrenamiento de ML."""
    
    st.title("🤖 Machine Learning Automático")
    st.markdown("---")
    
    if st.session_state.df is None:
        st.warning("⚠️ Primero carga un archivo en la sección 'Cargar Datos'")
        return
    
    df = st.session_state.df
    
    # Configuración del modelo
    st.markdown("### ⚙️ Configuración del Modelo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        target = st.selectbox(
            "🎯 Variable Objetivo (Target)",
            df.columns.tolist(),
            key="ml_target"
        )
    
    with col2:
        problem_type = st.selectbox(
            "📊 Tipo de Problema",
            list(ML_PROBLEM_TYPES.keys()),
            key="ml_problem_type"
        )
    
    with col3:
        model_name = st.selectbox(
            "🤖 Algoritmo",
            list(ML_MODELS.keys()),
            key="ml_model"
        )
    
    # Información del target
    st.markdown("### 📋 Información de la variable objetivo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Tipo de dato", str(df[target].dtype))
    
    with col2:
        st.metric("Valores únicos", df[target].nunique())
    
    with col3:
        nulls = df[target].isnull().sum()
        st.metric("Valores nulos", nulls)
    
    if nulls > 0:
        st.warning(f"⚠️ La variable objetivo tiene {nulls} valores nulos. Serán eliminados automáticamente.")
    
    # Opciones avanzadas
    with st.expander("⚙️ Opciones avanzadas"):
        test_size = st.slider(
            "Tamaño del conjunto de prueba (%)",
            10, 40, 20,
            key="test_size"
        )
        random_state = st.number_input(
            "Semilla aleatoria",
            0, 100, 42,
            key="random_state"
        )
    
    # Botón de entrenamiento
    st.markdown("---")
    
    if st.button("🚀 Entrenar Modelo", type="primary", use_container_width=True):
        with st.spinner("🔄 Entrenando modelo... Esto puede tomar un momento"):
            try:
                # Crear y entrenar modelo
                engine = MLEngine(
                    df,
                    target,
                    problem_type=ML_PROBLEM_TYPES[problem_type]
                )
                
                # Modificar test_size si es necesario
                engine.test_size = test_size / 100
                engine.random_state = random_state
                
                engine.train(model_name=ML_MODELS[model_name])
                metrics = engine.evaluate()
                
                # Guardar en session state
                st.session_state.ml_engine = engine
                st.session_state.ml_metrics = metrics
                st.session_state.ml_trained = True
                
                st.success("✅ ¡Modelo entrenado exitosamente!")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error en el entrenamiento: {str(e)}")
                st.info("💡 Verifica que los datos estén limpios y la variable objetivo sea adecuada.")
                return
    
    # Mostrar resultados si ya se entrenó
    if st.session_state.get('ml_trained', False):
        st.markdown("---")
        st.markdown("## 📊 Resultados del Modelo")
        
        metrics = st.session_state.ml_metrics
        engine = st.session_state.ml_engine
        
        # Métricas principales
        st.markdown("### 📈 Métricas de Rendimiento")
        
        if engine.problem_type == 'regression':
            col1, col2, col3 = st.columns(3)
            
            with col1:
                r2 = metrics.get('R2', 0)
                st.metric(
                    "R² Score",
                    f"{r2:.4f}",
                    delta=f"{'Bueno' if r2 > 0.7 else 'Regular' if r2 > 0.5 else 'Bajo'}"
                )
            
            with col2:
                mae = metrics.get('MAE', 0)
                st.metric("MAE (Error Absoluto Medio)", f"{mae:.4f}")
            
            with col3:
                rmse = metrics.get('RMSE', 0)
                st.metric("RMSE (Raíz del Error Cuadrático Medio)", f"{rmse:.4f}")
            
            # Interpretación
            with st.expander("📖 Interpretación de métricas"):
                st.markdown(f"""
                - **R² Score ({r2:.4f}):** {'Excelente' if r2 > 0.9 else 'Bueno' if r2 > 0.7 else 'Regular' if r2 > 0.5 else 'Bajo'}. 
                  Indica qué proporción de la varianza explica el modelo.
                - **MAE ({mae:.4f}):** Error promedio en las mismas unidades que la variable objetivo.
                - **RMSE ({rmse:.4f}):** Penaliza más los errores grandes. También en unidades de la variable objetivo.
                """)
        else:
            accuracy = metrics.get('Accuracy', 0)
            st.metric("Accuracy (Precisión)", f"{accuracy:.2%}")
            
            # Reporte de clasificación
            if 'Report' in metrics:
                with st.expander("📋 Reporte detallado de clasificación"):
                    report_df = pd.DataFrame(metrics['Report']).transpose()
                    st.dataframe(report_df, use_container_width=True)
        
        # Gráficos
        st.markdown("### 📉 Visualizaciones del Modelo")
        
        tab1, tab2 = st.tabs(["Predicciones vs Reales", "Importancia de Características"])
        
        with tab1:
            fig = Visualizer.predictions_plot(engine)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            importance = engine.get_feature_importance()
            if importance:
                fig = Visualizer.feature_importance_plot(importance)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("La importancia de características solo está disponible para modelos basados en árboles.")
        
        # Exportar modelo
        st.markdown("### 💾 Exportar")
        
        if st.button("📥 Descargar métricas del modelo"):
            metrics_df = pd.DataFrame([metrics])
            csv = metrics_df.to_csv(index=False)
            st.download_button(
                "Descargar métricas (CSV)",
                csv,
                "metricas_modelo.csv",
                "text/csv"
            )