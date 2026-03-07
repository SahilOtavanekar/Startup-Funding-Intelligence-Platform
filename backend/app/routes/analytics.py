"""
Analytics routes — GET /industry-trends, GET /startups

Returns aggregated analytics and raw startup records.
Reads from local training_data.csv as primary source,
with optional Supabase fallback for live data.
"""

import os
import logging
from collections import defaultdict

import pandas as pd
from fastapi import APIRouter, HTTPException, Request
from app.core.limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter()

# Path to training data (always available locally)
TRAINING_DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "models", "training_data.csv"
)


def _load_local_data() -> pd.DataFrame:
    """Load the local training CSV for analytics."""
    if not os.path.exists(TRAINING_DATA_PATH):
        raise FileNotFoundError("Training data not found. Run seed_data first.")
    return pd.read_csv(TRAINING_DATA_PATH)


# ---------------------------------------------------------------------------
# GET /industry-trends
# ---------------------------------------------------------------------------
@router.get("/industry-trends")
@limiter.limit("30/minute")
async def industry_trends(request: Request):
    """Return funding distribution and growth trends by industry (Supabase or Local)."""
    try:
        # Try Supabase first
        supabase_url = os.getenv("SUPABASE_URL", "")
        if supabase_url and supabase_url != "https://your-project.supabase.co":
            try:
                from app.services.data_service import get_industry_analytics_data
                data = get_industry_analytics_data()
                if data:
                    return data
            except Exception as e:
                logger.warning("Supabase Industry Trends failed: %s", e)

        # Fallback to local CSV
        df = _load_local_data()

        # --- Funding by Industry -------------------------------------------
        industry_funding = (
            df.groupby("industry")["total_raised"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        industry_funding.columns = ["name", "funding"]
        # Convert to millions for readability
        industry_funding["funding"] = (
            industry_funding["funding"] / 1_000_000
        ).round(1)

        # --- Success rate by Industry --------------------------------------
        success_rate = (
            df.groupby("industry")["funding_success"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )
        success_rate.columns = ["name", "success_rate"]
        success_rate["success_rate"] = (success_rate["success_rate"] * 100).round(1)

        # --- Funding by Year -----------------------------------------------
        year_funding = (
            df.groupby("founded_year")["total_raised"]
            .sum()
            .reset_index()
        )
        year_funding.columns = ["year", "amount"]
        year_funding["amount"] = (year_funding["amount"] / 1_000_000).round(1)
        year_funding = year_funding.sort_values("year")

        # --- Funding Round Distribution ------------------------------------
        round_counts = df["previous_funding_rounds"].value_counts().sort_index()
        round_labels = {0: "Pre-Seed", 1: "Seed", 2: "Series A", 3: "Series B"}
        round_distribution = [
            {
                "name": round_labels.get(k, f"Round {k}"),
                "value": int(v),
            }
            for k, v in round_counts.items()
            if k <= 5
        ]

        # --- Location Distribution -----------------------------------------
        location_counts = (
            df["location"]
            .value_counts()
            .head(10)
            .reset_index()
        )
        location_counts.columns = ["name", "count"]

        # --- Average team size by success ----------------------------------
        team_by_success = (
            df.groupby("funding_success")["team_size"]
            .mean()
            .reset_index()
        )
        team_by_success.columns = ["success", "avg_team_size"]
        team_by_success["success"] = team_by_success["success"].map(
            {0: "Not Funded", 1: "Funded"}
        )
        team_by_success["avg_team_size"] = team_by_success["avg_team_size"].round(1)

        return {
            "industry_funding": industry_funding.to_dict(orient="records"),
            "success_rate": success_rate.to_dict(orient="records"),
            "year_funding": year_funding.to_dict(orient="records"),
            "round_distribution": round_distribution,
            "location_distribution": location_counts.to_dict(orient="records"),
            "team_by_success": team_by_success.to_dict(orient="records"),
            "total_startups": len(df),
            "total_funded": int(df["funding_success"].sum()),
            "avg_funding": round(float(df["total_raised"].mean() / 1_000_000), 2),
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error("Analytics error: %s", e)
        raise HTTPException(status_code=500, detail=f"Analytics error: {e}")


# ---------------------------------------------------------------------------
# GET /startups
# ---------------------------------------------------------------------------
@router.get("/startups")
@limiter.limit("30/minute")
async def list_startups(request: Request, limit: int = 100):
    """Return startup records from local data (or Supabase if configured)."""
    try:
        # Try Supabase first
        supabase_url = os.getenv("SUPABASE_URL", "")
        if supabase_url and supabase_url != "https://your-project.supabase.co":
            try:
                from app.services.data_service import get_all_startups
                data = get_all_startups(limit=limit)
                if data:
                    return {"startups": data, "source": "supabase"}
            except Exception as e:
                logger.warning("Supabase fallback failed: %s", e)

        # Fallback to local CSV
        df = _load_local_data()
        startups = df[
            ["startup_name", "industry", "location", "founded_year",
             "team_size", "startup_age", "investor_count",
             "total_raised", "funding_success"]
        ].head(limit)

        return {
            "startups": startups.to_dict(orient="records"),
            "source": "local",
            "total": len(df),
        }

    except Exception as e:
        logger.error("Startups endpoint error: %s", e)
        raise HTTPException(status_code=500, detail=f"Error: {e}")
