from celery import Celery
import pandas as pd
from core.ml_engine import MLEngine
import pickle
import io

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.task(bind=True)
def train_model_task(self, df_dict, target):
    """Entrena modelo en segundo plano. df_dict es el DataFrame en formato dict."""
    df = pd.DataFrame(df_dict)
    engine = MLEngine(df, target)
    engine.train()
    metrics = engine.evaluate()
    # Serializar modelo entrenado (se puede guardar en Redis/DB)
    buf = io.BytesIO()
    pickle.dump(engine, buf)
    buf.seek(0)
    # Guardar en Redis o devolver ID
    # Aquí simplificamos devolviendo métricas
    return {'metrics': metrics, 'model': 'Serializado (pendiente guardar en DB)'}