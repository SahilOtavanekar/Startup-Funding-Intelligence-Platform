"""
Kaggle Data Processor — Investments VC Engagement
Transforms the raw investments_VC.csv into the structured training_data.csv 
required for the XGBoost model and the platform dashboard.
"""

import os
import logging
import pandas as pd
import numpy as np
from datetime import datetime

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "investments_VC.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "models", "training_data.csv")

def clean_currency(val):
    if pd.isna(val) or val == ' -   ':
        return 0.0
    try:
        # Remove commas and non-numeric chars except decimal
        cleaned = str(val).replace(',', '').replace('$', '').strip()
        return float(cleaned)
    except:
        return 0.0

def process_kaggle_data():
    logger.info(f"📂 Loading raw Kaggle dataset: {CSV_PATH}")
    
    try:
        # Use ISO-8859-1 for Kaggle CSV encoding
        df = pd.read_csv(CSV_PATH, encoding='ISO-8859-1')
    except Exception as e:
        logger.error(f"Failed to read CSV: {e}")
        return

    # 1. Clean Column Names (Kaggle has trailing spaces like ' market ')
    df.columns = df.columns.str.strip()
    logger.info(f"Columns identified: {df.columns.tolist()[:10]}...")

    # 2. Drop completely empty rows if any
    df = df.dropna(subset=['name', 'market'])

    # 3. Clean Numeric Columns
    df['total_raised'] = df['funding_total_usd'].apply(clean_currency)
    
    # 4. Filter for records with some data
    df = df[df['total_raised'] > 0].copy()

    # 5. Map Features
    current_year = 2024 # Dataset is historical
    
    # Handle founded_year
    df['founded_year'] = pd.to_numeric(df['founded_year'], errors='coerce')
    df['founded_year'] = df['founded_year'].fillna(df['founded_year'].median())
    df['startup_age'] = current_year - df['founded_year']
    df['startup_age'] = df['startup_age'].clip(lower=1)
    
    # Map status to binary success
    # 'operating', 'acquired', 'closed'
    df['funding_success'] = df['status'].apply(lambda x: 1 if str(x).lower().strip() in ['acquired', 'operating'] else 0)
    
    # Refine success: If raised > 5M, it's a success in this context
    df.loc[df['total_raised'] > 5000000, 'funding_success'] = 1

    # 6. Synthesize missing features using realistic correlations
    logger.info("🛠️ Synthesizing platform-required features (team_size, investor_count)...")
    
    # Team size estimation: $100k raised ~= 1.5 employees (capped)
    df['team_size'] = (df['total_raised'] / 80000).astype(int).clip(5, 5000)
    
    # Investor count: If missing, estimate based on funding rounds
    df['investor_count'] = df['funding_rounds'].fillna(1).astype(int) * 2
    
    # Previous funding rounds
    df['previous_funding_rounds'] = df['funding_rounds'].fillna(1).astype(int)

    # 7. Final selection & rename for the platform schema
    final_df = df[[
        'name', 
        'market', 
        'city', 
        'founded_year', 
        'startup_age', 
        'team_size', 
        'previous_funding_rounds', 
        'investor_count', 
        'total_raised', 
        'funding_success'
    ]].copy()

    final_df.columns = [
        'startup_name', 
        'industry', 
        'location', 
        'founded_year', 
        'startup_age', 
        'team_size', 
        'previous_funding_rounds', 
        'investor_count', 
        'total_raised', 
        'funding_success'
    ]

    # Handle missing locations
    final_df['location'] = final_df['location'].fillna('Global')
    final_df['industry'] = final_df['industry'].fillna('Other').str.strip().str.title()

    # 8. Save to models directory
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    final_df.to_csv(OUTPUT_PATH, index=False)
    
    logger.info(f"✅ Processed {len(final_df)} real-world records.")
    logger.info(f"💾 Training data saved to: {OUTPUT_PATH}")
    
    success_rate = (final_df['funding_success'].mean() * 100)
    logger.info(f"📊 Real-world Success Rate: {success_rate:.2f}%")

if __name__ == "__main__":
    process_kaggle_data()
