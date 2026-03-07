"""
Synthetic Data Generator — India Edition.
Generates realistic historical data for Indian startups to form the base
training dataset for the machine learning model.
"""

import os
import random
import csv
import logging
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

# Output path
OUTPUT_CSV = os.path.join(
    os.path.dirname(__file__), "..", "models", "training_data.csv"
)

# Indian dimensions
INDIAN_CITIES = [
    "Bengaluru", "Mumbai", "Gurugram", "Delhi", "Noida", 
    "Hyderabad", "Pune", "Chennai", "Ahmedabad"
]

INDIAN_INDUSTRIES = [
    "FinTech", "EdTech", "E-commerce", "HealthTech", "SaaS", 
    "AgriTech", "CleanTech", "Logistics", "Consumer Brands", "DeepTech"
]

# A list of realistic sounding or famous real Indian startups
INDIAN_STARTUPS_BASE = [
    "Flipkart", "Paytm", "BYJU'S", "Oyo", "Swiggy", "Zomato", "Ola", 
    "Razorpay", "Cred", "Lenskart", "Zerodha", "Dream11", "Unacademy", 
    "Udaan", "ShareChat", "Digit Insurance", "Pine Labs", "PhonePe", 
    "Groww", "Upstox", "Meesho", "Nykaa", "Urban Company", "Delhivery", 
    "FirstCry", "PharmEasy", "Vedantu", "Licious", "Spinny", "Cars24",
    "Pristyn Care", "MobiKwik", "BharatPe", "InMobi", "Glance", "DailyHunt",
    "Cure.fit", "KreditBee", "Acko", "Rupeek", "Zeta", "Chargebee", "Postman",
    "BrowserStack", "Freshworks", "Zoho"
]

def generate_indian_historical_data(n_records: int = 600) -> list[dict]:
    """Generate realistic Indian startup funding history."""
    records = []
    
    current_year = datetime.now().year
    
    # First, guarantee the famous ones
    for name in INDIAN_STARTUPS_BASE:
        industry = random.choice(["FinTech", "E-commerce", "EdTech", "SaaS"])
        location = random.choice(["Bengaluru", "Mumbai", "Gurugram"])
        founded_year = random.randint(2008, 2018)
        age = current_year - founded_year
        team_size = random.randint(500, 5000)
        rounds = random.randint(4, 8)
        investors = random.randint(5, 20)
        # Big unicorns -> hundreds of millions or billions in total raised
        total_raised = random.randint(100_000_000, 2_000_000_000) 
        
        status = 1  # 100% funded
        
        records.append({
            "startup_name": name,
            "industry": industry,
            "location": location,
            "founded_year": founded_year,
            "startup_age": age,
            "team_size": team_size,
            "previous_funding_rounds": rounds,
            "investor_count": investors,
            "total_raised": total_raised,
            "funding_success": status
        })

    # Fill the rest with synthetic early/mid stage Indian startups
    remaining = n_records - len(records)
    for i in range(remaining):
        industry = random.choice(INDIAN_INDUSTRIES)
        location = random.choices(
            INDIAN_CITIES, 
            weights=[35, 25, 15, 5, 5, 5, 5, 3, 2], k=1
        )[0]
        
        founded_year = random.randint(2015, current_year - 1)
        age = current_year - founded_year
        
        # Determine success logic (approx 35% success rate for general startups)
        success_prob = 0.1
        if age > 2: success_prob += 0.1
        if industry in ["FinTech", "SaaS", "E-commerce"]: success_prob += 0.1
        if location in ["Bengaluru", "Gurugram"]: success_prob += 0.1
        
        success = 1 if random.random() < success_prob else 0
        
        if success:
            team_size = random.randint(10, 250)
            rounds = random.randint(1, 4)
            investors = random.randint(1, 10)
            total_raised = random.randint(500_000, 50_000_000)
        else:
            team_size = random.randint(2, 20)
            rounds = random.randint(0, 1)
            investors = random.randint(0, 2)
            total_raised = random.randint(0, 200_000)
            
        name = f"{random.choice(['Bharat', 'Indic', 'Smart', 'Insta', 'Quick', 'NextGen', 'Desi'])}{random.choice(['Tech', 'Pay', 'Kart', 'Edu', 'Health', 'Farm'])} {i}"
        
        records.append({
            "startup_name": name,
            "industry": industry,
            "location": location,
            "founded_year": founded_year,
            "startup_age": age,
            "team_size": team_size,
            "previous_funding_rounds": rounds,
            "investor_count": investors,
            "total_raised": total_raised,
            "funding_success": success
        })
        
    return records

def save_to_csv(records: list[dict], path: str):
    if not records:
        return
    keys = records[0].keys()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)
    logger.info(f"💾 Saved {len(records)} records to {path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("🌱 Generating Indian Startup Ecosystem dataset...")
    data = generate_indian_historical_data(n_records=1000)
    save_to_csv(data, OUTPUT_CSV)
    
    # Display snapshot
    df = pd.DataFrame(data)
    logger.info("\nCity Distribution:")
    logger.info(df['location'].value_counts())
    logger.info("Done.")
