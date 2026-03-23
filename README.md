# 🚀 Startup Funding Intelligence Platform

A high-performance, **ML-powered analytics platform** for uncovering insights into the Indian startup ecosystem. This project transforms historical Kaggle funding data into a live, interactive dashboard with predictive forecasting and growth momentum analysis.

---

## 🌟 Core Features

### 📊 **Interactive Insights Dashboard**
*   **Funding Trends:** Historical analysis of capital infusion from 2015 to 2025.
*   **Industry Benchmarks:** Success rate and total funding raised by sector (Fintech, E-Commerce, etc.).
*   **Geo-Hub Analysis:** Geographic distribution of startups across India's top hubs (Bengaluru, Mumbai, NCR).
*   **Round Distribution:** Breakdown of the ecosystem from Pre-Seed to Late Stage.

### 🔮 **ML-Powered Market Forecasting**
*   **Prophet Integration:** Uses the **Facebook Prophet** model to analyze historical funding waves and generate a 5-year predictive market forecast.
*   **Smooth Connection:** Visual transition between historical data (Cyan) and predictive simulation (Gold).

### 🔥 **Trending Startups & Live ETtech Momentum**
*   **Weighted Momentum Algorithm:** Ranks startups using a scientifically weighted formula:
    *   **60% Weight:** Recent Funding Activity (2024–2025 rounds).
    *   **30% Weight:** Annualized Growth Rate (Total Capital ÷ Age).
    *   **10% Weight:** Institutional Backing & Round Count.
*   **Live Data Scraping:** Includes a headless extraction engine for the **Economic Times (ETtech) Deals Digest**, merging the latest 2025/2026 funding news directly into the platform's analytical brain.

### 🔎 **Global Startup Database**
*   **Full-Text Search:** Search through all **3,097 preprocessed startup records** instantly.
*   **Deep Filtering:** Filter the entire dataset by industry, age, or location with server-side performance.

---

## 🛠️ Technology Stack

*   **Backend:** Python 3.11, FastAPI, Pandas, Prophet (ML), Headless Scraping.
*   **Frontend:** React, Vite, Recharts, Vanilla CSS (Glassmorphism).
*   **Data Source:** Hybrid (Kaggle Historical + Economic Times Live Deals).

---

## 🧪 Data Pipeline & Preprocessing

The project features an advanced multi-source data merging engine (`merge_scraped_data.py`) that:
*   **Synthesizes Sources:** Deduplicates 3,000+ historical Kaggle records with real-time news from ET Startups.
*   **Intelligent Currency Parsing:** Automatically converts "Cr" (Crores) and "Lakhs" to USD equivalents using the latest exchange rates.
*   **Entity Normalization:** Standardizes locations (e.g., *Bangalore* → *Bengaluru*) and industry classifications to ensure statistical integrity.


---

## 🚀 Getting Started

### 1. Prerequisites
*   Python 3.11+
*   Node.js 18+

### 2. Backend Setup
```bash
cd backend
# 1. Create and activate a virtual environment
python -m venv venv
./venv/Scripts/activate 

# 2. Install dependencies
pip install -r requirements.txt

# 3. Build & Preprocess the dataset
python app/scraping/seed_data.py

# 4. Start the API server
uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 📄 API Security & Documentation
*   **Protected Routes:** All analytics routes are gated with custom headers (`x-api-key`).
*   **Auto-Docs:** Explore the full API schema at `http://localhost:8000/docs`.

---

*Built for Data Science enthusiasts and Startup Founders.*
