# 📊 DataVision AI

**Plataforma inteligente de análisis de datos** construida con Python y Streamlit.  
Permite a cualquier usuario cargar archivos CSV, Excel o JSON para explorar, limpiar, visualizar y modelar datos sin necesidad de programar.

---

## ✨ Características principales

- **Carga automática** de archivos CSV, Excel y JSON.
- **Detección inteligente de tipos** de columnas (numéricas, categóricas, fechas, booleanas, texto).
- **Inspección de calidad**:
  - Valores nulos con gráficos de barras.
  - Filas duplicadas.
  - Detección de outliers usando el método IQR.
- **Limpieza interactiva**:
  - Eliminar duplicados.
  - Imputar valores nulos (media, mediana, moda o eliminar filas).
  - Convertir tipos de datos.
- **Dashboard interactivo**:
  - KPIs automáticos.
  - Histogramas, box plots, violin plots.
  - Matriz de correlación y matriz de dispersión.
  - Comparaciones categóricas.
  - Series temporales.
  - Gráficos de composición.
- **Machine Learning automático**:
  - Regresión y clasificación.
  - Modelos: Random Forest, Regresión Lineal/Logística.
  - Métricas: R², MAE, RMSE, Accuracy, reporte de clasificación.
  - Importancia de características.
- **Exportación**:
  - Datos procesados en CSV, Excel o JSON.
  - Reporte PDF con resumen ejecutivo, gráficos y conclusiones.
- **Registro de actividad (logs)** en consola y en `logs/datavision.log`.

---

## 🛠️ Tecnologías utilizadas

- **Python 3.10+**
- **Streamlit** para la interfaz web.
- **Pandas** y **NumPy** para manipulación de datos.
- **Plotly** para visualizaciones interactivas.
- **Scikit-learn** para Machine Learning.
- **FPDF2** para generación de reportes PDF.
- **PyArrow** para serialización eficiente.

---

## 🚀 Cómo ejecutar localmente

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/DanielEstebanDiazYepes/DataVision-AI
   cd DataVision-AI


2. **Crea un entorno virtual (recomendado)**:
   ```bash
   python -m venv venv
   source venv/bin/activate      # En Windows: venv\Scripts\activate


3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt


4. **IEjecuta la aplicación**:
   ```bash
   streamlit run app.py


0. **O si usas Python**:
   ```bash
   python -m streamlit run app.py


5. **Abre tu navegador en**:
   ```bash
   http://localhost:8501




