import json
import os
import pandas as pd
import re

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "training_data.csv")
JSON_PATH_TALKY = os.path.join(os.path.dirname(__file__), "..", "models", "scraped_data_2025.json")
JSON_PATH_ET = os.path.join(os.path.dirname(__file__), "..", "models", "scraped_data_et.json")

def parse_amount(amount_str):
    """Converts diverse currency strings like '$25 million' or 'Rs 110 crore' into float USD."""
    if not amount_str or "undisclosed" in amount_str.lower():
        return 0.0
    
    # Try to extract USD amount from strings like 'Rs 110 crore ($13 million)'
    usd_match = re.search(r'\$(\d+\.?\d*)\s*(million|M|B|billion|K)', amount_str, re.IGNORECASE)
    if usd_match:
        val = float(usd_match.group(1))
        scale = usd_match.group(2).lower()
        if scale in ['m', 'million']:
            return val * 1_000_000
        elif scale in ['b', 'billion']:
            return val * 1_000_000_000
        elif scale in ['k']:
            return val * 1_000
        return val

    # Try raw dollar amounts like '$25,000,000' or '$635,000'
    raw_usd = re.search(r'\$(\d+[,.\d]*)', amount_str)
    if raw_usd:
        return float(raw_usd.group(1).replace(',', ''))

    # If only Rs (Rupees) exists, convert INR to USD (Approx rate: 1 USD = 83 INR)
    inr_match = re.search(r'(?:Rs|INR)\s*(\d+\.?\d*)\s*(crore)', amount_str, re.IGNORECASE)
    if inr_match:
        val = float(inr_match.group(1))
        # 1 Crore = 10,000,000 INR
        inr_total = val * 10_000_000
        return inr_total / 83.0 # convert to USD
    
    return 0.0

def merge_file(df, json_path):
    if not os.path.exists(json_path):
        return df

    with open(json_path, 'r') as f:
        scraped_data = json.load(f)

    print(f"🔄 Merging {len(scraped_data)} records from {os.path.basename(json_path)}...")

    for item in scraped_data:
        # Pre-clean the startup name (handling unicode)
        name = item['startup_name'].encode('ascii', 'ignore').decode('ascii').strip()
        amount = parse_amount(item.get('amount', '0'))
        
        # Search for existing startup by name (case-insensitive)
        mask = df['startup_name'].str.lower() == name.lower()
        
        if mask.any():
            # Update existing record
            idx = df[mask].index[0]
            df.at[idx, 'total_raised'] += amount
            df.at[idx, 'previous_funding_rounds'] += 1
            if df.at[idx, 'total_raised'] > 1_000_000:
                df.at[idx, 'funding_success'] = 1
        else:
            # Add as new startup
            new_row = {
                "startup_name": name,
                "industry": item.get("sector") or item.get("industry") or "Other",
                "location": item.get("location", "Unknown"),
                "founded_year": 2025,
                "team_size": 150, # Default estimate for funded companies
                "startup_age": 1,
                "investor_count": 1,
                "total_raised": amount,
                "previous_funding_rounds": 1,
                "funding_success": 1 if amount > 1_000_000 else 0
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df

def main():
    if not os.path.exists(CSV_PATH):
        print("❌ CSV not found.")
        return

    df = pd.read_csv(CSV_PATH)
    
    # Merge both sources
    df = merge_file(df, JSON_PATH_TALKY)
    df = merge_file(df, JSON_PATH_ET)

    df.to_csv(CSV_PATH, index=False)
    print(f"🚀 Database Synchronized. Total Rows: {len(df)}")

if __name__ == "__main__":
    main()
