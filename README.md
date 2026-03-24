# 🚀 Startup Funding Intelligence Platform

A state-of-the-art **MLOps-driven analytics engine** designed to decode the Indian startup ecosystem. This platform synthesizes historical Kaggle data with real-time news to provide predictive insights, growth momentum rankings, and deep-sector analytics.

![Dashboard Preview](https://img.shields.io/badge/UI-Glassmorphism-blueviolet?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/Frontend-React%2018-61DAFB?style=for-the-badge&logo=react)
![ML](https://img.shields.io/badge/ML-Prophet%20%7C%20XGBoost-ff69b4?style=for-the-badge)

---

## 🌟 Core Features

### 📊 **Predictive Analytics Dashboard**
*   **Time-Series Forecasting:** Leverages **Facebook Prophet** to model funding cycles and simulate a 5-year investment outlook.
*   **Historical Context:** Visual comparisons between capital infusion trends (2015–2025) and predictive growth.
*   **Success Metrics:** Automatic calculation of industry-specific success rates based on capital efficiency and funding velocity.

### 🔥 **Trending Startups & Live Discovery**
*   **Momentum Ranking Algorithm:** A sophisticated scoring engine that ranks startups based on:
    *   **Recent Activity (60%)**: Funding rounds in 2024–2025.
    *   **Growth Velocity (30%)**: Annualized capital raised vs. company age.
    *   **Stability (10%)**: Investor count and round depth.
*   **Live Scraping:** Integrated **Economic Times (ETtech)** deals extractor for real-time market updates.

### ⚙️ **Data Synthesis Engine**
*   **Multi-Source Merging:** Deduplicates and standardizes data from Kaggle (Static) and ET (Real-time).
*   **Smart Currency Normalization:** Converts "Cr" (Crores) and "Lakhs" into USD equivalents using dynamic exchange rates.
*   **Entity Sanitization:** Proactively cleans unescaped unicode and normalizes geographical hubs (e.g., *Bangalore* → *Bengaluru*).

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python 3.11, FastAPI, Pandas, Selenium, Beautiful Soup 4 |
| **Frontend** | React, Vite, Recharts, Framer Motion (Glassmorphism) |
| **Machine Learning** | Facebook Prophet, XGBoost, Scikit-Learn |
| **Ops & Tracking** | MLflow, GitHub Actions (CI/CD), Docker, Docker-compose |
| **Security** | API Key Gatekeeping, Rate Limiting (SlowAPI) |

---

## 🏗️ MLOps & CI/CD Pipeline

The project implements a robust transition from development to production:
*   **Automated Testing:** Pytest suite for API reliability and data integrity.
*   **Quality Gates:** Flake8 linting and type-checking integrated into GitHub Actions.
*   **Containerization:** Full Docker support for both services with multi-stage builds.
*   **Experiment Tracking:** MLflow integration for logging model parameters and performance metrics.

---

## 🚀 Quick Start

### 1. Requirements
*   **Python:** 3.11+
*   **Node.js:** 18+
*   **Docker:** (Optional, for containerized run)

### 2. Manual Setup

**Backend:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app/scraping/seed_data.py  # Seed the intelligence brain
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### 3. Docker One-Tap Launch
```bash
docker-compose up --build
```

---

## 📄 Documentation & API
Accessible at `http://localhost:8000/docs`.  
*Note: Ensure `x-api-key` is included in request headers for protected analytics routes.*

---
*Built with ❤️ for the Startup Ecosystem by Antigravity.*
