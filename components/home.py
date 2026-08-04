"""
Página de inicio de DataVision AI.
Muestra la bienvenida y características principales.
"""

import streamlit as st

def render_home():
    """Renderiza la página de inicio."""
    
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <h1>🌟 Bienvenido a DataVision AI</h1>
        <p style="font-size: 1.2rem; color: #b0b0b0;">
            Transforma tus datos en insights poderosos con análisis inteligente automatizado
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📤</div>
            <div class="feature-title">Carga Inteligente</div>
            <div class="feature-description">
                Soporta múltiples formatos (CSV, Excel, JSON) y detecta 
                automáticamente tipos de datos, patrones y anomalías.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Análisis Profundo</div>
            <div class="feature-description">
                Identifica valores nulos, duplicados, outliers y genera 
                estadísticas descriptivas completas automáticamente.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">ML Automático</div>
            <div class="feature-description">
                Entrena modelos de regresión y clasificación con un solo clic.
                Obtén predicciones y métricas de rendimiento al instante.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # CTA
    st.markdown("### 🚀 ¿Listo para comenzar?")
    st.markdown("Dirígete a la sección **📤 Cargar Datos** en el menú lateral para empezar.")
    
    if st.button("✨ Comenzar Ahora", type="primary", use_container_width=True):
        st.session_state.navigation = "📤 Cargar Datos"
        st.rerun()
    
    st.markdown("---")
    
    # Estadísticas de la app
    st.markdown("### 📊 ¿Qué puedes hacer con DataVision AI?")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋", "Limpieza de datos")
    with col2:
        st.metric("📈", "Dashboards interactivos")
    with col3:
        st.metric("🤖", "Machine Learning")
    with col4:
        st.metric("📄", "Reportes PDF")