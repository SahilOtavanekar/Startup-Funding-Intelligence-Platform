"""
Startup Funding Intelligence Platform — FastAPI Entry Point

Initializes the FastAPI application, registers route modules,
and configures CORS middleware.
"""

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import prediction, analytics

app = FastAPI(
    title="Startup Funding Intelligence API",
    description="Predict startup funding success and explore funding trends.",
    version="1.0.0",
)

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
app.include_router(prediction.router, tags=["Prediction"])
app.include_router(analytics.router, tags=["Analytics"])


@app.get("/", tags=["Health"])
async def root():
    """Health-check endpoint."""
    return {"status": "ok", "message": "Startup Funding Intelligence API is running."}
