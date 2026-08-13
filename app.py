import streamlit as st
from config import PAGE_CONFIG
from components.sidebar import render_sidebar
from components.home import render_home
from components.upload import render_upload
from components.inspection import render_inspection
from components.cleaning import render_cleaning
from components.dashboard import render_dashboard
from components.ml_training import render_ml_training
from components.export import render_export
import warnings
warnings.filterwarnings("ignore", message="Could not infer format")

# Configuración de la página (debe ser la PRIMERA llamada a Streamlit)
st.set_page_config(**PAGE_CONFIG)

# Inicializar session state
def init_session_state():
    defaults = {
        'df': None,
        'filename': None,
        'col_types': None,
        'ml_engine': None,
        'ml_metrics': None,
        'ml_trained': False,
        'export_buffer': None,
        'export_mime': None,
        'download_format': None,
        'pdf_bytes': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    pages = {
        "Inicio": render_home,
        "Cargar Datos": render_upload,
        "Inspección": render_inspection,
        "Limpieza": render_cleaning,
        "Dashboard": render_dashboard,
        "ML": render_ml_training,
        "Exportar": render_export
    }

def main():
    init_session_state()
    menu = render_sidebar()

    pages = {
        "Inicio": render_home,
        "Cargar Datos": render_upload,
        "Inspección": render_inspection,
        "Limpieza": render_cleaning,
        "Dashboard": render_dashboard,
        "ML": render_ml_training,
        "Exportar": render_export
    }

    if menu in pages:
        pages[menu]()
    else:
        st.warning(f"Página '{menu}' en desarrollo...")

    # Footer simple
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>DataVision AI v1.0</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()