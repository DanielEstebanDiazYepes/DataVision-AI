"""
Configuraciones globales de DataVision AI.
Centraliza constantes, temas y configuraciones para fácil mantenimiento.
"""

# Información de la app
APP_NAME = "DataVision AI"
APP_VERSION = "1.0.0"
APP_ICON = "📊"
APP_DESCRIPTION = "Plataforma inteligente de análisis de datos"

# Configuración de página
PAGE_CONFIG = {
    "page_title": APP_NAME,
    "page_icon": APP_ICON,
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Formatos de archivo soportados
SUPPORTED_FORMATS = ["csv", "xlsx", "json"]

# Tipos de datos
DATA_TYPES = {
    "numérica": "numeric",
    "categórica": "category",
    "fecha": "datetime",
    "booleana": "bool",
    "texto": "string"
}

# Estrategias de imputación
IMPUTATION_STRATEGIES = {
    "Media": "mean",
    "Mediana": "median",
    "Moda": "mode",
    "Eliminar filas": "drop"
}

# Modelos ML disponibles
ML_MODELS = {
    "Random Forest": "random_forest",
    "Regresión Lineal/Logística": "linear"
}

# Tipos de problemas ML
ML_PROBLEM_TYPES = {
    "Auto-detectar": None,
    "Regresión": "regression",
    "Clasificación": "classification"
}

# Formatos de exportación
EXPORT_FORMATS = {
    "CSV": "csv",
    "Excel": "excel",
    "JSON": "json"
}

# Navegación
NAVIGATION_MENU = {
    "🏠 Inicio": "home",
    "📤 Cargar Datos": "upload",
    "🔍 Inspección": "inspection",
    "🧹 Limpieza": "cleaning",
    "📊 Dashboard": "dashboard",
    "🤖 Machine Learning": "ml",
    "📥 Exportar": "export"
}