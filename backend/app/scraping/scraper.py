"""
Scraper — Collect real-time startup funding data from Inc42.

This module extracts live announcements of Indian startup fundings, using regex
to parse names, amounts, and rounds from recent news headlines.
"""

import logging
import re
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

logger = logging.getLogger(__name__)

# Real-Time Indian Startup Funding Feed
INC42_RSS_URL = "https://inc42.com/feed/"

# Common Regex to extract funding amounts from Indian headlines
AMOUNT_PATTERN = re.compile(r'(?:Rs|₹|\$)\s*([\d\.]+)[\s-]*(Mn|Million|Cr|Billion)', re.IGNORECASE)
ROUND_PATTERN = re.compile(r'(Series [A-Z]|Seed|Pre-[S|s]eed|Angel|Venture|Debt)', re.IGNORECASE)

def _convert_amount(amount_str, multiplier_str):
    """Convert amount strings to raw $ USD approximate values."""
    val = float(amount_str)
    multiplier_str = multiplier_str.upper()
    
    # Very rough INR to USD conversion for 'Cr' (crore): 1 Cr INR ~= $120,000 USD
    if 'CR' in multiplier_str:
        return val * 120_000
    
    # Millions
    if 'M' in multiplier_str or 'ILLION' in multiplier_str:
        return val * 1_000_000
        
    # Billions
    if 'B' in multiplier_str:
        return val * 1_000_000_000
        
    return val

def scrape_live_fundings() -> list[dict]:
    """
    Scrape the latest Inc42 RSS feed and extract Indian funding rounds.
    """
    results = []
    try:
        # Use headers because some Indian sites block weird user agents
        response = requests.get(INC42_RSS_URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        response.raise_for_status()
        
        root = ET.fromstring(response.text)
        
        for item in root.findall('.//item'):
            title = item.find('title').text
            
            if not title:
                continue
                
            headline = title.strip()
            # Only care about funding events
            if 'raise' not in headline.lower() and 'secures' not in headline.lower() and 'funding' not in headline.lower() and 'infusion' not in headline.lower():
                continue
                
            amount_match = AMOUNT_PATTERN.search(headline)
            funding_amount = 0
            if amount_match:
                funding_amount = _convert_amount(amount_match.group(1), amount_match.group(2))
                
            round_match = ROUND_PATTERN.search(headline)
            funding_round = round_match.group(1).title() if round_match else "Undisclosed"
            
            # Extract startup name - usually before keywords
            # E.g. "StartupName Raises $5 Mn" -> "StartupName"
            # Or "Exclusive: Streetwear Brand Bonkers Corner To Raise..." -> "Bonkers Corner"
            startup_name = headline
            if 'Raises' in headline:
                startup_name = headline.split('Raises')[0]
            elif 'To Raise' in headline:
                startup_name = headline.split('To Raise')[0]
            elif 'Secures' in headline:
                startup_name = headline.split('Secures')[0]
                
            # Clean up introductory fluff
            startup_name = startup_name.replace('Exclusive:', '').strip()
            
            # Ignore aggregate news headers (e.g. "From Rozana To Cent — Indian Startups Raised $98 Mn")
            if 'Startups Raised' in startup_name or len(startup_name) > 40:
                continue

            # VALIDATION LAYER
            # 1. Require an actual numeric funding amount (discard vague PR like "secures fresh capital")
            if funding_amount <= 0:
                logger.warning(f"Discarding record (No Amount): {headline}")
                continue
                
            # 2. Require a clean, short startup name (discard failing regex phrases)
            if len(startup_name) > 30 or " " * 4 in startup_name:
                logger.warning(f"Discarding record (Messy Name): {startup_name}")
                continue
                
            # 3. Discard likely aggregate articles containing 'startups' (plural)
            if 'startups' in startup_name.lower() or 'companies' in startup_name.lower():
                logger.warning(f"Discarding record (Aggregate News): {headline}")
                continue

            # Passed Validation
            results.append({
                "startup_name": startup_name,
                "industry": "Technology", # Base assumption
                "location": "Bengaluru",  # Base assumption
                "founded_year": datetime.now().year - 2,
                "startup_age": 2,         # Derived age
                "team_size": 45, 
                "total_raised": funding_amount,
                "previous_funding_rounds": 1 if 'Seed' in funding_round else 3,
                "investor_count": 2,
                "funding_success": 1,
            })

        logger.info("Successfully extracted %d live Indian funding events.", len(results))

    except Exception as e:
        logger.error("Live scraping failed: %s", e)

    return results

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data = scrape_live_fundings()
    
    if data:
        import os
        import csv
        CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "training_data.csv")
        file_exists = os.path.isfile(CSV_PATH)
        
        with open(CSV_PATH, "a" if file_exists else "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            if not file_exists:
                writer.writeheader()
            writer.writerows(data)
            
        logger.info("Successfully appended %d live Indian records to training_data.csv!", len(data))
    else:
        logger.info("No live fundings to append.")
