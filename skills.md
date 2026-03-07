# Antigravity Agent Skills Configuration

## For Startup Funding Intelligence Platform

This document defines the **skills and operational behaviors** the Antigravity agent should follow to optimize the development workflow of the Startup Funding Intelligence Platform.

The agent should operate as a **full-stack AI engineering assistant** capable of managing backend, frontend, data engineering, and machine learning tasks while maintaining clean architecture and production-quality code.

---

# 1. Core Agent Responsibilities

The Antigravity agent should be able to:

* Plan and generate full-stack project structure
* Maintain modular code architecture
* Implement backend APIs
* Implement machine learning pipelines
* Integrate databases
* Develop frontend dashboards
* Ensure the application runs correctly
* Debug runtime errors
* Maintain code readability and documentation

The agent must prioritize **maintainability, modularity, and scalability**.

---

# 2. Backend Development Skills

The agent must be capable of designing and maintaining backend services using Python.

### Required Backend Capabilities

* Build REST APIs using FastAPI
* Implement modular API routing
* Implement service layers for business logic
* Connect backend services to Supabase PostgreSQL
* Handle API validation and error handling
* Implement asynchronous request handling where appropriate

### Backend Code Organization

The backend should follow this layered structure:

Controllers
Routes that define API endpoints.

Services
Business logic and data operations.

Models
Machine learning training and inference code.

Utilities
Reusable helper functions.

---

# 3. Database Integration Skills

The agent must manage database interactions with Supabase.

Capabilities include:

* Creating and modifying database schema
* Writing efficient SQL queries
* Implementing database CRUD operations
* Managing relationships between tables
* Connecting backend services to Supabase

Tables expected in the system include:

* startups
* funding_rounds
* investors

The agent must ensure database queries are **efficient and well structured**.

---

# 4. Web Scraping Skills

The agent should be able to implement automated data collection.

Capabilities:

* Scraping structured data from web pages
* Parsing HTML content
* Handling pagination
* Cleaning scraped data
* Storing structured results in the database

Libraries that should be used:

* Requests
* BeautifulSoup
* Selenium when necessary for dynamic content

The agent must ensure scrapers are **fault tolerant and reusable**.

---

# 5. Data Processing and Feature Engineering

The agent must build reliable preprocessing pipelines.

Responsibilities include:

* Handling missing data
* Encoding categorical features
* Scaling numerical features
* Generating derived features

Example engineered features include:

* startup_age
* investor_count
* funding_history
* team_size

Data processing pipelines should be **reusable and modular**.

---

# 6. Machine Learning Development Skills

The agent should be capable of training and deploying machine learning models.

Required capabilities:

* Training models using XGBoost
* Evaluating model performance
* Hyperparameter tuning
* Saving trained models
* Loading models for inference

The agent should ensure models are stored in a version-controlled structure.

Model artifacts must be saved in the backend models directory.

---

# 7. Model Explainability

The agent should integrate explainability tools to interpret predictions.

Tool:

SHAP

Capabilities:

* Generate SHAP value explanations
* Display feature importance
* Provide interpretable prediction outputs

This ensures transparency in the prediction system.

---

# 8. Experiment Tracking

The agent must implement experiment tracking using MLflow.

Responsibilities:

* Log model parameters
* Log training metrics
* Store model artifacts
* Maintain experiment history

The agent should ensure MLflow experiments are **structured and reproducible**.

---

# 9. Frontend Development Skills

The agent should generate a professional React dashboard.

Capabilities include:

* Creating modular React components
* Building interactive dashboards
* Fetching data from APIs
* Integrating Supabase client for database queries
* Managing application state

Recommended libraries:

* Recharts for visualizations
* Axios for API calls

Frontend components should be reusable and well organized.

---

# 10. Data Visualization

The agent must implement visual dashboards that display:

* funding trends
* top industries
* startup ecosystem insights
* prediction outputs

Charts should be interactive and responsive.

Preferred tools:

* Recharts
* Chart.js

---

# 11. API Integration Skills

The agent must manage communication between frontend and backend.

Capabilities include:

* sending prediction requests
* retrieving analytics data
* handling API responses
* managing loading states and errors

All API communication should follow **clean and documented endpoints**.

---

# 12. Containerization Skills

The agent must support containerized development.

Responsibilities:

* creating Dockerfiles
* defining docker-compose configuration
* ensuring services start correctly

Services expected:

* backend service
* frontend service
* MLflow tracking server

---

# 13. Debugging and Error Handling

The agent should actively monitor and resolve development issues.

Capabilities include:

* identifying runtime errors
* fixing dependency conflicts
* resolving API failures
* diagnosing database connectivity issues

All errors should include **clear logging and debugging information**.

---

# 14. Code Quality Standards

The agent must enforce the following standards:

* modular code structure
* descriptive variable names
* clear function documentation
* separation of concerns
* minimal code duplication

The agent should also ensure:

* readable commit messages
* well structured repositories
* clear project documentation

---

# 15. Performance Optimization

The agent should optimize system performance by:

* reducing redundant database queries
* caching frequently accessed data
* minimizing API latency
* optimizing data processing pipelines

The agent should prioritize **efficient resource usage**.

---

# 16. Security Awareness

The agent must ensure basic security practices:

* protect API keys and secrets
* avoid exposing database credentials
* validate user inputs
* sanitize incoming requests

Sensitive values should be stored in environment variables.

---

# 17. Documentation Skills

The agent must automatically maintain documentation.

Responsibilities:

* update README files
* document API endpoints
* describe system architecture
* maintain setup instructions

Documentation must allow developers to **run the project easily**.

---

# 18. Development Workflow Optimization

The agent should maintain a structured workflow:

1. Implement database schema
2. Implement scraping pipeline
3. Build data preprocessing pipeline
4. Train machine learning models
5. Implement backend API
6. Build frontend dashboard
7. Integrate prediction endpoints
8. Containerize services
9. Deploy application

The agent must follow this sequence to ensure smooth development.

---

# 19. Continuous Improvement

The agent should continuously improve the project by:

* identifying architectural improvements
* optimizing model performance
* improving UI/UX
* enhancing system scalability

The goal is to maintain a **production-quality data science application**.

---

# 20. Final Goal

The Antigravity agent should help produce a **fully functioning full-stack data science platform** capable of:

* collecting startup funding data
* analyzing market trends
* predicting funding success
* presenting insights through a professional dashboard

The system should demonstrate **end-to-end machine learning product development**.
