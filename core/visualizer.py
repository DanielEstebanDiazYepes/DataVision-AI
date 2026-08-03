import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class Visualizer:
    """Genera visualizaciones interactivas con Plotly."""
    
    @staticmethod
    def auto_plot(df, col, col_type):
        """Genera gráfico automático según tipo de columna."""
        if col_type == 'numérica':
            fig = px.histogram(
                df, x=col,
                title=f'Distribución de {col}',
                marginal='box',
                template='plotly_dark'
            )
        elif col_type == 'categórica':
            counts = df[col].value_counts().head(20).reset_index()
            counts.columns = [col, 'count']
            fig = px.bar(
                counts, x=col, y='count',
                title=f'Frecuencia de {col}',
                template='plotly_dark'
            )
        elif col_type == 'fecha':
            df_temp = df.copy()
            df_temp[col] = pd.to_datetime(df_temp[col])
            time_series = df_temp.set_index(col).resample('D').size().reset_index(name='count')
            fig = px.line(
                time_series, x=col, y='count',
                title=f'Serie Temporal de {col}',
                template='plotly_dark'
            )
        else:
            fig = px.histogram(
                df, x=col,
                title=f'Distribución de {col}',
                template='plotly_dark'
            )
        return fig
    
    @staticmethod
    def missing_values_plot(missing_df):
        """Gráfico de barras para valores nulos."""
        missing_positive = missing_df[missing_df['Nulos'] > 0]
        fig = px.bar(
            missing_positive,
            x='Columna', y='Nulos',
            title='Valores Nulos por Columna',
            template='plotly_dark',
            color='Nulos',
            color_continuous_scale='reds'
        )
        return fig
    
    @staticmethod
    def outlier_plot(df, col, outliers):
        """Box plot con outliers resaltados."""
        fig = go.Figure()
        
        fig.add_trace(go.Box(
            y=df[col],
            name=col,
            boxpoints='outliers',
            marker_color='lightblue'
        ))
        
        fig.update_layout(
            title=f'Outliers en {col}',
            template='plotly_dark',
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def correlation_heatmap(df):
        """Mapa de calor de correlaciones."""
        corr = df.corr()
        fig = px.imshow(
            corr,
            title='Matriz de Correlación',
            template='plotly_dark',
            color_continuous_scale='RdBu_r',
            aspect='auto'
        )
        return fig
    
    @staticmethod
    def comparison_plot(df, cat_col, num_col):
        """Gráfico de comparación (box plot por categoría)."""
        fig = px.box(
            df, x=cat_col, y=num_col,
            title=f'{num_col} por {cat_col}',
            template='plotly_dark',
            color=cat_col
        )
        return fig
    
    @staticmethod
    def time_series_plot(df, date_col, value_col):
        """Gráfico de serie temporal."""
        df_temp = df.copy()
        df_temp[date_col] = pd.to_datetime(df_temp[date_col])
        df_temp = df_temp.sort_values(date_col)
        
        fig = px.line(
            df_temp, x=date_col, y=value_col,
            title=f'{value_col} a lo largo del tiempo',
            template='plotly_dark'
        )
        return fig
    
    @staticmethod
    def predictions_plot(engine):
        """Gráfico de predicciones vs valores reales."""
        preds = engine.model.predict(engine.X_test)
        
        if engine.problem_type == 'regression':
            fig = px.scatter(
                x=engine.y_test, y=preds,
                title='Predicciones vs Valores Reales',
                labels={'x': 'Valores Reales', 'y': 'Predicciones'},
                template='plotly_dark',
                trendline='ols'
            )
        else:
            # Para clasificación, mostrar matriz de confusión como heatmap
            from sklearn.metrics import confusion_matrix
            cm = confusion_matrix(engine.y_test, preds)
            fig = px.imshow(
                cm,
                title='Matriz de Confusión',
                template='plotly_dark',
                color_continuous_scale='Blues'
            )
        
        return fig
    
    @staticmethod
    def feature_importance_plot(importance_dict):
        """Gráfico de importancia de características."""
        importance_df = pd.DataFrame(
            list(importance_dict.items()),
            columns=['Feature', 'Importance']
        ).sort_values('Importance', ascending=True).tail(10)
        
        fig = px.bar(
            importance_df,
            x='Importance', y='Feature',
            title='Top 10 Características más Importantes',
            template='plotly_dark',
            orientation='h'
        )
        return fig