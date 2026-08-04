import pandas as pd
import numpy as np

np.random.seed(42)
n = 200

# Datos base
df = pd.DataFrame({
    'id': range(1, n+1),
    'nombre': np.random.choice(['Ana', 'Luis', 'María', 'Carlos', 'Elena', None], n, p=[0.2, 0.2, 0.2, 0.15, 0.15, 0.1]),
    'edad': np.random.normal(40, 12, n).astype(int),
    'salario': np.random.normal(50000, 15000, n),
    'fecha_ingreso': pd.date_range('2020-01-01', periods=n, freq='D'),
    'ciudad': np.random.choice(['Madrid', 'Barcelona', 'Valencia', None], n, p=[0.3, 0.3, 0.3, 0.1]),
    'activo': np.random.choice([True, False], n),
    'compras': np.random.poisson(5, n),        # Variable numérica para regresión
    'segmento': np.random.choice(['Premium', 'Estándar', 'Básico'], n)  # Para clasificación
})

# Insertar valores nulos adicionales en columnas clave
df.loc[10:15, 'edad'] = np.nan
df.loc[20:25, 'salario'] = np.nan
df.loc[30:35, 'fecha_ingreso'] = pd.NaT
df.loc[40:45, 'ciudad'] = None
df.loc[50:55, 'compras'] = np.nan

# Insertar outliers
df.loc[0, 'salario'] = 500000   # extremo
df.loc[1, 'edad'] = 120         # extremo
df.loc[2, 'compras'] = 50       # extremo

# Duplicar algunas filas
duplicados = df.iloc[60:65].copy()
df = pd.concat([df, duplicados], ignore_index=True)

# Añadir una columna con muchos valores nulos (>50%) para probar detección
df['notas'] = np.where(np.random.rand(len(df)) > 0.7, 'Alta', None)

# Añadir una columna de fecha extra con nulos
df['ultima_compra'] = pd.NaT
df.loc[:100, 'ultima_compra'] = pd.date_range('2023-01-01', periods=101, freq='W')

# Guardar
df.to_csv('dataset_prueba_completa.csv', index=False)
print("Dataset creado: dataset_prueba_completa.csv")
print(f"Dimensiones: {df.shape}")
print(f"Nulos totales: {df.isnull().sum().sum()}")
print(f"Duplicados: {df.duplicated().sum()}")