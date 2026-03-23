import pandas as pd
import os
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def _clean_text(text):
    """Clean un-escaped unicode/special characters and normalize city names."""
    if not isinstance(text, str):
        return str(text)
    text = text.encode('ascii', 'ignore').decode('ascii').strip()
    if text.lower() == "bangalore":
        return "Bengaluru"
    return text

def _load_data() -> pd.DataFrame:
    """Load and clean the local training CSV."""
    df = pd.read_csv(CSV_PATH)
    if 'industry' in df.columns:
        df['industry'] = df['industry'].apply(_clean_text)
    if 'location' in df.columns:
        df['location'] = df['location'].apply(_clean_text)
    if 'startup_name' in df.columns:
        df['startup_name'] = df['startup_name'].apply(_clean_text)
    return df

# Path to the processed training data
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models", "training_data.csv")

def get_available_industries() -> List[str]:
    """Return a sorted list of all unique industries in the dataset."""
    df = _load_data()
    # Return top 150 industries by frequency to avoid massive lists, or just drop very rare ones
    counts = df['industry'].value_counts()
    # Let's return industries that have at least 10 records for meaningful insights
    valid_industries = counts[counts >= 10].index.tolist()
    return sorted(valid_industries)

def get_available_locations() -> List[str]:
    """Return a sorted list of top locations."""
    df = _load_data()
    counts = df['location'].value_counts()
    valid_locations = counts[counts >= 10].index.tolist()
    # Remove 'Global' if we only want specific cities/countries, or keep it
    return sorted(valid_locations)

def get_industry_roadmap(industry: str) -> Dict[str, Any]:
    """Extract success blueprint and benchmarks for a specific industry."""
    df = _load_data()
    
    # Filter by industry
    industry_df = df[df['industry'].str.lower() == industry.lower()]
    
    if len(industry_df) == 0:
        return {"error": f"No records found for industry: {industry}"}
        
    # Get only successful companies within this industry
    successful_df = industry_df[industry_df['funding_success'] == 1]
    
    # If no successful companies, fallback to overall industry averages
    analysis_df = successful_df if len(successful_df) > 0 else industry_df
        
    # 1. Typical Roadmap (Medians of successful companies)
    avg_team_size = int(analysis_df['team_size'].median())
    avg_age = max(1, int(analysis_df['startup_age'].median()))
    avg_funding = float(analysis_df['total_raised'].median())
    
    # Format funding to readable string
    if avg_funding >= 1_000_000:
        funding_str = f"${avg_funding / 1_000_000:.1f}M"
    elif avg_funding >= 1_000:
        funding_str = f"${avg_funding / 1_000:.0f}K"
    else:
        funding_str = f"${avg_funding:,.0f}"

    # 2. Top Investor Hubs (Locations with most successful funding)
    # Exclude global or missing locations from top hubs if possible
    valid_locations = analysis_df[analysis_df['location'] != 'Global']
    if len(valid_locations) == 0:
        valid_locations = analysis_df

    top_locations = valid_locations['location'].value_counts().head(3).index.tolist()

    # 3. Market Sentiment
    total_startups = len(industry_df)
    success_rate = round(len(successful_df) / total_startups * 100, 1) if total_startups > 0 else 0
    
    if success_rate >= 90:
        sentiment = "Highly Favorable (Strong VC Interest)"
    elif success_rate >= 50:
        sentiment = "Favorable (Stable Sector)"
    else:
        sentiment = "Competitive (High Barrier to Entry)"
        
    return {
        "industry": industry_df.iloc[0]['industry'],  # use proper case
        "total_startups_analyzed": total_startups,
        "success_rate": success_rate,
        "sentiment": sentiment,
        "blueprint": {
            "target_funding": funding_str,
            "target_team_size": avg_team_size,
            "target_age_years": avg_age,
        },
        "top_hubs": top_locations
    }

def get_top_growing_startups(industry: str = None, location: str = None, limit: int = 15) -> List[Dict[str, Any]]:
    """Returns top startups based on funding velocity and recent activity."""
    df = _load_data()
    
    # Filter valid rows
    df = df[df['startup_name'].notna() & (df['total_raised'] > 0)]
    
    if industry and industry != 'All':
        df = df[df['industry'].str.lower() == industry.lower()]
        
    if location and location != 'All':
        df = df[df['location'].str.lower() == location.lower()]
    
    # Focus on relatively young startups (<= 10 years old) to find "growing" potential
    young_df = df[df['startup_age'] <= 10].copy()
    
    if len(young_df) == 0:
        young_df = df.copy() # fallback if no young startups
        
    # Growth Score: Funding Velocity (total raised per year of existence)
    young_df['funding_velocity'] = young_df['total_raised'] / young_df['startup_age'].clip(lower=1)
    
    # Sort by funding velocity descending
    top_df = young_df.sort_values(by=['funding_velocity', 'investor_count'], ascending=[False, False]).head(limit)
    
    results = []
    for _, row in top_df.iterrows():
        funding = row['total_raised']
        if funding >= 1_000_000_000:
            funding_str = f"${funding / 1_000_000_000:.1f}B"
        elif funding >= 1_000_000:
            funding_str = f"${funding / 1_000_000:.1f}M"
        else:
            funding_str = f"${funding / 1_000:.0f}K"
            
        # Create a visual momentum score 1-100
        base_score = min(99, int((row['funding_velocity'] / 1_000_000) * 2 + (row['investor_count'] * 3)))
        momentum = max(50, base_score) # floor at 50 for top list
        
        results.append({
            "startup_name": row['startup_name'],
            "industry": row['industry'],
            "location": row['location'],
            "startup_age": int(row['startup_age']),
            "team_size": int(row['team_size']),
            "total_raised": funding_str,
            "investor_count": int(row['investor_count']),
            "momentum_score": momentum
        })
        
    return results
