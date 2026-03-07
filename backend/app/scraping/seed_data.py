"""
Seed Data Generator — create realistic synthetic startup funding data.

Generates 500+ startup records with funding rounds and investors,
then uploads them to Supabase.  Also saves a local CSV for ML training.

Usage:
    python -m app.scraping.seed_data
"""

import os
import random
import uuid
import logging
from datetime import date, timedelta
from typing import Any

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# =============================================================================
# Configuration
# =============================================================================

NUM_STARTUPS = 500
MIN_YEAR = 2010
MAX_YEAR = 2024

INDUSTRIES = [
    "Technology", "Healthcare", "Finance", "Education", "E-commerce",
    "Energy", "Real Estate", "Food & Beverage", "Transportation", "Media",
    "Agriculture", "Manufacturing", "Retail", "Gaming", "SaaS",
]

LOCATIONS = [
    "San Francisco, CA", "New York, NY", "Austin, TX", "Boston, MA",
    "Seattle, WA", "Los Angeles, CA", "Chicago, IL", "Denver, CO",
    "Miami, FL", "Atlanta, GA", "London, UK", "Berlin, Germany",
    "Bangalore, India", "Singapore", "Tel Aviv, Israel",
    "Toronto, Canada", "Sydney, Australia", "São Paulo, Brazil",
]

FUNDING_ROUNDS = ["Pre-Seed", "Seed", "Series A", "Series B", "Series C", "Series D"]

INVESTOR_TYPES = ["VC", "Angel", "Corporate", "Accelerator", "Government"]

INVESTOR_NAMES = [
    "Sequoia Capital", "Andreessen Horowitz", "Y Combinator", "Tiger Global",
    "Accel Partners", "Lightspeed Ventures", "Khosla Ventures", "Founders Fund",
    "Benchmark Capital", "Greylock Partners", "Index Ventures", "General Catalyst",
    "Bessemer Venture Partners", "NEA", "Kleiner Perkins", "SoftBank Vision Fund",
    "GV (Google Ventures)", "Insight Partners", "Sapphire Ventures", "IVP",
    "Ribbit Capital", "Coatue Management", "First Round Capital", "Redpoint Ventures",
    "Mayfield Fund", "Matrix Partners", "Battery Ventures", "Scale Venture Partners",
    "Innovation Endeavors", "Emergence Capital", "Tech Angel Group", "Seedcamp",
    "500 Global", "Plug and Play", "Techstars", "MassChallenge",
    "Microsoft Ventures", "Intel Capital", "Samsung NEXT", "Cisco Investments",
]

STARTUP_PREFIXES = [
    "Neo", "Hyper", "Data", "Cloud", "Smart", "Fin", "Med", "Eco",
    "Quantum", "Nexus", "Vertex", "Apex", "Zenith", "Nova", "Pulse",
    "Flux", "Synth", "Core", "Pixel", "Cyber", "Proto", "Meta",
    "Alpha", "Omni", "Velo", "Agri", "Bio", "Nano", "Solar", "Urban",
]

STARTUP_SUFFIXES = [
    "Labs", "AI", "Tech", "Hub", "Works", "Logic", "Systems", "Flow",
    "Bridge", "Path", "Forge", "Stack", "Wave", "Grid", "Link",
    "Sphere", "Mind", "Scale", "Base", "Point", "Sense", "Craft",
    "Health", "Pay", "Learn", "Ship", "Store", "Play", "Drive", "Farm",
]


# =============================================================================
# Generator Functions
# =============================================================================

def _random_startup_name() -> str:
    """Generate a plausible startup name."""
    return f"{random.choice(STARTUP_PREFIXES)}{random.choice(STARTUP_SUFFIXES)}"


def _funding_amount_for_round(funding_round: str) -> float:
    """Return a realistic funding amount ($) for the given round type."""
    ranges = {
        "Pre-Seed": (50_000, 500_000),
        "Seed": (250_000, 3_000_000),
        "Series A": (2_000_000, 20_000_000),
        "Series B": (10_000_000, 60_000_000),
        "Series C": (30_000_000, 150_000_000),
        "Series D": (80_000_000, 500_000_000),
    }
    lo, hi = ranges.get(funding_round, (100_000, 5_000_000))
    return round(random.uniform(lo, hi), 2)


