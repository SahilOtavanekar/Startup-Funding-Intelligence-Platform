"""
Prediction routes — POST /predict

Accepts startup parameters and returns the predicted funding success probability.
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
import logging

from app.services.model_service import predict
from app.core.limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter()


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class PredictionRequest(BaseModel):
    industry: str = Field(..., description="Startup industry category")
    team_size: int = Field(..., ge=1, description="Number of team members")
    startup_age: int = Field(..., ge=0, description="Age of the startup in years")
    investor_count: int = Field(..., ge=0, description="Number of investors")
    location: str = Field(
        default="San Francisco, CA",
        description="Startup location (optional)",
    )
    previous_funding_rounds: int = Field(
        default=1,
        ge=0,
        description="Number of previous funding rounds (optional)",
    )


class PredictionResponse(BaseModel):
    funding_success_probability: float = Field(
        ..., ge=0, le=1, description="Predicted probability of funding success"
    )
    feature_importance: dict | None = Field(
        None, description="Feature importance from the model"
    )


# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------
@router.post("/predict", response_model=PredictionResponse)
@limiter.limit("15/minute")
async def predict_funding(request: PredictionRequest, request_meta: Request):
    """Predict the probability of funding success for a startup."""
    try:
        result = predict(request.model_dump())
        return PredictionResponse(
            funding_success_probability=result["funding_success_probability"],
            feature_importance=result.get("feature_importance"),
        )
    except RuntimeError as e:
        logger.error("Prediction failed: %s", e)
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error("Unexpected prediction error: %s", e)
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
