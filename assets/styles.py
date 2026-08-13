PREMIUM_THEME = """
<style>
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f4f6f8;
        --bg-card: #ffffff;
        --accent-primary: #1f4e79;
        --accent-secondary: #2a6da3;
        --text-primary: #262730;
        --text-secondary: #4b5563;
        --border-color: #e5e7eb;
        --radius-sm: 6px;
        --radius-md: 8px;
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
        --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
        --transition: all 0.2s ease;
    }

    .main { background-color: var(--bg-primary); }
    .stApp { background: var(--bg-primary); }

    h1, h2, h3, h4, h5, h6 { color: var(--text-primary) !important; }
    p, span, div, label { color: var(--text-secondary); }

    [data-testid="stSidebar"] {
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }

    [data-testid="stMetric"] {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 16px;
        box-shadow: var(--shadow-sm);
    }

    [data-testid="stMetricValue"] { color: var(--accent-primary) !important; }

    .stButton > button {
        background-color: var(--accent-primary);
        color: white;
        border: none;
        border-radius: var(--radius-md);
        padding: 10px 20px;
        font-weight: 500;
        transition: var(--transition);
    }
    .stButton > button:hover {
        background-color: var(--accent-secondary);
        box-shadow: var(--shadow-md);
    }

    .stFileUploader {
        background: var(--bg-secondary);
        border: 1px dashed var(--border-color);
        border-radius: var(--radius-md);
    }

    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary);
        border-radius: var(--radius-md);
    }
    .stTabs [aria-selected="true"] {
        background: var(--accent-primary);
        color: white;
    }

    .stAlert { border-radius: var(--radius-md); }
</style>
"""

def get_all_styles():
    return PREMIUM_THEME