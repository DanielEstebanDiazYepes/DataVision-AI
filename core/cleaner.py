class DataCleaner:
    @staticmethod
    def remove_duplicates(df):
        return df.drop_duplicates()
    
    @staticmethod
    def fill_missing(df, column, strategy='mean'):
        if strategy == 'mean':
            df[column].fillna(df[column].mean(), inplace=True)
        elif strategy == 'median':
            df[column].fillna(df[column].median(), inplace=True)
        elif strategy == 'mode':
            df[column].fillna(df[column].mode()[0], inplace=True)
        elif strategy == 'drop':
            df.dropna(subset=[column], inplace=True)
        # Escalable: agregar más estrategias (forward fill, interpolación)
        return df