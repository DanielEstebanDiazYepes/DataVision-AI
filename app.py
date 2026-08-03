import streamlit as st
import pandas as pd
import time
from core.data_loader import DataLoader
from core.inspector import DataInspector
from core.cleaner import DataCleaner
from core.analyzer import Analyzer
from core.visualizer import Visualizer
from core.ml_engine import MLEngine
from core.exporter import export_data

# Configuración de la página
st.set_page_config(
    page_title="DataVision AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para tema oscuro profesional
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stApp { background-color: #0e1117; }
    .css-1d391kg { background-color: #262730; }
    .st-bb { background-color: #262730; }
    .st-at { background-color: #262730; }
    h1, h2, h3, h4, h5, h6 { color: #ffffff; }
    p, span, div { color: #e0e0e0; }
    .stDataFrame { background-color: #1e1e1e; }
    .metric-card {
        background-color: #1e3a5f;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #4da6ff;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #b0b0b0;
    }
</style>
""", unsafe_allow_html=True)

# Inicialización del estado de sesión
if 'df' not in st.session_state:
    st.session_state.df = None
if 'filename' not in st.session_state:
    st.session_state.filename = None
if 'col_types' not in st.session_state:
    st.session_state.col_types = None
if 'cleaned_df' not in st.session_state:
    st.session_state.cleaned_df = None

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/data-configuration.png", width=80)
    st.title("DataVision AI")
    st.markdown("---")
    
    # Navegación
    menu = st.radio(
        "📋 Navegación",
        ["🏠 Inicio", "📤 Cargar Datos", "🔍 Inspección", "🧹 Limpieza", 
         "📊 Dashboard", "🤖 Machine Learning", "📥 Exportar"]
    )
    
    st.markdown("---")
    st.markdown("### ℹ️ Acerca de")
    st.info("DataVision AI v1.0 - Plataforma inteligente de análisis de datos")

# Contenido principal
if menu == "🏠 Inicio":
    st.title("🌟 Bienvenido a DataVision AI")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📤 Carga Inteligente")
        st.write("Soporta CSV, Excel y JSON. Detecta automáticamente tipos de datos.")
    
    with col2:
        st.markdown("### 🔍 Análisis Profundo")
        st.write("Identifica nulos, duplicados, outliers y genera estadísticas completas.")
    
    with col3:
        st.markdown("### 🤖 ML Automático")
        st.write("Entrena modelos de regresión y clasificación con un solo clic.")
    
    st.markdown("---")
    st.markdown("### 🚀 Comienza cargando tu archivo de datos")
    
    if st.button("Ir a Cargar Datos →"):
        st.session_state.menu = "📤 Cargar Datos"

elif menu == "📤 Cargar Datos":
    st.title("📤 Cargar Archivo de Datos")
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "Selecciona un archivo (CSV, Excel, JSON)",
        type=["csv", "xlsx", "json"],
        help="Arrastra y suelta tu archivo aquí o haz clic para seleccionarlo"
    )
    
    if uploaded_file is not None:
        with st.spinner("Cargando y analizando archivo..."):
            try:
                df, filename = DataLoader.load_file(uploaded_file)
                st.session_state.df = df
                st.session_state.filename = filename
                st.session_state.col_types = DataLoader.detect_column_types(df)
                
                st.success(f"✅ Archivo cargado exitosamente: **{filename}**")
                
                # Mostrar preview
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📊 Filas", df.shape[0])
                with col2:
                    st.metric("📋 Columnas", df.shape[1])
                with col3:
                    st.metric("🔢 Numéricas", sum(1 for v in st.session_state.col_types.values() if v == 'numérica'))
                with col4:
                    st.metric("📝 Categóricas", sum(1 for v in st.session_state.col_types.values() if v == 'categórica'))
                
                st.markdown("### Vista previa de los datos")
                st.dataframe(df.head(10), use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error al cargar el archivo: {str(e)}")
    else:
        st.info("ℹ️ Esperando a que cargues un archivo...")

elif menu == "🔍 Inspección":
    st.title("🔍 Inspección de Datos")
    st.markdown("---")
    
    if st.session_state.df is None:
        st.warning("⚠️ Primero carga un archivo en la sección 'Cargar Datos'")
    else:
        df = st.session_state.df
        
        # Pestañas de inspección
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Tipos de Datos", "🔍 Valores Nulos", "🔄 Duplicados", "📊 Outliers"])
        
        with tab1:
            st.markdown("### Tipos de Columnas Detectados")
            types_df = pd.DataFrame(
                list(st.session_state.col_types.items()),
                columns=['Columna', 'Tipo Detectado']
            )
            st.dataframe(types_df, use_container_width=True)
        
        with tab2:
            st.markdown("### Análisis de Valores Nulos")
            missing = DataInspector.missing_values(df)
            
            if missing['Nulos'].sum() == 0:
                st.success("✅ No se encontraron valores nulos en el dataset")
            else:
                st.warning(f"⚠️ Se encontraron {missing['Nulos'].sum()} valores nulos")
                
                # Gráfico de nulos
                fig = Visualizer.missing_values_plot(missing)
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(missing[missing['Nulos'] > 0], use_container_width=True)
        
        with tab3:
            st.markdown("### Análisis de Duplicados")
            duplicates = DataInspector.duplicate_rows(df)
            
            if duplicates == 0:
                st.success("✅ No se encontraron filas duplicadas")
            else:
                st.warning(f"⚠️ Se encontraron {duplicates} filas duplicadas")
                if st.button("Ver filas duplicadas"):
                    st.dataframe(df[df.duplicated(keep=False)], use_container_width=True)
        
        with tab4:
            st.markdown("### Detección de Outliers (IQR)")
            numeric_cols = [col for col, type_ in st.session_state.col_types.items() if type_ == 'numérica']
            
            if numeric_cols:
                selected_col = st.selectbox("Selecciona una columna numérica", numeric_cols)
                outliers = DataInspector.detect_outliers(df, selected_col)
                n_outliers = outliers.sum()
                
                st.metric("Outliers Detectados", n_outliers)
                
                if n_outliers > 0:
                    fig = Visualizer.outlier_plot(df, selected_col, outliers)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay columnas numéricas para analizar outliers")

elif menu == "🧹 Limpieza":
    st.title("🧹 Limpieza de Datos")
    st.markdown("---")
    
    if st.session_state.df is None:
        st.warning("⚠️ Primero carga un archivo en la sección 'Cargar Datos'")
    else:
        df = st.session_state.df.copy()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Opciones de Limpieza")
            
            # Eliminar duplicados
            if st.button("🗑️ Eliminar Filas Duplicadas"):
                df = DataCleaner.remove_duplicates(df)
                st.success("✅ Filas duplicadas eliminadas")
                st.session_state.df = df
            
            st.markdown("---")
            
            # Manejo de nulos
            st.markdown("### 🔧 Manejar Valores Nulos")
            
            # Seleccionar columna
            cols_with_nulls = df.columns[df.isnull().any()].tolist()
            
            if cols_with_nulls:
                selected_col = st.selectbox("Columna con nulos", cols_with_nulls)
                
                strategy = st.radio(
                    "Estrategia de imputación",
                    ["Media", "Mediana", "Moda", "Eliminar filas"],
                    horizontal=True
                )
                
                if st.button("✅ Aplicar Limpieza"):
                    strategy_map = {
                        "Media": "mean",
                        "Mediana": "median",
                        "Moda": "mode",
                        "Eliminar filas": "drop"
                    }
                    df = DataCleaner.fill_missing(df, selected_col, strategy_map[strategy])
                    st.success(f"✅ Valores nulos procesados en columna '{selected_col}'")
                    st.session_state.df = df
            else:
                st.success("✅ No hay columnas con valores nulos")
            
            st.markdown("---")
            
            # Cambiar tipo de dato
            st.markdown("### 🔄 Cambiar Tipo de Dato")
            col_to_change = st.selectbox("Seleccionar columna", df.columns.tolist())
            new_type = st.selectbox("Nuevo tipo", ["numérica", "texto", "fecha", "categórica"])
            
            if st.button("🔄 Convertir Tipo"):
                try:
                    if new_type == "numérica":
                        df[col_to_change] = pd.to_numeric(df[col_to_change], errors='coerce')
                    elif new_type == "fecha":
                        df[col_to_change] = pd.to_datetime(df[col_to_change], errors='coerce')
                    elif new_type == "texto":
                        df[col_to_change] = df[col_to_change].astype(str)
                    st.success(f"✅ Columna '{col_to_change}' convertida a {new_type}")
                    st.session_state.df = df
                    st.session_state.col_types = DataLoader.detect_column_types(df)
                except Exception as e:
                    st.error(f"Error en la conversión: {str(e)}")
        
        with col2:
            st.markdown("### 📊 Datos Actuales")
            st.metric("Filas", len(df))
            st.metric("Columnas", len(df.columns))
            st.dataframe(df.head(5), use_container_width=True)

elif menu == "📊 Dashboard":
    st.title("📊 Dashboard Interactivo")
    st.markdown("---")
    
    if st.session_state.df is None:
        st.warning("⚠️ Primero carga un archivo en la sección 'Cargar Datos'")
    else:
        df = st.session_state.df
        
        # KPIs
        st.markdown("### 📈 Indicadores Clave (KPIs)")
        col1, col2, col3, col4 = st.columns(4)
        
        stats = Analyzer.basic_stats(df)
        
        with col1:
            st.metric("📊 Total Registros", len(df))
        with col2:
            st.metric("📋 Total Columnas", len(df.columns))
        with col3:
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                st.metric("🔢 Columnas Numéricas", len(numeric_cols))
        with col4:
            st.metric("📝 Columnas Texto", len(df.select_dtypes(include=['object']).columns))
        
        st.markdown("---")
        
        # Visualizaciones
        st.markdown("### 📉 Visualizaciones Automáticas")
        
        # Seleccionar tipo de gráfico
        viz_type = st.selectbox(
            "Selecciona el tipo de visualización",
            ["Distribución", "Correlación", "Comparación", "Serie Temporal"]
        )
        
        if viz_type == "Distribución":
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            if num_cols:
                col = st.selectbox("Selecciona columna numérica", num_cols)
                fig = Visualizer.auto_plot(df, col, 'numérica')
                st.plotly_chart(fig, use_container_width=True)
                
                # Agregar estadísticas
                st.markdown("### 📊 Estadísticas Descriptivas")
                col_stats = df[col].describe()
                
                cols = st.columns(6)
                metrics = ['mean', 'std', 'min', '25%', '50%', 'max']
                labels = ['Media', 'Desv. Est.', 'Mínimo', 'Q1', 'Mediana', 'Máximo']
                
                for c, metric, label in zip(cols, metrics, labels):
                    c.metric(label, f"{col_stats[metric]:.2f}")
        
        elif viz_type == "Correlación":
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            if len(num_cols) > 1:
                fig = Visualizer.correlation_heatmap(df[num_cols])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Se necesitan al menos 2 columnas numéricas")
        
        elif viz_type == "Comparación":
            cat_cols = df.select_dtypes(include=['object']).columns.tolist()
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if cat_cols and num_cols:
                col1, col2 = st.columns(2)
                with col1:
                    cat_col = st.selectbox("Columna categórica", cat_cols)
                with col2:
                    num_col = st.selectbox("Columna numérica", num_cols)
                
                fig = Visualizer.comparison_plot(df, cat_col, num_col)
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Serie Temporal":
            date_cols = [col for col, type_ in st.session_state.col_types.items() if type_ == 'fecha']
            
            if date_cols:
                date_col = st.selectbox("Columna de fecha", date_cols)
                num_cols = df.select_dtypes(include=['number']).columns.tolist()
                
                if num_cols:
                    value_col = st.selectbox("Columna de valores", num_cols)
                    fig = Visualizer.time_series_plot(df, date_col, value_col)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No se detectaron columnas de fecha")

elif menu == "🤖 Machine Learning":
    st.title("🤖 Machine Learning Automático")
    st.markdown("---")
    
    if st.session_state.df is None:
        st.warning("⚠️ Primero carga un archivo en la sección 'Cargar Datos'")
    else:
        df = st.session_state.df
        
        st.markdown("### Configuración del Modelo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            target = st.selectbox("🎯 Variable Objetivo", df.columns.tolist())
        
        with col2:
            problem_type = st.radio(
                "Tipo de Problema",
                ["Auto-detectar", "Regresión", "Clasificación"],
                horizontal=True
            )
        
        model_type = st.selectbox(
            "🤖 Modelo",
            ["Random Forest", "Regresión Lineal/Logística"]
        )
        
        if st.button("🚀 Entrenar Modelo", type="primary"):
            with st.spinner("Entrenando modelo... Esto puede tomar un momento"):
                try:
                    # Mapear tipos
                    problem_map = {
                        "Auto-detectar": None,
                        "Regresión": "regression",
                        "Clasificación": "classification"
                    }
                    
                    model_map = {
                        "Random Forest": "random_forest",
                        "Regresión Lineal/Logística": "linear"
                    }
                    
                    engine = MLEngine(df, target, problem_map[problem_type])
                    engine.train(model_name=model_map[model_type])
                    metrics = engine.evaluate()
                    
                    st.success("✅ Modelo entrenado exitosamente!")
                    
                    # Mostrar métricas
                    st.markdown("### 📊 Métricas del Modelo")
                    
                    if engine.problem_type == 'regression':
                        col1, col2, col3 = st.columns(3)
                        col1.metric("R² Score", f"{metrics['R2']:.4f}")
                        col2.metric("MAE", f"{metrics['MAE']:.2f}")
                        col3.metric("RMSE", f"{metrics['RMSE']:.2f}")
                    else:
                        st.metric("Accuracy", f"{metrics['Accuracy']:.2%}")
                    
                    # Gráfico de predicciones vs reales
                    st.markdown("### 📈 Predicciones vs Valores Reales")
                    fig = Visualizer.predictions_plot(engine)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Importancia de características
                    if model_type == "Random Forest":
                        st.markdown("### 🔍 Importancia de Características")
                        importance = engine.get_feature_importance()
                        if importance:
                            fig = Visualizer.feature_importance_plot(importance)
                            st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"❌ Error en el entrenamiento: {str(e)}")
                    st.info("ℹ️ Asegúrate de que los datos estén limpios y la variable objetivo sea adecuada")

elif menu == "📥 Exportar":
    st.title("📥 Exportar Datos y Reportes")
    st.markdown("---")
    
    if st.session_state.df is None:
        st.warning("⚠️ Primero carga un archivo en la sección 'Cargar Datos'")
    else:
        df = st.session_state.df
        
        st.markdown("### 💾 Exportar Datos Procesados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            export_format = st.selectbox(
                "Formato de exportación",
                ["CSV", "Excel", "JSON"]
            )
        
        with col2:
            if st.button("📥 Descargar Datos"):
                format_map = {"CSV": "csv", "Excel": "excel", "JSON": "json"}
                buf, mime = export_data(df, format_map[export_format])
                
                st.download_button(
                    label=f"💾 Descargar {export_format}",
                    data=buf,
                    file_name=f"datos_procesados.{format_map[export_format]}",
                    mime=mime
                )
        
        st.markdown("---")
        st.markdown("### 📄 Generar Reporte PDF")
        
        if st.button("📄 Generar Reporte Completo"):
            with st.spinner("Generando reporte PDF..."):
                try:
                    from core.reporter import PDFReporter
                    
                    # Generar algunas estadísticas para el reporte
                    stats = {
                        "Total Registros": len(df),
                        "Total Columnas": len(df.columns),
                        "Columnas Numéricas": len(df.select_dtypes(include=['number']).columns),
                        "Columnas Categóricas": len(df.select_dtypes(include=['object']).columns),
                        "Valores Nulos": df.isnull().sum().sum()
                    }
                    
                    # Generar gráficos para el reporte
                    graphs_paths = []
                    if len(df.select_dtypes(include=['number']).columns) > 0:
                        num_col = df.select_dtypes(include=['number']).columns[0]
                        fig = Visualizer.auto_plot(df, num_col, 'numérica')
                        fig.write_image("temp_graph.png")
                        graphs_paths.append("temp_graph.png")
                    
                    reporter = PDFReporter("Reporte DataVision AI")
                    pdf_bytes = reporter.add_summary(stats, graphs_paths)
                    
                    st.download_button(
                        label="📥 Descargar Reporte PDF",
                        data=pdf_bytes,
                        file_name="reporte_datavision.pdf",
                        mime="application/pdf"
                    )
                    
                    st.success("✅ Reporte generado exitosamente!")
                    
                except Exception as e:
                    st.error(f"❌ Error al generar el reporte: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>DataVision AI v1.0 | Desarrollado con ❤️ usando Streamlit</p>",
    unsafe_allow_html=True
)