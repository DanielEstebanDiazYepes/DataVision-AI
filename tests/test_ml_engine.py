# tests/test_ml_engine.py
import pytest
import pandas as pd
import numpy as np
from core.ml_engine import MLEngine

def test_regression_training():
    """Test con suficientes datos para evitar NaN en métricas."""
    # Crear 20 muestras para tener train/test splits significativos
    np.random.seed(42)
    df = pd.DataFrame({
        'feat1': range(20),
        'feat2': [x * 2 for x in range(20)],
        'target': [x * 3 for x in range(20)]
    })
    
    engine = MLEngine(df, 'target', problem_type='regression')
    engine.train(model_name='linear')
    metrics = engine.evaluate()
    
    # Verificar que las métricas existen y son razonables
    assert 'R2' in metrics
    assert 'MAE' in metrics
    assert 'RMSE' in metrics
    assert not np.isnan(metrics['R2'])
    assert metrics['R2'] > 0.9  # Debería ser muy bueno con relación perfecta