"""
Model Service — load trained model and run inference.

Handles loading model.pkl and providing predictions via the predict() method.
"""

import os
import joblib
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "model.pkl")

_model = None


def load_model():
    """Load the trained model from disk."""
    global _model
    if os.path.exists(MODEL_PATH):
        _model = joblib.load(MODEL_PATH)
    else:
        _model = None
    return _model


def get_model():
    """Return the loaded model, loading it if necessary."""
    global _model
    if _model is None:
        load_model()
    return _model


def predict(features: dict) -> float:
    """
    Run inference on a single sample.

    Parameters
    ----------
    features : dict
        Keys: industry (encoded), team_size, startup_age, investor_count

    Returns
    -------
    float
        Predicted probability of funding success.
    """
    model = get_model()
    if model is None:
        raise RuntimeError("Model not available. Train the model first (Phase 5).")

    # Build feature array in expected order
    X = np.array([[
        features["industry_encoded"],
        features["team_size"],
        features["startup_age"],
        features["investor_count"],
    ]])
    proba = model.predict_proba(X)[0][1]  # probability of class 1 (success)
    return float(proba)
