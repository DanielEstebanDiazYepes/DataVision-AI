"""
Estilos CSS premium para DataVision AI.
Diseño moderno, profesional y responsive.
"""

# Tema oscuro principal con gradientes y efectos modernos
PREMIUM_THEME = """
<style>
    /* ========== VARIABLES CSS ========== */
    :root {
        --bg-primary: #0a0e17;
        --bg-secondary: #111827;
        --bg-card: #1a1f2e;
        --bg-card-hover: #1e2640;
        --accent-primary: #3b82f6;
        --accent-secondary: #60a5fa;
        --accent-gradient: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --border-color: #1e293b;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
        --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
        --shadow-lg: 0 8px 30px rgba(0,0,0,0.5);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* ========== FONDO PRINCIPAL ========== */
    .main {
        background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    }
    
    .stApp {
        background: transparent;
    }
    
    /* ========== TIPOGRAFÍA ========== */
    h1 {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-weight: 700;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h2 {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-weight: 600;
        color: var(--text-primary) !important;
        font-size: 1.8rem !important;
    }
    
    h3 {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-weight: 600;
        color: var(--accent-secondary) !important;
        font-size: 1.4rem !important;
    }
    
    p, span, div, label {
        color: var(--text-secondary);
    }
    
    /* ========== SIDEBAR ========== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1a1f2e 100%);
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] h1 {
        font-size: 1.8rem !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        background: var(--bg-card);
        border-radius: var(--radius-md);
        padding: 8px;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        padding: 10px 15px;
        border-radius: var(--radius-sm);
        transition: var(--transition);
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: var(--bg-card-hover);
    }
    
    /* ========== CARDS Y CONTENEDORES ========== */
    .stExpander {
        background: var(--bg-card);
        border-radius: var(--radius-md);
        border: 1px solid var(--border-color);
        overflow: hidden;
        transition: var(--transition);
    }
    
    .stExpander:hover {
        border-color: var(--accent-primary);
        box-shadow: var(--shadow-md);
    }
    
    /* ========== MÉTRICAS ========== */
    [data-testid="stMetric"] {
        background: var(--bg-card);
        border-radius: var(--radius-md);
        padding: 20px;
        border: 1px solid var(--border-color);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--accent-gradient);
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--accent-primary);
    }
    
    [data-testid="stMetricValue"] {
        color: var(--accent-secondary) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
    }
    
    /* ========== BOTONES ========== */
    .stButton > button {
        background: var(--accent-gradient);
        color: white;
        border: none;
        border-radius: var(--radius-md);
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        transition: var(--transition);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255,255,255,0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
    }
    
    .stButton > button:active::after {
        width: 300px;
        height: 300px;
    }
    
    /* Botón secundario */
    .stButton > button[kind="secondary"] {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
    }
    
    /* ========== INPUTS Y SELECTS ========== */
    .stSelectbox [data-baseweb="select"] {
        background: var(--bg-card);
        border-radius: var(--radius-sm);
        border: 1px solid var(--border-color);
    }
    
    .stTextInput > div > div > input {
        background: var(--bg-card);
        border-radius: var(--radius-sm);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
    }
    
    .stSlider > div > div > div {
        background: var(--accent-primary);
    }
    
    /* ========== FILE UPLOADER ========== */
    .stFileUploader {
        background: var(--bg-card);
        border-radius: var(--radius-lg);
        padding: 30px;
        border: 2px dashed var(--border-color);
        transition: var(--transition);
    }
    
    .stFileUploader:hover {
        border-color: var(--accent-primary);
        background: var(--bg-card-hover);
    }
    
    /* ========== TABS ========== */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-card);
        border-radius: var(--radius-md);
        padding: 5px;
        gap: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary);
        border-radius: var(--radius-sm);
        transition: var(--transition);
        padding: 8px 16px;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--accent-gradient);
        color: white;
    }
    
    /* ========== DATAFRAME ========== */
    .stDataFrame {
        background: var(--bg-card);
        border-radius: var(--radius-md);
        border: 1px solid var(--border-color);
        overflow: hidden;
    }
    
    /* ========== ALERTS ========== */
    .stAlert {
        border-radius: var(--radius-md);
        border: none;
        background: var(--bg-card);
    }
    
    /* ========== ANIMACIONES ========== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .element-container {
        animation: fadeInUp 0.5s ease-out;
    }
    
    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--bg-card-hover);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-primary);
    }
</style>
"""

# Estilos específicos para landing page
LANDING_STYLES = """
<style>
    .hero-section {
        text-align: center;
        padding: 60px 0;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .feature-card {
        background: var(--bg-card);
        border-radius: var(--radius-lg);
        padding: 30px;
        text-align: center;
        border: 1px solid var(--border-color);
        transition: var(--transition);
        height: 100%;
    }
    
    .feature-card:hover {
        border-color: var(--accent-primary);
        transform: translateY(-10px);
        box-shadow: var(--shadow-lg);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        animation: float 3s ease-in-out infinite;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 10px;
    }
    
    .feature-description {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
</style>
"""

def get_all_styles():
    """Retorna todos los estilos combinados para la aplicación."""
    return PREMIUM_THEME + LANDING_STYLES