"""
Model Training — train an XGBoost classifier for funding success prediction.

Logs experiments to MLflow and saves the best model as model.pkl.
"""

import os
import logging
import joblib
import mlflow
import mlflow.xgboost
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from app.utils.feature_engineering import preprocess_pipeline

logger = logging.getLogger(__name__)

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")


def train(df: pd.DataFrame, target_col: str = "funding_success") -> dict:
    """
    Full training pipeline: preprocess → split → train → evaluate → log → save.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataset containing features and target column.
    target_col : str
        Name of the binary target column.

    Returns
    -------
    dict
        Evaluation metrics: accuracy, f1_score, roc_auc.
    """
    # --- Preprocess -------------------------------------------------------
    df, artifacts = preprocess_pipeline(df)

    feature_cols = [
        "industry_encoded",
        "location_encoded",
        "team_size",
        "startup_age",
        "investor_count",
    ]
    X = df[feature_cols]
    y = df[target_col]

    # --- Split ------------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # --- Train ------------------------------------------------------------
    params = {
        "learning_rate": 0.1,
        "max_depth": 6,
        "n_estimators": 200,
        "use_label_encoder": False,
        "eval_metric": "logloss",
        "random_state": 42,
    }
    model = XGBClassifier(**params)

    with mlflow.start_run(run_name="xgboost_funding_prediction"):
        model.fit(X_train, y_train)

        # --- Evaluate -----------------------------------------------------
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "f1_score": f1_score(y_test, y_pred),
            "roc_auc": roc_auc_score(y_test, y_proba),
        }

        # --- Log to MLflow ------------------------------------------------
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)
        mlflow.xgboost.log_model(model, artifact_path="model")

        logger.info("Training complete. Metrics: %s", metrics)

    # --- Save model to disk -----------------------------------------------
    joblib.dump(model, MODEL_PATH)
    logger.info("Model saved to %s", MODEL_PATH)

    # Also save preprocessing artifacts for inference
    joblib.dump(artifacts, os.path.join(MODEL_DIR, "preprocessing_artifacts.pkl"))

    return metrics


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Run this module with a DataFrame to train. See Phase 5 in the SOP.")
