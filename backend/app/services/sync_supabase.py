"""
Push Local Kaggle Dataset to Remote Supabase.
Requires supabase pip package and Environment Variables configured.
"""
import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client
import math

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")  # We are using anon key which we temporarily gave INSERT powers to

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Missing Supabase credentials.")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
csv_path = os.path.join(os.path.dirname(__file__), "..", "models", "training_data.csv")

def run_sync():
    """Populate Supabase with Kaggle Dataset records."""
    df = pd.read_csv(csv_path)
    
    # We only want to push around 300 rows to avoid blowing up tiny instances, but we can do them all. Let's do 350 to provide a solid analytical baseline.
    sample_df = df.head(350).copy()
    
    print(f"Syncing {len(sample_df)} real Kaggle records directly into Postgres...")

    for index, row in sample_df.iterrows():
        try:
            # 1. Insert Startup
            startup_data = {
                "startup_name": str(row["startup_name"]),
                "industry": str(row["industry"]),
                "location": str(row["location"]),
                "founded_year": int(row["founded_year"]) if not pd.isna(row["founded_year"]) else 2018,
                "team_size": int(row["team_size"]) if not pd.isna(row["team_size"]) else 10
            }
            
            # Since anon has INSERT, it can write.
            # Upsert or Insert
            result = supabase.table("startups").insert(startup_data).execute()
            startup_id = result.data[0]['id']
            
            # 2. Insert Funding Round
            if float(row["total_raised"]) > 0:
                round_data = {
                    "startup_id": startup_id,
                    "funding_amount": float(row["total_raised"]),
                    "funding_round": "Growth/Institutional" if int(row["funding_success"]) == 1 else "Seed/Early",
                    "investor_count": int(row["investor_count"]) if not pd.isna(row["investor_count"]) else 0,
                }
                supabase.table("funding_rounds").insert(round_data).execute()
                
            if index % 50 == 0 and index != 0:
                print(f"Synced {index} records...")
                
        except Exception as e:
            print(f"Failed on row {index}: {e}")

    print("✅ Supabase Sync Complete!")

if __name__ == "__main__":
    run_sync()
