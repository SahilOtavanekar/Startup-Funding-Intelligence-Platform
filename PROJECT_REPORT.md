# Startup Funding Intelligence Platform
## Comprehensive Project Documentation

### 1. Executive Summary
The **Startup Funding Intelligence Platform** is a data-driven ecosystem designed to help investors and entrepreneurs analyze the startup landscape. By combining historical funding data from Kaggle, real-time news scraping (TechCrunch, Inc42), and a calibrated XGBoost machine learning model, the platform provides actionable insights into funding trends and predicts the success probability of early-stage ventures.

---

### 2. Core Architecture & Tech Stack
The project follows a modern, modular microservices-inspired architecture:

*   **Frontend**: React (Vite) + Vanilla CSS (Glassmorphism UI)
    *   Responsive dashboard with Chart.js integration.
    *   State-driven prediction forms and dynamic data tables.
*   **Backend**: FastAPI (Python)
    *   High-performance asynchronous API.
    *   SlowAPI for rate limiting (Security).
    *   API Key authentication for protected routes.
*   **Database**: Supabase (PostgreSQL)
    *   Managed cloud database for persistence.
    *   Relational mapping between Startups and Funding Rounds.
*   **Machine Learning**: XGBoost + Scikit-Learn
    *   **Model**: Calibrated XGBoost Classifier (Platt Scaling).
    *   **Tracking**: MLflow for experiment management.
    *   **Tools**: Joblib for serialization, Pandas for ETL.
*   **Scraping**: BeautifulSoup4 + Selenium
    *   RSS feed parser for industrial news.
    *   Automated seeding scripts for initial data population.

---

### 3. Data Lifecycle & Infrastructure

#### A. Data Sourcing
1.  **Historical Base**: 3000+ records of Indian startups sourced from Kaggle.
2.  **Live Updates**: Automated scraping of news headlines to maintain market context.

#### B. Storage & Access
*   **Storage**: Primary data resides in **Supabase PostgreSQL**.
*   **Local Cache**: `training_data.csv` is maintained for rapid ML model re-training.
*   **Access**: The backend uses the `postgrest` protocol via the Supabase Python SDK to perform relational joins and filters.

#### C. Connections
*   **React $\leftrightarrow$ FastAPI**: Secured via `x-api-key` header and CORS policy (Port 3001 $\rightarrow$ 8000).
*   **FastAPI $\leftrightarrow$ Supabase**: Authenticated via JWT Service Keys.
*   **FastAPI $\leftrightarrow$ MLflow**: Logs metrics and parameters to a local SQLite-backed MLflow server.

---

### 4. Key Functional Modules

| Module | Description |
| :--- | :--- |
| **Prediction Engine** | Uses 6 key features (Industry, Location, Team Size, Age, Investors, Prev Rounds) to calculate a calibrated success probability. |
| **Analytics Dashboard** | Visualizes funding distribution by industry, success rates, and year-over-year growth. |
| **Startup Directory** | A searchable, filtered database showing real-world company metrics and institutional funding status. |
| **Data Sync Service** | Automates the migration of local CSV training data into the live PostgreSQL database. |

---

### 5. Project Quality & USPs
*   **Probability Calibration**: Unlike standard classifiers, our model uses Platt Scaling to ensure the "percentage" output is mathematically reliable.
*   **Premium Aesthetics**: A custom Glassmorphism UI design that feels like a modern FinTech product.
*   **Modular Code**: Strict separation of concerns between services, routes, and models.
*   **Production Readiness**: Includes rate limiting, API security, and standardized environment configuration via `.env`.

---

### 6. Use Cases
*   **Venture Capitalists**: Preliminary screening of startup cohorts based on historical success patterns.
*   **Founders**: Benchmarking their startup's vital stats (team size, age) against successful industry peers.
*   **Market Analysts**: Tracking the shift in funding focus (e.g., E-Tech vs Fintech) across different Indian hubs like Bangalore and Mumbai.

---

### 7. Future Enhancements
*   **User Authentication**: Implementing Clerk or Supabase Auth for personalized watchlists.
*   **Deep News Sentiment**: Using LLMs (Gemini/OpenAI) to perform sentiment analysis on scraped news.
*   **Feature Expansion**: Incorporating founder's educational background and patent data into the ML model.
*   **Auto-Deployment**: Dockerizing the stack for AWS/Azure deployment.

---

**Version**: 1.0.0  
**Status**: Fully Functional & Verified  
**Author**: Developed with Antigravity AI  
