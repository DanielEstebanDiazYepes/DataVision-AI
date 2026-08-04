"""
Componente de carga de datos.
Maneja la subida de archivos y preview inicial.
"""

import streamlit as st
from core.data_loader import DataLoader

def render_upload():
    """Renderiza la página de carga de datos."""
    
    st.title("📤 Cargar Archivo de Datos")
    st.markdown("---")
    
    # Instrucciones
    with st.expander("ℹ️ Instrucciones de carga", expanded=False):
        st.markdown("""
        - **Formatos soportados:** CSV, Excel (.xlsx, .xls), JSON
        - **Tamaño máximo recomendado:** 200 MB
        - **Encoding:** Se detecta automáticamente (UTF-8, Latin-1)
        - **Primera fila como encabezado:** Sí, por defecto
        """)
    
    uploaded_file = st.file_uploader(
        "Arrastra y suelta tu archivo aquí o haz clic para seleccionarlo",
        type=["csv", "xlsx", "json"],
        help="Formatos soportados: CSV, Excel, JSON"
    )
    
    if uploaded_file is not None:
        with st.spinner("🔄 Cargando y analizando archivo..."):
            try:
                # Cargar datos
                df, filename = DataLoader.load_file(uploaded_file)
                
                # Guardar en session state
                st.session_state.df = df
                st.session_state.filename = filename
                st.session_state.col_types = DataLoader.detect_column_types(df)
                
                # Feedback positivo
                st.success(f"✅ Archivo cargado exitosamente: **{filename}**")
                
                # Métricas rápidas
                st.markdown("### 📊 Resumen del Dataset")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total de Filas", f"{df.shape[0]:,}")
                
                with col2:
                    st.metric("Total de Columnas", df.shape[1])
                
                with col3:
                    num_cols = sum(1 for v in st.session_state.col_types.values() if v == 'numérica')
                    st.metric("Columnas Numéricas", num_cols)
                
                with col4:
                    cat_cols = sum(1 for v in st.session_state.col_types.values() if v in ['categórica', 'texto'])
                    st.metric("Columnas Texto", cat_cols)
                
                # Preview de datos
                st.markdown("### 👁️ Vista Previa (Primeras 10 filas)")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Información de columnas
                with st.expander("🔍 Ver tipos de datos detectados", expanded=False):
                    types_df = DataLoader.get_column_types_dataframe(st.session_state.col_types)
                    st.dataframe(types_df, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error al cargar el archivo: {str(e)}")
                st.info("💡 Verifica que el archivo no esté corrupto y tenga un formato válido.")
    
    else:
        # Estado vacío
        st.info("👆 Esperando a que cargues un archivo de datos...")
        
        # Ejemplo de datos de prueba
        with st.expander("🧪 ¿No tienes datos? Usa datos de ejemplo", expanded=False):
            st.markdown("Puedes descargar estos datasets de ejemplo:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 Dataset Iris (Clasificación)"):
                    import seaborn as sns
                    df = sns.load_dataset('iris')
                    st.session_state.df = df
                    st.session_state.filename = "iris.csv"
                    st.session_state.col_types = DataLoader.detect_column_types(df)
                    st.rerun()
            
            with col2:
                if st.button("💰 Dataset Tips (Regresión)"):
                    import seaborn as sns
                    df = sns.load_dataset('tips')
                    st.session_state.df = df
                    st.session_state.filename = "tips.csv"
                    st.session_state.col_types = DataLoader.detect_column_types(df)
                    st.rerun()