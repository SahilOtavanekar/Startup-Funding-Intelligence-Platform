"""
Feature Engineering — transform raw data into ML-ready features.

Provides reusable preprocessing pipeline functions for both
training and real-time inference.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import LabelEncoder, StandardScaler


# ---------------------------------------------------------------------------
# Derived features
# ---------------------------------------------------------------------------

def compute_startup_age(df: pd.DataFrame) -> pd.DataFrame:
    """Add startup_age column (current year − founded_year)."""
    current_year = datetime.now().year
    df["startup_age"] = current_year - df["founded_year"]
    df["startup_age"] = df["startup_age"].clip(lower=0)
    return df


def compute_funding_history(df: pd.DataFrame) -> pd.DataFrame:
    """Add previous_funding_rounds count per startup."""
    round_counts = (
        df.groupby("startup_id")["funding_round"]
        .count()
        .reset_index()
        .rename(columns={"funding_round": "previous_funding_rounds"})
    )
    df = df.merge(round_counts, on="startup_id", how="left")
    df["previous_funding_rounds"] = df["previous_funding_rounds"].fillna(0).astype(int)
    return df


# ---------------------------------------------------------------------------
# Encoding & scaling
# ---------------------------------------------------------------------------

def encode_categoricals(df: pd.DataFrame, columns: list[str]) -> tuple[pd.DataFrame, dict]:
    """
    Label-encode specified categorical columns.

    Returns the transformed DataFrame and a dict of fitted LabelEncoders.
    """
    encoders = {}
    for col in columns:
        le = LabelEncoder()
        df[col + "_encoded"] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
    return df, encoders


def scale_numericals(df: pd.DataFrame, columns: list[str]) -> tuple[pd.DataFrame, StandardScaler]:
    """
    Standard-scale specified numerical columns.

    Returns the transformed DataFrame and the fitted scaler.
    """
    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df, scaler


# ---------------------------------------------------------------------------
# Full pipeline
# ---------------------------------------------------------------------------

def preprocess_pipeline(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Run the complete preprocessing pipeline.

    Returns the processed DataFrame and a dict of artifacts
    (encoders, scaler) needed for inference.
    """
    # Handle missing values
    df = df.fillna({
        "team_size": df["team_size"].median(),
        "investor_count": 0,
        "founded_year": df["founded_year"].mode().iloc[0] if not df["founded_year"].mode().empty else 2020,
    })

    # Derived features
    df = compute_startup_age(df)

    # Encode categoricals
    categorical_cols = ["industry", "location"]
    df, encoders = encode_categoricals(df, categorical_cols)

    # Scale numericals
    numerical_cols = ["team_size", "startup_age", "investor_count"]
    df, scaler = scale_numericals(df, numerical_cols)

    artifacts = {"encoders": encoders, "scaler": scaler}
    return df, artifacts
