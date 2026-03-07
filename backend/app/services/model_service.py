"""
Model Service — load trained model and run inference.

Handles loading model.pkl and preprocessing_artifacts.pkl,
then providing predictions via the predict() method.
"""

import os
import logging
import joblib
import numpy as np

logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
ARTIFACTS_PATH = os.path.join(MODEL_DIR, "preprocessing_artifacts.pkl")

_model = None
_artifacts = None


def load_model():
    """Load the trained model and preprocessing artifacts from disk."""
    global _model, _artifacts

    if os.path.exists(MODEL_PATH):
        _model = joblib.load(MODEL_PATH)
        logger.info("✅ Model loaded from %s", MODEL_PATH)
    else:
        _model = None
        logger.warning("⚠️  Model file not found at %s", MODEL_PATH)

    if os.path.exists(ARTIFACTS_PATH):
        _artifacts = joblib.load(ARTIFACTS_PATH)
        logger.info("✅ Preprocessing artifacts loaded")
    else:
        _artifacts = None
        logger.warning("⚠️  Preprocessing artifacts not found at %s", ARTIFACTS_PATH)

    return _model


def get_model():
    """Return the loaded model, loading it if necessary."""
    global _model
    if _model is None:
        load_model()
    return _model


def get_artifacts():
    """Return preprocessing artifacts."""
    global _artifacts
    if _artifacts is None:
        load_model()
    return _artifacts


def predict(features: dict) -> dict:
    """
    Run inference on a single sample.

    Parameters
    ----------
    features : dict
        Keys: industry, team_size, startup_age, investor_count
        Optionally: location, previous_funding_rounds

    Returns
    -------
    dict
        {
            "funding_success_probability": float,
            "feature_importance": dict | None
        }
    """
    model = get_model()
    if model is None:
        raise RuntimeError(
            "Model not available. Train the model first: "
            "python -m app.models.train_model"
        )

    artifacts = get_artifacts()

    # --- Encode categoricals ------------------------------------------------
    industry_val = features.get("industry", "Technology")
    location_val = features.get("location", "San Francisco, CA")

    industry_encoder = artifacts["industry_encoder"]
    location_encoder = artifacts["location_encoder"]

    # Handle unseen categories gracefully
    try:
        industry_encoded = industry_encoder.transform([industry_val])[0]
    except ValueError:
        industry_encoded = 0  # fallback

    try:
        location_encoded = location_encoder.transform([location_val])[0]
    except ValueError:
        location_encoded = 0  # fallback

    team_size = float(features.get("team_size", 5))
    startup_age = float(features.get("startup_age", 3))
    investor_count = float(features.get("investor_count", 2))
    previous_rounds = float(features.get("previous_funding_rounds", 1))

    # --- Scale numerical features -------------------------------------------
    scaler = artifacts["scaler"]
    numerical_vals = np.array([[team_size, startup_age, investor_count, previous_rounds]])
    scaled = scaler.transform(numerical_vals)[0]

    # --- Build feature vector in expected order------------------------------
    X = np.array([[
        industry_encoded,
        location_encoded,
        scaled[0],  # team_size (scaled)
        scaled[1],  # startup_age (scaled)
        scaled[2],  # investor_count (scaled)
        scaled[3],  # previous_funding_rounds (scaled)
    ]])

    proba = model.predict_proba(X)[0][1]  # probability of class 1 (success)

    # --- Feature importance (from model) ------------------------------------
    try:
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
        elif hasattr(model, "calibrated_classifiers_"):
            # Average importances from all folds in the calibrated ensemble
            importances = np.mean([
                clf.estimator.feature_importances_ 
                for clf in model.calibrated_classifiers_
                if hasattr(clf.estimator, "feature_importances_")
            ], axis=0)
        else:
            importances = None

        if importances is not None:
            feature_names = artifacts.get("feature_cols", [
                "industry", "location", "team_size",
                "startup_age", "investor_count", "previous_funding_rounds"
            ])
            # Make human-readable names
            readable_names = [
                n.replace("_encoded", "") for n in feature_names
            ]
            importance_dict = {
                name: round(float(imp), 4)
                for name, imp in zip(readable_names, importances)
            }
        else:
            importance_dict = None
    except Exception as e:
        logger.warning("Could not extract feature importance: %s", e)
        importance_dict = None

    return {
        "funding_success_probability": float(round(proba, 4)),
        "feature_importance": importance_dict,
    }
