"""
Prediction routes — POST /predict

Accepts startup parameters and returns the predicted funding success probability.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class PredictionRequest(BaseModel):
    industry: str = Field(..., description="Startup industry category")
    team_size: int = Field(..., ge=1, description="Number of team members")
    startup_age: int = Field(..., ge=0, description="Age of the startup in years")
    investor_count: int = Field(..., ge=0, description="Number of investors")


class PredictionResponse(BaseModel):
    funding_success_probability: float = Field(
        ..., ge=0, le=1, description="Predicted probability of funding success"
    )
    feature_importance: dict | None = Field(
        None, description="SHAP-based feature importance (optional)"
    )


# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------
@router.post("/predict", response_model=PredictionResponse)
async def predict_funding(request: PredictionRequest):
    """Predict the probability of funding success for a startup."""
    # TODO: Phase 6 — wire up model_service for real inference
    raise HTTPException(status_code=503, detail="Model not loaded yet. Complete Phase 5 first.")
