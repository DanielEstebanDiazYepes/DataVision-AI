"""
Componente de exportación.
Permite descargar datos procesados y generar reportes PDF.
"""

import streamlit as st
import pandas as pd
from core.exporter import export_data
from core.reporter import PDFReporter
from core.visualizer import Visualizer
from config import EXPORT_FORMATS
import os
import tempfile

def render_export():
    """Renderiza la página de exportación."""
    st.title("📥 Exportar Datos y Reportes")
    st.markdown("---")

    if st.session_state.df is None:
        st.warning("⚠️ Primero carga un archivo en la sección 'Cargar Datos'")
        return

    df = st.session_state.df

    # Sección 1: Exportar datos procesados
    st.markdown("### 💾 Exportar Datos Procesados")

    col1, col2 = st.columns(2)

    with col1:
        export_format = st.selectbox(
            "Formato de exportación",
            list(EXPORT_FORMATS.keys()),
            key="export_format_widget"   # Clave diferente para el widget
        )

    with col2:
        if st.button("📥 Preparar descarga", type="primary"):
            format_key = EXPORT_FORMATS[export_format]
            buf, mime = export_data(df, format_key)

            # Guardar en session state con nombres que no colisionen
            st.session_state.export_buffer = buf
            st.session_state.export_mime = mime
            st.session_state.download_format = export_format.lower()   # nombre diferente
            st.success(f"✅ Archivo preparado en formato {export_format}")

    if st.session_state.get('export_buffer'):
        st.download_button(
            label=f"💾 Descargar datos_procesados.{st.session_state.download_format}",
            data=st.session_state.export_buffer,
            file_name=f"datos_procesados.{st.session_state.download_format}",
            mime=st.session_state.export_mime,
            key="download_data"
        )

    # Opciones de exportación
    with st.expander("⚙️ Opciones de exportación"):
        if export_format == "CSV":
            encoding = st.selectbox("Encoding", ["utf-8", "latin1", "cp1252"], key="csv_encoding")
            separator = st.selectbox("Separador", [",", ";", "\\t", "|"], key="csv_sep")
        elif export_format == "Excel":
            sheet_name = st.text_input("Nombre de la hoja", "Datos", key="excel_sheet")
            include_index = st.checkbox("Incluir índice", False, key="excel_index")

    st.markdown("---")

    # Sección 2: Generar reporte PDF
    st.markdown("### 📄 Generar Reporte PDF Profesional")
    st.markdown("""
    El reporte incluirá:
    - 📊 Resumen ejecutivo
    - 📈 Estadísticas descriptivas
    - 📉 Gráficos principales
    - 🔍 Análisis de calidad de datos
    - 💡 Recomendaciones automáticas
    """)

    include_sections = st.multiselect(
        "Secciones a incluir en el reporte",
        ["Resumen ejecutivo", "Estadísticas", "Gráficos", "Calidad de datos", "Recomendaciones"],
        default=["Resumen ejecutivo", "Estadísticas", "Gráficos", "Calidad de datos"],
        key="pdf_sections"
    )

    if st.button("📄 Generar Reporte PDF", type="primary", use_container_width=True):
        with st.spinner("🔄 Generando reporte PDF..."):
            try:
                # Preparar estadísticas
                stats = {
                    "Total Registros": len(df),
                    "Total Columnas": len(df.columns),
                    "Columnas Numéricas": len(df.select_dtypes(include=['number']).columns),
                    "Columnas Categóricas": len(df.select_dtypes(include=['object']).columns),
                    "Valores Nulos Totales": int(df.isnull().sum().sum()),
                    "Filas Duplicadas": int(df.duplicated().sum())
                }

                # Generar gráficos temporales
                graphs_paths = []
                temp_dir = tempfile.mkdtemp()

                # Gráfico de distribución de la primera columna numérica
                num_cols = df.select_dtypes(include=['number']).columns.tolist()
                if num_cols:
                    fig = Visualizer.auto_plot(df, num_cols[0], 'numérica')
                    path = os.path.join(temp_dir, "distribucion.png")
                    fig.write_image(path)
                    graphs_paths.append(path)

                # Gráfico de valores nulos (si hay)
                from core.inspector import DataInspector
                missing = DataInspector.missing_values(df)
                if missing['Nulos'].sum() > 0:
                    fig = Visualizer.missing_values_plot(missing)
                    path = os.path.join(temp_dir, "nulos.png")
                    fig.write_image(path)
                    graphs_paths.append(path)

                # Generar PDF
                reporter = PDFReporter("Reporte DataVision AI")
                pdf_bytes = reporter.add_summary(stats, graphs_paths)

                # Limpiar archivos temporales
                for path in graphs_paths:
                    os.remove(path)
                os.rmdir(temp_dir)

                st.session_state.pdf_bytes = pdf_bytes
                st.success("✅ Reporte generado exitosamente!")
                st.balloons()

            except Exception as e:
                st.error(f"❌ Error al generar el reporte: {str(e)}")
                st.info("💡 Asegúrate de tener instalado kaleido para generar imágenes: pip install kaleido")

    if st.session_state.get('pdf_bytes'):
        st.download_button(
            label="📥 Descargar Reporte PDF",
            data=st.session_state.pdf_bytes,
            file_name="reporte_datavision.pdf",
            mime="application/pdf",
            key="download_pdf"
        )

    st.markdown("---")

    # Sección 3: Información del dataset
    st.markdown("### 📋 Resumen del Dataset a Exportar")

    col1, col2, col3 = st.columns(3)
    col1.metric("Filas", len(df))
    col2.metric("Columnas", len(df.columns))
    memory = df.memory_usage(deep=True).sum() / 1024**2
    col3.metric("Tamaño en memoria", f"{memory:.2f} MB")
    st.dataframe(df.head(), use_container_width=True)