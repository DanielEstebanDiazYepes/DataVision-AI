import streamlit as st
from config import APP_NAME, APP_VERSION, APP_DESCRIPTION

def render_sidebar():
    with st.sidebar:
        st.title(APP_NAME)
        st.markdown(APP_DESCRIPTION)
        st.markdown("---")
        menu = st.radio(
            "Navegación",
            ["Inicio", "Cargar Datos", "Inspección", "Limpieza", "Dashboard", "ML", "Exportar"],
            key="navigation"
        )
        st.markdown("---")
        st.info(f"Versión: {APP_VERSION}")
        if st.session_state.get('df') is not None:
            st.success("Datos cargados")
            st.metric("Filas", st.session_state.df.shape[0])
            st.metric("Columnas", st.session_state.df.shape[1])
        else:
            st.warning("Sin datos cargados")
        return menu