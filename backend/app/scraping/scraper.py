"""
Scraper — Collect startup funding data from web sources.

This module handles data extraction, cleaning, and normalization
before storing records in the Supabase database.
"""

import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def scrape_startup_data(url: str) -> list[dict]:
    """
    Scrape startup funding data from a given URL.

    Parameters
    ----------
    url : str
        The target URL to scrape.

    Returns
    -------
    list[dict]
        List of dicts with keys: startup_name, industry, location,
        founded_year, team_size, funding_amount, funding_round, investor_count.
    """
    results = []
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # -----------------------------------------------------------------
        # TODO: Phase 3 — implement source-specific parsing logic here.
        #   Each source will have unique HTML structure; create dedicated
        #   parser functions per source (e.g., parse_techcrunch, parse_crunchbase).
        # -----------------------------------------------------------------
        logger.info("Scraping %s — parser not yet implemented.", url)

    except requests.RequestException as e:
        logger.error("Scraping failed for %s: %s", url, e)

    return results


def clean_record(record: dict) -> dict:
    """Normalize and validate a scraped record before DB insertion."""
    cleaned = {}
    cleaned["startup_name"] = str(record.get("startup_name", "")).strip()
    cleaned["industry"] = str(record.get("industry", "")).strip().title()
    cleaned["location"] = str(record.get("location", "")).strip()
    cleaned["founded_year"] = int(record.get("founded_year", 0))
    cleaned["team_size"] = max(int(record.get("team_size", 0)), 0)
    cleaned["funding_amount"] = max(float(record.get("funding_amount", 0)), 0)
    cleaned["funding_round"] = str(record.get("funding_round", "")).strip()
    cleaned["investor_count"] = max(int(record.get("investor_count", 0)), 0)
    return cleaned