def _team_size_for_age(startup_age: int) -> int:
    """Estimate team size correlated with startup age."""
    base = random.randint(2, 8)
    growth = int(startup_age * random.uniform(1.5, 5.0))
    return max(2, base + growth)


def _determine_funding_success(
    industry: str,
    team_size: int,
    startup_age: int,
    investor_count: int,
    total_raised: float,
) -> int:
    """
    Deterministic-ish funding success label based on multiple signals.
    1 = success (received follow-on / later-stage funding),
    0 = not yet successful.

    This creates a learnable but non-trivial pattern for the ML model.
    """
    score = 0.0
    # Industry boost
    high_growth = {"Technology", "SaaS", "Healthcare", "Finance", "E-commerce"}
    if industry in high_growth:
        score += 0.15
    # Team size signal
    if team_size >= 10:
        score += 0.15
    elif team_size >= 5:
        score += 0.08
    # Age signal (sweet spot: 2-7 years)
    if 2 <= startup_age <= 7:
        score += 0.15
    elif startup_age > 7:
        score += 0.05
    # Investor count signal
    if investor_count >= 5:
        score += 0.20
    elif investor_count >= 3:
        score += 0.12
    elif investor_count >= 1:
        score += 0.05
    # Total raised signal
    if total_raised >= 10_000_000:
        score += 0.20
    elif total_raised >= 2_000_000:
        score += 0.10
    elif total_raised >= 500_000:
        score += 0.05

    # Add randomness so the boundary isn't perfectly separable
    score += random.uniform(-0.15, 0.15)
    return 1 if score >= 0.40 else 0


def generate_startups() -> list[dict[str, Any]]:
    """Generate a list of synthetic startup records."""
    used_names: set[str] = set()
    startups = []

    for _ in range(NUM_STARTUPS):
        # Unique name
        name = _random_startup_name()
        while name in used_names:
            name = _random_startup_name()
        used_names.add(name)

        founded_year = random.randint(MIN_YEAR, MAX_YEAR)
        startup_age = 2026 - founded_year
        industry = random.choice(INDUSTRIES)
        location = random.choice(LOCATIONS)
        team_size = _team_size_for_age(startup_age)

        startups.append({
            "id": str(uuid.uuid4()),
            "startup_name": name,
            "industry": industry,
            "location": location,
            "founded_year": founded_year,
            "team_size": team_size,
        })
    return startups


def generate_investors() -> list[dict[str, Any]]:
    """Create investor records from the predefined list."""
    investors = []
    for name in INVESTOR_NAMES:
        investors.append({
            "id": str(uuid.uuid4()),
            "investor_name": name,
            "investor_type": random.choice(INVESTOR_TYPES),
        })
    return investors


