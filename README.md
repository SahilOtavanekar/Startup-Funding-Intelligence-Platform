# Startup Funding Intelligence Platform

An AI-powered web application that analyzes startup data, explores industry trends, and uses an **XGBoost** machine learning model to predict the probability of a startup securing funding.

## Features

- 🔮 **Funding Predictor:** Input startup parameters (industry, team size, age, investor count) to get a live prediction of funding success. Includes feature importance to explain exactly *why* the model made its prediction.
- 📈 **Industry Intelligence:** Interactive charts built with *Recharts* displaying funding distributions, success rates, location popularity, and timeline trends.
- 🏢 **Startup Database:** A searchable, sortable database of startup records.
- 🧪 **MLflow Tracking:** Integrated experiment tracking for reproducible machine learning model training.
- 🎨 **Glassmorphism UI:** A sleek, modern dark-themed interface built from scratch using vanilla CSS variables and utility classes.

## Tech Stack

- **Frontend:** React (Vite), React Router, Recharts, Axios
- **Backend:** FastAPI, Python, Uvicorn
- **Machine Learning:** XGBoost, Scikit-learn, Pandas, MLflow
- **Database:** Supabase (PostgreSQL) - *Live data integration ready*
- **Containerization:** Docker & Docker Compose

## Quick Start (Local Setup)

### 1. Clone & Environment
Copy the example environment file and update it with your Supabase credentials (optional for testing, as local mock data is generated).
```bash
cp .env.example .env
```

### 2. Startup Database & ML Model
Generate synthetic data and train the model.
```bash
cd backend
pip install -r requirements.txt

# Generate 500+ records of realistic startup data
python -m app.scraping.seed_data

# Train the XGBoost model 
python -m app.models.train_model
```

### 3. Run FastAPI Backend
```bash
cd backend
uvicorn app.main:app --reload
```
The API documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

### 4. Run React Frontend
In a new terminal:
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

## Docker Deployment (Optional)

You can spin up the entire stack, including the MLflow tracking server, using Docker Compose:

```bash
docker-compose up --build
```
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **MLflow Tracking:** http://localhost:5000

## Project Structure

```text
├── backend/                  # FastAPI + ML codebase
│   ├── app/
│   │   ├── models/           # train_model.py, model.pkl
│   │   ├── routes/           # API endpoints (prediction, analytics)
│   │   ├── scraping/         # Data generators & scraper logic
│   │   ├── services/         # Model logic & Supabase queries
│   │   └── utils/            # Feature engineering pipeline
│   ├── migrations/           # Supabase SQL schema definitions
│   └── requirements.txt
├── frontend/                 # React application
│   ├── public/
│   └── src/
│       ├── components/       # Reusable UI (Dashboard, Charts, PredictionForm)
│       ├── pages/            # View views (Home, Insights, Predict, Startups)
│       ├── services/         # Axios API & Supabase Client
│       └── index.css         # Glassmorphism Design System
├── docker-compose.yml        # Multi-container orchestration
└── ...
```

## Future Enhancements
- Connect the active web Scraper (`scraper.py`) to live sources like Crunchbase or YCombinator.
- Add user authentication via Supabase Auth to track user-saved predictions.
- Migrate from SQLite to an external PostgreSQL database for MLflow tracking.
