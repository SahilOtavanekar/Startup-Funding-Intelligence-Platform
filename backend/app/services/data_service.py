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
    """Fetch startup records from the database."""
    client = get_client()
    response = client.table("startups").select("*").limit(limit).execute()
    return response.data


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

def get_industry_trends():
    """Aggregate funding data by industry for trend analysis."""
    client = get_client()
    # Fetch all funding rounds joined with startup industry
    response = (
        client.table("funding_rounds")
        .select("funding_amount, funding_round, date, startups(industry)")
        .execute()
    )
    return response.data
