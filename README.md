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

### 🔥 **Trending Startups Leaderboard**
*   **Growth Velocity Algorithm:** Ranks startups not just by "total raised," but by **Operational Momentum** (Capital Raised ÷ Company Age).
*   **Momentum Score:** A proprietary 1–99 score based on funding velocity and investor backing.

### 🔎 **Global Startup Database**
*   **Full-Text Search:** Search through all **3,044 preprocessed startup records** instantly.
*   **Deep Filtering:** Filter the entire dataset by industry, age, or location with server-side performance.

---

## 🛠️ Technology Stack

*   **Backend:** Python 3.11, FastAPI, Pandas, Prophet (ML).
*   **Frontend:** React, Vite, Recharts, Vanilla CSS (Glassmorphism).
*   **Data Source:** Real Kaggle mirror of the **Indian Startup Funding** dataset.

---

## 🧪 Data Pipeline & Preprocessing

The project features a standalone data cleaning engine (`seed_data.py`) that transforms raw funding logs into a research-ready database:
*   **Imputation:** Mathematically infers missing company ages and team sizes based on capital ratios.
*   **Normalization:** Merges historical naming conflicts (e.g., *Bangalore* → *Bengaluru*) to ensure statistical accuracy.
*   **Classification:** Maps over 800+ raw industry verticals into clean, manageable categories.

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
