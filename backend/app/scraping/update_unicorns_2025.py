import pandas as pd
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "training_data.csv")

# Real-world scraped data for 2025/2026
UNICORNS = [
    {
        "startup_name": "Zepto",
        "industry": "Ecommerce",
        "location": "Mumbai",
        "founded_year": 2021,
        "team_size": 2500,
        "startup_age": 4,
        "investor_count": 14,
        "total_raised": 2_930_000_000,
        "previous_funding_rounds": 9,
        "funding_success": 1
    },
    {
        "startup_name": "Razorpay",
        "industry": "Fintech",
        "location": "Bengaluru",
        "founded_year": 2014,
        "team_size": 3000,
        "startup_age": 11,
        "investor_count": 29,
        "total_raised": 816_000_000,
        "previous_funding_rounds": 8,
        "funding_success": 1
    },
    {
        "startup_name": "Groww",
        "industry": "Fintech",
        "location": "Bengaluru",
        "founded_year": 2016,
        "team_size": 1200,
        "startup_age": 9,
        "investor_count": 12,
        "total_raised": 596_000_000,
        "previous_funding_rounds": 6,
        "funding_success": 1
    },
    {
        "startup_name": "Porter",
        "industry": "Logistics",
        "location": "Bengaluru",
        "founded_year": 2014,
        "team_size": 1500,
        "startup_age": 11,
        "investor_count": 18,
        "total_raised": 356_500_000,
        "previous_funding_rounds": 7,
        "funding_success": 1
    }
]

def update_unicorns():
    if not os.path.exists(CSV_PATH):
        print("❌ CSV not found.")
        return

    df = pd.read_csv(CSV_PATH)
    print(f"🔄 Updating high-momentum unicorns in {len(df)} records...")

    for unicorn in UNICORNS:
        name = unicorn['startup_name']
        # Remove any existing (incorrect) records for these startups
        df = df[df['startup_name'].str.lower() != name.lower()]
        
        # Add the correct, high-value record
        df = pd.concat([df, pd.DataFrame([unicorn])], ignore_index=True)
        print(f"✅ Synced {name}: ${unicorn['total_raised']/1e6:.1f}M (Recent Momentum)")

    df.to_csv(CSV_PATH, index=False)
    print(f"🚀 Database Synchronized. Total Rows: {len(df)}")

if __name__ == "__main__":
    update_unicorns()
