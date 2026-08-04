import pandas as pd

class DataCleaner:
    @staticmethod
    def remove_duplicates(df):
        return df.drop_duplicates().copy()

    @staticmethod
    def fill_missing(df, column, strategy='mean'):
        df_clean = df.copy()
        if strategy in ['mean', 'median']:
            df_clean[column] = pd.to_numeric(df_clean[column], errors='coerce')

        if strategy == 'mean':
            fill_value = df_clean[column].mean()
        elif strategy == 'median':
            fill_value = df_clean[column].median()
        elif strategy == 'mode':
            fill_value = df_clean[column].mode()[0] if not df_clean[column].mode().empty else None
        elif strategy == 'drop':
            return df_clean.dropna(subset=[column])
        else:
            raise ValueError(f"Estrategia no soportada: {strategy}")

        if fill_value is not None and not pd.isna(fill_value):
            df_clean[column] = df_clean[column].fillna(fill_value)
        return df_clean