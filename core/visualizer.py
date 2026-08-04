"""
Visualizador principal de DataVision AI.
Genera gráficos interactivos con Plotly, manejando datos sucios de forma robusta.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots

class Visualizer:
    """Genera visualizaciones interactivas con Plotly."""

    @staticmethod
    def auto_plot(df, col, col_type):
        """Gráfico automático según tipo de columna."""
        if col_type == 'numérica':
            fig = px.histogram(df, x=col, title=f'Distribución de {col}',
                               marginal='box', template='plotly_dark')
        elif col_type == 'categórica':
            counts = df[col].value_counts().head(20).reset_index()
            counts.columns = [col, 'count']
            fig = px.bar(counts, x=col, y='count',
                         title=f'Frecuencia de {col}', template='plotly_dark')
        elif col_type == 'fecha':
            df_temp = df.copy()
            df_temp[col] = pd.to_datetime(df_temp[col])
            time_series = df_temp.set_index(col).resample('D').size().reset_index(name='count')
            fig = px.line(time_series, x=col, y='count',
                          title=f'Serie Temporal de {col}', template='plotly_dark')
        else:
            fig = px.histogram(df, x=col, title=f'Distribución de {col}',
                               template='plotly_dark')
        return fig

    @staticmethod
    def missing_values_plot(missing_df):
        """Gráfico de barras para valores nulos."""
        missing_positive = missing_df[missing_df['Nulos'] > 0]
        if missing_positive.empty:
            fig = go.Figure()
            fig.add_annotation(text="No hay valores nulos", showarrow=False, font=dict(size=20))
            fig.update_layout(template='plotly_dark')
            return fig
        fig = px.bar(missing_positive, x='Columna', y='Nulos',
                     title='Valores Nulos por Columna', template='plotly_dark',
                     color='Nulos', color_continuous_scale='reds')
        return fig

    @staticmethod
    def outlier_plot(df, col, outliers):
        """Box plot con outliers resaltados."""
        fig = go.Figure()
        fig.add_trace(go.Box(y=df[col], name=col, boxpoints='outliers', marker_color='lightblue'))
        fig.update_layout(title=f'Outliers en {col}', template='plotly_dark', showlegend=False)
        return fig

    @staticmethod
    def correlation_heatmap(df):
        """Mapa de calor seguro: solo columnas numéricas."""
        num_df = df.select_dtypes(include=[np.number])
        if num_df.shape[1] < 2:
            fig = go.Figure()
            fig.add_annotation(text="Se necesitan al menos 2 columnas numéricas", showarrow=False)
            fig.update_layout(template='plotly_dark')
            return fig
        corr = num_df.corr(numeric_only=True)
        fig = px.imshow(corr, title='Matriz de Correlación', template='plotly_dark',
                        color_continuous_scale='RdBu_r', aspect='auto')
        return fig

    @staticmethod
    def time_series_plot(df, date_col, value_col, freq='D'):
        """Serie temporal con conversión robusta de tipos."""
        df_temp = df[[date_col, value_col]].copy()
        df_temp[date_col] = pd.to_datetime(df_temp[date_col], errors='coerce')
        df_temp[value_col] = pd.to_numeric(df_temp[value_col], errors='coerce')
        df_temp = df_temp.dropna()
        df_temp = df_temp.set_index(date_col)
        ts = df_temp[value_col].resample(freq).mean().reset_index()
        fig = px.line(ts, x=date_col, y=value_col,
                      title=f'{value_col} a lo largo del tiempo', template='plotly_dark')
        return fig

    @staticmethod
    def predictions_plot(engine):
        """Predicciones vs reales / matriz de confusión."""
        preds = engine.model.predict(engine.X_test)
        if engine.problem_type == 'regression':
            fig = px.scatter(x=engine.y_test, y=preds,
                             title='Predicciones vs Valores Reales',
                             labels={'x': 'Valores Reales', 'y': 'Predicciones'},
                             template='plotly_dark', trendline='ols')
        else:
            from sklearn.metrics import confusion_matrix
            cm = confusion_matrix(engine.y_test, preds)
            fig = px.imshow(cm, title='Matriz de Confusión', template='plotly_dark',
                            color_continuous_scale='Blues', text_auto=True)
        return fig

    @staticmethod
    def feature_importance_plot(importance_dict):
        """Top 10 importancia de características."""
        importance_df = pd.DataFrame(
            list(importance_dict.items()),
            columns=['Feature', 'Importance']
        ).sort_values('Importance', ascending=True).tail(10)
        fig = px.bar(importance_df, x='Importance', y='Feature',
                     title='Top 10 Características más Importantes',
                     template='plotly_dark', orientation='h')
        return fig

    @staticmethod
    def type_distribution_pie(type_counts):
        """Gráfico de dona con distribución de tipos de datos."""
        fig = px.pie(values=type_counts.values, names=type_counts.index,
                     title='Distribución de Tipos de Datos', template='plotly_dark',
                     hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig

    @staticmethod
    def distribution_plot(df, col, plot_type='histogram', bins=30):
        """Histograma, box plot o violin plot."""
        if plot_type == 'histogram':
            fig = px.histogram(df, x=col, nbins=bins, title=f'Histograma de {col}',
                               template='plotly_dark', marginal='rug',
                               color_discrete_sequence=['#3b82f6'])
        elif plot_type == 'box':
            fig = px.box(df, y=col, title=f'Diagrama de Caja de {col}',
                         template='plotly_dark', color_discrete_sequence=['#8b5cf6'])
        elif plot_type == 'violin':
            fig = px.violin(df, y=col, title=f'Diagrama de Violín de {col}',
                            template='plotly_dark', box=True,
                            color_discrete_sequence=['#10b981'])
        else:
            raise ValueError(f"Tipo de gráfico no soportado: {plot_type}")
        return fig

    @staticmethod
    def comparison_plot(df, cat_col, num_col, agg_func='mean'):
        """Gráfico de comparación categórica forzando numérico."""
        df_clean = df[[cat_col, num_col]].copy()
        df_clean[num_col] = pd.to_numeric(df_clean[num_col], errors='coerce')
        df_clean = df_clean.dropna(subset=[num_col])
        grouped = df_clean.groupby(cat_col)[num_col].agg(agg_func).reset_index()
        grouped.columns = [cat_col, f'{agg_func} de {num_col}']
        fig = px.bar(grouped, x=cat_col, y=f'{agg_func} de {num_col}',
                     title=f'{agg_func.capitalize()} de {num_col} por {cat_col}',
                     template='plotly_dark', color=cat_col,
                     color_discrete_sequence=px.colors.qualitative.Bold)
        return fig

    @staticmethod
    def scatter_matrix(df):
        """Matriz de dispersión optimizada: máximo 5 columnas, muestreo si >1000 filas."""
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(num_cols) > 5:
            num_cols = num_cols[:5]
        if len(num_cols) < 2:
            fig = go.Figure()
            fig.add_annotation(text="Se necesitan al menos 2 columnas numéricas", showarrow=False)
            fig.update_layout(template='plotly_dark')
            return fig

        df_subset = df[num_cols]
        if len(df_subset) > 1000:
            df_subset = df_subset.sample(1000, random_state=42)

        n = len(num_cols)
        fig = make_subplots(rows=n, cols=n, shared_xaxes=False, shared_yaxes=False,
                            horizontal_spacing=0.02, vertical_spacing=0.02)

        for i, col1 in enumerate(num_cols):
            for j, col2 in enumerate(num_cols):
                if i == j:
                    fig.add_trace(go.Histogram(x=df_subset[col1], name=col1, showlegend=False,
                                               marker_color='#636efa'), row=i+1, col=j+1)
                else:
                    fig.add_trace(go.Scatter(x=df_subset[col2], y=df_subset[col1],
                                             mode='markers', marker=dict(size=4, opacity=0.6, color='#636efa'),
                                             showlegend=False), row=i+1, col=j+1)

        for i, col in enumerate(num_cols):
            fig.update_xaxes(title_text=col, row=n, col=i+1)
            fig.update_yaxes(title_text=col, row=i+1, col=1)

        fig.update_layout(title='Matriz de Dispersión', template='plotly_dark',
                          height=200*n, showlegend=False)
        return fig

    @staticmethod
    def pie_chart(df, cat_col, top_n=10):
        """Gráfico de pastel con top N categorías."""
        counts = df[cat_col].value_counts().head(top_n)
        if len(df[cat_col].unique()) > top_n:
            others_count = df[cat_col].value_counts().iloc[top_n:].sum()
            counts['Otros'] = others_count
        fig = px.pie(values=counts.values, names=counts.index,
                     title=f'Composición de {cat_col} (Top {top_n})',
                     template='plotly_dark', hole=0.3,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig