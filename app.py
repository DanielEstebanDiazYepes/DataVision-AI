"""
DataVision AI - Plataforma de Análisis Inteligente de Datos.
Aplicación principal que integra todos los componentes modulares.
"""

import streamlit as st
from config import PAGE_CONFIG
from assets.styles import get_all_styles
from components.sidebar import render_sidebar
from components.home import render_home
from components.upload import render_upload
from components.inspection import render_inspection
from components.cleaning import render_cleaning
from components.dashboard import render_dashboard
from components.ml_training import render_ml_training
from components.export import render_export

# Configuración inicial
st.set_page_config(**PAGE_CONFIG)

# Aplicar estilos premium
st.markdown(get_all_styles(), unsafe_allow_html=True)

# Inicializar session state
def init_session_state():
    """Inicializa todas las variables de estado de sesión."""
    defaults = {
        'df': None,
        'filename': None,
        'col_types': None,
        'ml_engine': None,
        'ml_metrics': None,
        'ml_trained': False,
        'export_buffer': None,
        'export_mime': None,
        'export_format': None,
        'pdf_bytes': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def main():
    """Función principal de la aplicación."""
    
    init_session_state()
    
    # Renderizar sidebar y obtener navegación
    menu = render_sidebar()
    
    # Router de páginas
    pages = {
        "🏠 Inicio": render_home,
        "📤 Cargar Datos": render_upload,
        "🔍 Inspección": render_inspection,
        "🧹 Limpieza": render_cleaning,
        "📊 Dashboard": render_dashboard,
        "🤖 Machine Learning": render_ml_training,
        "📥 Exportar": render_export
    }
    
    # Renderizar página seleccionada
    if menu in pages:
        pages[menu]()
    else:
        st.warning(f"🚧 Página '{menu}' en desarrollo...")
    
    # Footer minimalista
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; padding: 20px 0;'>
            <p style='color: var(--text-secondary); font-size: 0.85rem; margin: 0;'>
                DataVision AI v1.0 · Construido con Streamlit & Python · © 2024
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()