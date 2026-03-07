"""
Data Service — interact with Supabase for data queries.

Handles CRUD operations and analytics aggregations.
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

_client: Client | None = None


def get_client() -> Client:
    """Return a Supabase client (singleton)."""
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise RuntimeError(
                "SUPABASE_URL and SUPABASE_KEY must be set in environment variables."
            )
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


# ---------------------------------------------------------------------------
# Startups
# ---------------------------------------------------------------------------

def get_all_startups(limit: int = 100):
    """Fetch startup records from the database with aggregated funding amounts."""
    client = get_client()
    # Fetch startups and their related funding rounds
    response = client.table("startups").select("*, funding_rounds(funding_amount)").limit(limit).execute()
    
    data = response.data
    # Flatten the result: sum(funding_rounds.funding_amount) as total_raised
    for item in data:
        rounds = item.pop("funding_rounds", [])
        total = sum(r["funding_amount"] for r in rounds if r.get("funding_amount"))
        item["total_raised"] = total
        
    return data


# ---------------------------------------------------------------------------
# Funding Rounds
# ---------------------------------------------------------------------------

def get_funding_rounds(startup_id: str | None = None):
    """Fetch funding rounds, optionally filtered by startup_id."""
    client = get_client()
    query = client.table("funding_rounds").select("*")
    if startup_id:
        query = query.eq("startup_id", startup_id)
    response = query.execute()
    return response.data


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------

def get_industry_analytics_data():
    """Aggregate funding data from Supabase into the dashboard JSON format."""
    client = get_client()
    
    # Fetch data
    startups_res = client.table("startups").select("*").execute()
    rounds_res = client.table("funding_rounds").select("*").execute()
    
    if not startups_res.data:
        return None
        
    import pandas as pd
    df_s = pd.DataFrame(startups_res.data)
    df_r = pd.DataFrame(rounds_res.data)
    
    # Merge if rounds exist
    if not df_r.empty:
        df = pd.merge(df_s, df_r, left_on="id", right_on="startup_id", how="left")
    else:
        df = df_s
        df["funding_amount"] = 0
        df["funding_round"] = "None"
        
    df["funding_success"] = df["funding_round"].apply(lambda x: 1 if "Growth" in str(x) else 0)

    # Aggregations (Matched logic from analytics.py)
    industry_funding = df.groupby("industry")["funding_amount"].sum().sort_values(ascending=False).reset_index()
    industry_funding.columns = ["name", "funding"]
    industry_funding["funding"] = (industry_funding["funding"] / 1_000_000).round(1)

    success_rate = df.groupby("industry")["funding_success"].mean().sort_values(ascending=False).reset_index()
    success_rate.columns = ["name", "success_rate"]
    success_rate["success_rate"] = (success_rate["success_rate"] * 100).round(1)

    # --- Funding by Year -----------------------------------------------
    year_funding = df.groupby("founded_year")["funding_amount"].sum().reset_index()
    year_funding.columns = ["year", "amount"]
    year_funding["amount"] = (year_funding["amount"] / 1_000_000).round(1)
    year_funding = year_funding.sort_values("year")

    # --- Funding Round Distribution ------------------------------------
    round_counts = df["funding_round"].value_counts()
    round_distribution = [
        {"name": str(k), "value": int(v)}
        for k, v in round_counts.items()
        if k != "None"
    ]

    # --- Location Distribution -----------------------------------------
    location_counts = df["location"].value_counts().head(10).reset_index()
    location_counts.columns = ["name", "count"]

    # --- Average team size by success ----------------------------------
    team_by_success = df.groupby("funding_success")["team_size"].mean().reset_index()
    team_by_success.columns = ["success", "avg_team_size"]
    team_by_success["success"] = team_by_success["success"].map({0: "Not Funded", 1: "Funded"})
    team_by_success["avg_team_size"] = team_by_success["avg_team_size"].round(1)

    return {
        "industry_funding": industry_funding.to_dict(orient="records"),
        "success_rate": success_rate.to_dict(orient="records"),
        "year_funding": year_funding.to_dict(orient="records"),
        "round_distribution": round_distribution,
        "location_distribution": location_counts.to_dict(orient="records"),
        "team_by_success": team_by_success.to_dict(orient="records"),
        "total_startups": len(df_s),
        "total_funded": int(df["funding_success"].sum()),
        "avg_funding": round(float(df["funding_amount"].mean() / 1_000_000), 2) if not df.empty else 0,
        "source": "supabase"
    }
