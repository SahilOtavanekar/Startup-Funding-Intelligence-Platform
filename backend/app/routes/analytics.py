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


def _clean_text(text):
    """Clean un-escaped unicode/special characters and normalize city names."""
    if not isinstance(text, str):
        return str(text)
    # Remove common malformed patterns like \\xc2\\xa0 which appear in raw data
    text = text.encode('ascii', 'ignore').decode('ascii').strip()
    
    # Normalize common duplicates
    if text.lower() == "bangalore":
        return "Bengaluru"
    return text


def _load_local_data() -> pd.DataFrame:
    """Load the local training CSV for analytics."""
    if not os.path.exists(TRAINING_DATA_PATH):
        raise FileNotFoundError("Training data not found. Run seed_data first.")
    df = pd.read_csv(TRAINING_DATA_PATH)
    # Proactively clean names
    if "industry" in df.columns:
        df["industry"] = df["industry"].apply(_clean_text)
    if "location" in df.columns:
        df["location"] = df["location"].apply(_clean_text)
    if "startup_name" in df.columns:
        df["startup_name"] = df["startup_name"].apply(_clean_text)
    return df


# ---------------------------------------------------------------------------
# GET /industry-trends
# ---------------------------------------------------------------------------
@router.get("/industry-trends")
@limiter.limit("30/minute")
async def industry_trends(request: Request):
    """Return funding distribution and growth trends by industry (Supabase or Local)."""
    try:
        # Read from local CSV
        df = _load_local_data()

        # --- Funding by Industry -------------------------------------------
        industry_funding = (
            df.groupby("industry")["total_raised"]
            .sum()
            .sort_values(ascending=False)
            .head(15)  # Limit to Top 15 for readability
            .reset_index()
        )
        industry_funding.columns = ["name", "funding"]
        # Convert to millions for readability
        industry_funding["funding"] = (
            industry_funding["funding"] / 1_000_000
        ).round(1)

        # --- Success rate by Industry --------------------------------------
        # Filter for industries that have at least a minimum sample size (e.g., 10 startups)
        # to avoid niche categories skewing the 100% success rate at the top
        industry_groups = df.groupby("industry")
        success_rate = (
            industry_groups["funding_success"]
            .agg(["mean", "size"])
            .query("size >= 10")  # Minimum 10 startups to be considered
            ["mean"]
            .sort_values(ascending=False)
            .head(15)
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

        # --- Prophet Forecast ----------------------------------------------
        forecast_data = []
        try:
            from prophet import Prophet
            if len(year_funding) > 3:
                prophet_df = pd.DataFrame({
                    'ds': pd.to_datetime(year_funding['year'], format='%Y'),
                    'y': year_funding['amount']
                })
                logging.getLogger('cmdstanpy').setLevel(logging.ERROR)
                m = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)
                m.fit(prophet_df)
                
                future = m.make_future_dataframe(periods=4, freq='YS')
                forecast = m.predict(future)
                
                forecast['year'] = forecast['ds'].dt.year
                max_hist_year = year_funding['year'].max()
                
                # To connect the line smoothly in Recharts, append the last historical year as the start of the forecast
                last_hist = year_funding.iloc[-1]
                forecast_data.append({"year": int(last_hist['year']), "forecast": float(last_hist['amount'])})
                
                for _, row in forecast.iterrows():
                    if row['year'] > max_hist_year:
                        forecast_data.append({
                            "year": int(row['year']),
                            "forecast": max(0, round(row['yhat'], 1)) # Don't predict negative funding
                        })
        except Exception as e:
            logger.error(f"Prophet forecasting error: {e}")

        # --- Funding Round Distribution ------------------------------------
        round_counts = df["previous_funding_rounds"].value_counts().sort_index()
        round_labels = {
            0: "Pre-Seed",
            1: "Seed",
            2: "Series A",
            3: "Series B",
            4: "Series C",
            5: "Late Stage"
        }
        round_distribution = [
            {
                "name": round_labels.get(k, f"Round {k}"),
                "value": int(v),
            }
            for k, v in round_counts.items()
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
            "forecast_funding": forecast_data,
            "round_distribution": round_distribution,
            "location_distribution": location_counts.to_dict(orient="records"),
            "team_by_success": team_by_success.to_dict(orient="records"),
            "total_startups": len(df),
            "total_funded": int(df["funding_success"].sum()),
            "total_industries": int(df["industry"].nunique()),
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
async def list_startups(request: Request, search: str = None, industry: str = None, limit: int = 100):
    """Return filtered startup records from the entire dataset."""
    try:
        # Read from local CSV (3,000+ records)
        df = _load_local_data()
        
        # Apply Industry Filter
        if industry and industry != "All" and industry != "":
            df = df[df["industry"] == industry]
            
        # Apply Search Filter (Name or Location)
        if search:
            search = search.lower()
            mask = (
                df["startup_name"].str.lower().str.contains(search, na=False) |
                df["location"].str.lower().str.contains(search, na=False)
            )
            df = df[mask]

        total_matches = len(df)
        
        # Select columns and limit results for performance
        startups = df[
            ["startup_name", "industry", "location", "founded_year",
             "team_size", "startup_age", "investor_count",
             "total_raised", "funding_success"]
        ].head(limit)

        return {
            "startups": startups.to_dict(orient="records"),
            "total_matches": total_matches,
            "total_dataset": 3044 # or len(_load_local_data())
        }

    except Exception as e:
        logger.error("Startups endpoint error: %s", e)
        raise HTTPException(status_code=500, detail=f"Error: {e}")
