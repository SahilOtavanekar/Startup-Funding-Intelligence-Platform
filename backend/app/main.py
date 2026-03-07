"""
Startup Funding Intelligence Platform — FastAPI Entry Point

Initializes the FastAPI application, registers route modules,
and configures CORS middleware.
"""

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.routes import prediction, analytics
from app.core.security import get_api_key
from app.core.limiter import limiter

# ---------------------------------------------------------------------------
# App Initialization
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Startup Funding Intelligence API",
    description="Predict startup funding success and explore funding trends.",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ---------------------------------------------------------------------------
# CORS — allow the React frontend origin
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(prediction.router, tags=["Prediction"], dependencies=[Depends(get_api_key)])
app.include_router(analytics.router, tags=["Analytics"], dependencies=[Depends(get_api_key)])


@app.get("/", tags=["Health"])
async def root():
    """Health-check endpoint."""
    return {"status": "ok", "message": "Startup Funding Intelligence API is running."}
