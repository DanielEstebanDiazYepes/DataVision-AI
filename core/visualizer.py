

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import logging
from utils.logging_config import setup_logging

logger = setup_logging()

class Visualizer:

    @staticmethod
    def auto_plot(df, col, col_type):
       
        logger.info(f"Creando auto_plot para columna '{col}' tipo '{col_type}'")
        if col_type == 'numérica':
            fig = px.histogram(df, x=col, title=f'Distribución de {col}',
                               marginal='box', template='plotly_white')
        elif col_type == 'categórica':
            counts = df[col].value_counts().head(20).reset_index()
            counts.columns = [col, 'count']
            fig = px.bar(counts, x=col, y='count',
                         title=f'Frecuencia de {col}', template='plotly_white')
        elif col_type == 'fecha':
            df_temp = df.copy()
            df_temp[col] = pd.to_datetime(df_temp[col])
            time_series = df_temp.set_index(col).resample('D').size().reset_index(name='count')
            fig = px.line(time_series, x=col, y='count',
                          title=f'Serie Temporal de {col}', template='plotly_white')
        else:
            fig = px.histogram(df, x=col, title=f'Distribución de {col}',
                               template='plotly_white')
        return fig

    @staticmethod
    def missing_values_plot(missing_df):
       
        logger.info("Creando gráfico de valores nulos")
        missing_positive = missing_df[missing_df['Nulos'] > 0]
        if missing_positive.empty:
            fig = go.Figure()
            fig.add_annotation(text="No hay valores nulos", showarrow=False, font=dict(size=20))
            fig.update_layout(template='plotly_white')
            return fig
        fig = px.bar(missing_positive, x='Columna', y='Nulos',
                     title='Valores Nulos por Columna', template='plotly_white',
                     color='Nulos', color_continuous_scale='reds')
        return fig

    @staticmethod
    def outlier_plot(df, col, outliers):
        
        logger.info(f"Creando box plot para outliers en '{col}'")
        fig = go.Figure()
        fig.add_trace(go.Box(y=df[col], name=col, boxpoints='outliers', marker_color='lightblue'))
        fig.update_layout(title=f'Outliers en {col}', template='plotly_white', showlegend=False)
        return fig

    @staticmethod
    def correlation_heatmap(df):
        logger.info("Creando mapa de calor de correlación")
        num_df = df.select_dtypes(include=[np.number])
        if num_df.shape[1] < 2:
            fig = go.Figure()
            fig.add_annotation(text="Se necesitan al menos 2 columnas numéricas", showarrow=False)
            fig.update_layout(template='plotly_white')
            return fig
        
        # Eliminar filas con NaN para evitar matriz vacía
        num_df_clean = num_df.dropna()
        if len(num_df_clean) < 2:
            logger.warning("Pocos datos numéricos completos")
            fig = go.Figure()
            fig.add_annotation(text="Datos insuficientes después de eliminar nulos", showarrow=False)
            fig.update_layout(template='plotly_white')
            return fig
        
        corr = num_df_clean.corr(numeric_only=True)
        logger.info(f"Matriz de correlación calculada: {corr.shape}")
        
        fig = px.imshow(
            corr,
            title='Matriz de Correlación',
            template='plotly_white',
            color_continuous_scale='RdBu_r',
            aspect='auto',
            text_auto=True,        
            zmin=-1, zmax=1       
        )
        return fig

    @staticmethod
    def time_series_plot(df, date_col, value_col, freq='D'):
     
        logger.info(f"Creando serie temporal: {date_col} vs {value_col} (freq={freq})")
        df_temp = df[[date_col, value_col]].copy()
        df_temp[date_col] = pd.to_datetime(df_temp[date_col], errors='coerce')
        df_temp[value_col] = pd.to_numeric(df_temp[value_col], errors='coerce')
        df_temp = df_temp.dropna()
        df_temp = df_temp.set_index(date_col)
        ts = df_temp[value_col].resample(freq).mean().reset_index()
        fig = px.line(ts, x=date_col, y=value_col,
                      title=f'{value_col} a lo largo del tiempo', template='plotly_white')
        return fig

    @staticmethod
    def predictions_plot(engine):
       
        logger.info("Creando gráfico de predicciones")
        preds = engine.model.predict(engine.X_test)
        
        if engine.problem_type == 'regression':
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=engine.y_test,
                y=preds,
                mode='markers',
                marker=dict(color='#1f4e79', size=8, opacity=0.6),
                name='Predicciones'
            ))
            min_val = min(engine.y_test.min(), preds.min())
            max_val = max(engine.y_test.max(), preds.max())
            fig.add_trace(go.Scatter(
                x=[min_val, max_val],
                y=[min_val, max_val],
                mode='lines',
                line=dict(color='red', dash='dash'),
                name='Perfecta (y=x)'
            ))
            fig.update_layout(
                title='Predicciones vs Valores Reales',
                xaxis_title='Valores Reales',
                yaxis_title='Predicciones',
                template='plotly_white'
            )
        else:
            from sklearn.metrics import confusion_matrix
            cm = confusion_matrix(engine.y_test, preds)
            labels = sorted(set(engine.y_test) | set(preds))
            fig = go.Figure(data=go.Heatmap(
                z=cm,
                x=labels,
                y=labels,
                colorscale='Blues',
                text=cm,
                texttemplate="%{text}",
                textfont={"size":14},
                showscale=False
            ))
            fig.update_layout(
                title='Matriz de Confusión',
                xaxis_title='Predicción',
                yaxis_title='Valor Real',
                template='plotly_white'
            )
        return fig

    @staticmethod
    def feature_importance_plot(importance_dict):
       
        logger.info("Creando gráfico de importancia de características")
        importance_df = pd.DataFrame(
            list(importance_dict.items()),
            columns=['Feature', 'Importance']
        ).sort_values('Importance', ascending=True).tail(10)
        fig = px.bar(importance_df, x='Importance', y='Feature',
                     title='Top 10 Características más Importantes',
                     template='plotly_white', orientation='h')
        return fig

    @staticmethod
    def type_distribution_pie(type_counts):
        
        logger.info("Creando gráfico de pastel de tipos")
        fig = px.pie(values=type_counts.values, names=type_counts.index,
                     title='Distribución de Tipos de Datos', template='plotly_white',
                     hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig

    @staticmethod
    def distribution_plot(df, col, plot_type='histogram', bins=30):
       
        logger.info(f"Creando {plot_type} para '{col}'")
        if plot_type == 'histogram':
            fig = px.histogram(df, x=col, nbins=bins, title=f'Histograma de {col}',
                               template='plotly_white', marginal='rug',
                               color_discrete_sequence=['#1f4e79'])
        elif plot_type == 'box':
            fig = px.box(df, y=col, title=f'Diagrama de Caja de {col}',
                         template='plotly_white', color_discrete_sequence=['#1f4e79'])
        elif plot_type == 'box':
            fig = px.box(df, y=col, title=f'Diagrama de Caja de {col}',
                 template='plotly_white',
                 color_discrete_sequence=['#1f4e79'])
        elif plot_type == 'violin':
            fig = px.violin(df, y=col, title=f'Diagrama de Violín de {col}',
                            template='plotly_white', box=True,
                            color_discrete_sequence=['#1f4e79'])
        else:
            raise ValueError(f"Tipo de gráfico no soportado: {plot_type}")
        return fig

    @staticmethod
    def comparison_plot(df, cat_col, num_col, agg_func='mean'):
        logger.info(f"Creando comparación: {num_col} agrupado por {cat_col} ({agg_func})")
        df_clean = df[[cat_col, num_col]].copy()
        df_clean[num_col] = pd.to_numeric(df_clean[num_col], errors='coerce')
        df_clean = df_clean.dropna(subset=[num_col])
        
        if df_clean.empty:
            logger.warning("No hay datos numéricos válidos para comparar")
            fig = go.Figure()
            fig.add_annotation(text="No hay datos numéricos válidos para comparar", showarrow=False)
            fig.update_layout(template='plotly_white')
            return fig
        
        grouped = df_clean.groupby(cat_col)[num_col].agg(agg_func).reset_index()
        grouped.columns = [cat_col, f'{agg_func} de {num_col}']
        
        logger.info(f"Datos agrupados: {len(grouped)} categorías")
        
        fig = px.bar(
            grouped,
            x=cat_col,
            y=f'{agg_func} de {num_col}',
            title=f'{agg_func.capitalize()} de {num_col} por {cat_col}',
            template='plotly_white',
            color=cat_col,
            color_discrete_sequence=px.colors.qualitative.Dark24
        )
        return fig

    @staticmethod
    def scatter_matrix(df):
        
        logger.info("Creando matriz de dispersión")
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(num_cols) > 5:
            num_cols = num_cols[:5]
        if len(num_cols) < 2:
            fig = go.Figure()
            fig.add_annotation(text="Se necesitan al menos 2 columnas numéricas", showarrow=False)
            fig.update_layout(template='plotly_white')
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
                                               marker_color='#1f4e79'), row=i+1, col=j+1)
                else:
                    fig.add_trace(go.Scatter(x=df_subset[col2], y=df_subset[col1],
                                             mode='markers', marker=dict(size=4, opacity=0.6, color='#1f4e79'),
                                             showlegend=False), row=i+1, col=j+1)

     
        for r in range(1, n+1):
            for c in range(1, n+1):
                fig.update_xaxes(matches=None, row=r, col=c)
                fig.update_yaxes(matches=None, row=r, col=c)

        for i, col in enumerate(num_cols):
            fig.update_xaxes(title_text=col, row=n, col=i+1)
            fig.update_yaxes(title_text=col, row=i+1, col=1)

        fig.update_layout(title='Matriz de Dispersión', template='plotly_white',
                          height=200*n, showlegend=False)
        return fig

    @staticmethod
    def pie_chart(df, cat_col, top_n=10):
        
        logger.info(f"Creando gráfico de pastel para {cat_col}")
        counts = df[cat_col].value_counts().head(top_n)
        if len(df[cat_col].unique()) > top_n:
            others_count = df[cat_col].value_counts().iloc[top_n:].sum()
            counts['Otros'] = others_count
        fig = px.pie(values=counts.values, names=counts.index,
                     title=f'Composición de {cat_col} (Top {top_n})',
                     template='plotly_white', hole=0.3,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig
