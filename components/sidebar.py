"""
Componente de barra lateral para DataVision AI.
Navegación principal de la aplicación.
"""

import streamlit as st
from config import APP_NAME, APP_ICON, APP_DESCRIPTION, APP_VERSION, NAVIGATION_MENU

def render_sidebar():
    """Renderiza la barra lateral con navegación."""
    
    with st.sidebar:
        # Logo y título
        st.markdown(f"# {APP_ICON}")
        st.title(APP_NAME)
        st.markdown(f"*{APP_DESCRIPTION}*")
        st.markdown("---")
        
        # Navegación
        menu = st.radio(
            "📋 Navegación",
            list(NAVIGATION_MENU.keys()),
            key="navigation"
        )
        
        st.markdown("---")
        
        # Información adicional
        st.markdown("### ℹ️ Información")
        st.info(f"""
        **Versión:** {APP_VERSION}
        
        **Formatos soportados:**
        - CSV
        - Excel
        - JSON
        """)
        
        st.markdown("---")
        
        # Estado actual
        if st.session_state.get('df') is not None:
            st.success("✅ Datos cargados")
            st.metric("Filas", st.session_state.df.shape[0])
            st.metric("Columnas", st.session_state.df.shape[1])
        else:
            st.warning("⚠️ Sin datos cargados")
        
        return menu