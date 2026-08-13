import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error, accuracy_score, classification_report
from utils.logging_config import setup_logging

logger = setup_logging()

class MLEngine:
    def __init__(self, df, target, problem_type=None, test_size=0.2, random_state=42):
        self.df = df.dropna(subset=[target]).copy()
        self.target = target
        self.problem_type = problem_type or self._detect_problem_type()
        self.test_size = test_size
        self.random_state = random_state
        self.model = None
        self.preprocessor = None
        self.X_train = self.X_test = self.y_train = self.y_test = None
        logger.info("MLEngine inicializado. Target: %s | Tipo: %s", target, self.problem_type)

    def _detect_problem_type(self):
        if pd.api.types.is_numeric_dtype(self.df[self.target]):
            return 'regression'
        else:
            return 'classification'

    def preprocess_data(self):
        X = self.df.drop(columns=[self.target])
        y = self.df[self.target]
        num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
        logger.info("Preprocesando: %s numéricas, %s categóricas", len(num_cols), len(cat_cols))

        num_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        cat_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder(handle_unknown='ignore', max_categories=20, sparse_output=False))
        ])
        self.preprocessor = ColumnTransformer([
            ('num', num_pipeline, num_cols),
            ('cat', cat_pipeline, cat_cols)
        ])
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state)
        logger.info("Train size: %s | Test size: %s", len(self.X_train), len(self.X_test))

    def train(self, model_name='random_forest'):
        if self.preprocessor is None:
            self.preprocess_data()
        if self.problem_type == 'regression':
            model = RandomForestRegressor(n_estimators=100, random_state=self.random_state) \
                if model_name == 'random_forest' else LinearRegression()
        else:
            model = RandomForestClassifier(n_estimators=100, random_state=self.random_state) \
                if model_name == 'random_forest' else LogisticRegression(max_iter=1000)
        self.model = Pipeline([
            ('preprocessor', self.preprocessor),
            ('model', model)
        ])
        logger.info("Entrenando modelo '%s' (%s)", model_name, self.problem_type)
        self.model.fit(self.X_train, self.y_train)
        return self

    def evaluate(self):
        preds = self.model.predict(self.X_test)
        if self.problem_type == 'regression':
            metrics = {
                'R2': r2_score(self.y_test, preds),
                'MAE': mean_absolute_error(self.y_test, preds),
                'RMSE': root_mean_squared_error(self.y_test, preds)
            }
        else:
            metrics = {
                'Accuracy': accuracy_score(self.y_test, preds),
                'Report': classification_report(self.y_test, preds, output_dict=True)
            }
        logger.info("Métricas del modelo: %s", metrics)
        return metrics

    def get_feature_importance(self):
        if hasattr(self.model.named_steps['model'], 'feature_importances_'):
            importances = self.model.named_steps['model'].feature_importances_
            feature_names = self.model.named_steps['preprocessor'].get_feature_names_out()
            return dict(zip(feature_names, importances))
        return None