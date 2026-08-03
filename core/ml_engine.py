from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, accuracy_score, classification_report
from sklearn.metrics import root_mean_squared_error
import pandas as pd

class MLEngine:
    def __init__(self, df, target, problem_type=None):
        self.df = df.dropna(subset=[target])  # eliminar filas sin target
        self.target = target
        self.problem_type = problem_type or self._detect_problem_type()
        self.model = None
        self.preprocessor = None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        
    def _detect_problem_type(self):
        if pd.api.types.is_numeric_dtype(self.df[self.target]):
            return 'regression'
        else:
            return 'classification'
    
    def preprocess_data(self):
        X = self.df.drop(columns=[self.target])
        y = self.df[self.target]
        # Separar numéricas y categóricas
        num_cols = X.select_dtypes(include=['int64','float64']).columns.tolist()
        cat_cols = X.select_dtypes(include=['object','category']).columns.tolist()
        # Preprocesador: escala numéricas, codifica categóricas
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), num_cols),
                ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
            ])
        # Split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)
    
    def train(self, model_name='random_forest'):
        if self.preprocessor is None:
            self.preprocess_data()
        if self.problem_type == 'regression':
            if model_name == 'random_forest':
                model = RandomForestRegressor(n_estimators=100, random_state=42)
            else:
                model = LinearRegression()
        else:
            if model_name == 'random_forest':
                model = RandomForestClassifier(n_estimators=100, random_state=42)
            else:
                model = LogisticRegression(max_iter=1000)
        
        pipeline = Pipeline(steps=[('preprocessor', self.preprocessor),
                                   ('model', model)])
        pipeline.fit(self.X_train, self.y_train)
        self.model = pipeline
        return self
    
    def evaluate(self):
        preds = self.model.predict(self.X_test)
        if self.problem_type == 'regression':
            return {
                'R2': r2_score(self.y_test, preds),
                'MAE': mean_absolute_error(self.y_test, preds),
                'RMSE': mean_squared_error(self.y_test, preds, squared=False)
            }
        else:
            return {
                'Accuracy': accuracy_score(self.y_test, preds),
                'Report': classification_report(self.y_test, preds, output_dict=True)
            }
    
    def get_feature_importance(self):
        if hasattr(self.model.named_steps['model'], 'feature_importances_'):
            importances = self.model.named_steps['model'].feature_importances_
            # Obtener nombres de características después del preprocesador
            feature_names = (self.model.named_steps['preprocessor']
                             .get_feature_names_out())
            return dict(zip(feature_names, importances))
        return None