def generate_funding_rounds(
    startups: list[dict],
    investors: list[dict],
) -> tuple[list[dict], list[dict]]:
    """Generate funding rounds and investor-startup relationships."""
    funding_rounds = []
    startup_investors = []

    for startup in startups:
        # Each startup gets 1-4 funding rounds
        startup_age = 2026 - startup["founded_year"]
        max_rounds = min(len(FUNDING_ROUNDS), max(1, startup_age // 2))
        num_rounds = random.randint(1, max(1, max_rounds))

        for r_idx in range(num_rounds):
            round_name = FUNDING_ROUNDS[min(r_idx, len(FUNDING_ROUNDS) - 1)]
            amount = _funding_amount_for_round(round_name)
            investor_count = random.randint(1, min(8, r_idx + 3))

            # Assign random date spread across the startup's lifetime
            days_offset = random.randint(0, max(1, startup_age * 365))
            round_date = date(startup["founded_year"], 1, 1) + timedelta(days=min(days_offset, (2025 - startup["founded_year"]) * 365))

            fr_id = str(uuid.uuid4())
            funding_rounds.append({
                "id": fr_id,
                "startup_id": startup["id"],
                "funding_amount": amount,
                "funding_round": round_name,
                "investor_count": investor_count,
                "date": round_date.isoformat(),
            })

            # Link investors
            selected_investors = random.sample(investors, min(investor_count, len(investors)))
            for inv in selected_investors:
                startup_investors.append({
                    "id": str(uuid.uuid4()),
                    "startup_id": startup["id"],
                    "investor_id": inv["id"],
                    "funding_round_id": fr_id,
                })

    return funding_rounds, startup_investors


def build_training_dataframe(
    startups: list[dict],
    funding_rounds: list[dict],
) -> pd.DataFrame:
    """
    Build a flat DataFrame suitable for ML training.

    Each row = one startup with aggregated features + funding_success label.
    """
    # Aggregate funding info per startup
    fr_df = pd.DataFrame(funding_rounds)
    agg = fr_df.groupby("startup_id").agg(
        total_raised=("funding_amount", "sum"),
        num_rounds=("funding_round", "count"),
        max_investors=("investor_count", "max"),
    ).reset_index()

    df = pd.DataFrame(startups)
    df = df.merge(agg, left_on="id", right_on="startup_id", how="left")
    df["total_raised"] = df["total_raised"].fillna(0)
    df["num_rounds"] = df["num_rounds"].fillna(0).astype(int)
    df["max_investors"] = df["max_investors"].fillna(0).astype(int)

    # Rename to match model features
    df["startup_age"] = 2026 - df["founded_year"]
    df["investor_count"] = df["max_investors"]
    df["previous_funding_rounds"] = df["num_rounds"]

    # Generate target label
    df["funding_success"] = df.apply(
        lambda row: _determine_funding_success(
            row["industry"],
            row["team_size"],
            row["startup_age"],
            row["investor_count"],
            row["total_raised"],
        ),
        axis=1,
    )

    return df


def save_training_csv(df: pd.DataFrame, path: str = None) -> str:
    """Save the training DataFrame to CSV."""
    if path is None:
        path = os.path.join(
            os.path.dirname(__file__), "..", "models", "training_data.csv"
        )
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    logger.info("Training data saved to %s (%d rows)", path, len(df))
    return path


def upload_to_supabase(
    startups: list[dict],
    investors: list[dict],
    funding_rounds: list[dict],
    startup_investors: list[dict],
) -> None:
    """Upload generated data to Supabase tables."""
    from app.services.data_service import get_client

    client = get_client()
    batch_size = 50

    logger.info("Uploading %d startups …", len(startups))
    for i in range(0, len(startups), batch_size):
        client.table("startups").insert(startups[i : i + batch_size]).execute()

    logger.info("Uploading %d investors …", len(investors))
    for i in range(0, len(investors), batch_size):
        client.table("investors").insert(investors[i : i + batch_size]).execute()

    logger.info("Uploading %d funding rounds …", len(funding_rounds))
    for i in range(0, len(funding_rounds), batch_size):
        client.table("funding_rounds").insert(funding_rounds[i : i + batch_size]).execute()

    logger.info("Uploading %d startup-investor links …", len(startup_investors))
    for i in range(0, len(startup_investors), batch_size):
        client.table("startup_investors").insert(startup_investors[i : i + batch_size]).execute()

    logger.info("✅ All data uploaded to Supabase.")


# =============================================================================
# Main
# =============================================================================

def main():
    """Generate seed data, save CSV, and optionally upload to Supabase."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

    logger.info("🌱 Generating synthetic startup funding data …")

    startups = generate_startups()
    investors = generate_investors()
    funding_rounds, startup_investors = generate_funding_rounds(startups, investors)

    logger.info(
        "Generated: %d startups, %d investors, %d funding rounds, %d links",
        len(startups), len(investors), len(funding_rounds), len(startup_investors),
    )

    # Build training dataset
    training_df = build_training_dataframe(startups, funding_rounds)
    csv_path = save_training_csv(training_df)

    # Show class distribution
    dist = training_df["funding_success"].value_counts()
    logger.info("Target distribution:\n%s", dist.to_string())

    # Upload to Supabase if env vars are set
    supabase_url = os.getenv("SUPABASE_URL", "")
    if supabase_url and supabase_url != "https://your-project.supabase.co":
        logger.info("Supabase URL detected — uploading data …")
        upload_to_supabase(startups, investors, funding_rounds, startup_investors)
    else:
        logger.info(
            "⚠️  Supabase URL not configured. Skipping upload. "
            "Training CSV saved at: %s",
            csv_path,
        )


if __name__ == "__main__":
    main()
