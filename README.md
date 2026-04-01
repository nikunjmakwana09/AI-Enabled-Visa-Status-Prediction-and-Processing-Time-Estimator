# AI-Enabled Visa Status Prediction & Processing Time Estimator

An AI-powered platform that predicts visa processing time and provides intelligent embassy insights using machine learning and generative AI.

The system combines **machine learning prediction**, **AI-generated advisory insights**, and **interactive analytics** to help applicants understand expected visa timelines and possible delays.

---

# Live Demo

### AI Dashboard

Streamlit Web Application

```
https://ai-visa-time-estimstor.streamlit.app/
```

### Prediction API

FastAPI Cloud Service

```
https://ai-enabled-visa-status-prediction-and-tg4s.onrender.com
```

### API Documentation

```
https://ai-enabled-visa-status-prediction-and-tg4s.onrender.com/docs
```

---

# Project Overview

Visa applicants often face uncertainty about **processing timelines, embassy workload, and potential delays**.

This project builds an **AI-powered prediction platform** that estimates visa processing time and provides actionable insights to applicants.

The system analyzes historical visa data and predicts expected processing time using machine learning.

In addition, a generative AI system produces an **embassy intelligence report** explaining possible delays and guidance for applicants.

---

# Key Features

### AI Processing Time Prediction

Predicts visa processing time based on:

- application month
- geographic region
- processing embassy
- visa type

---

### Confidence Interval Estimation

The system provides:

- predicted processing days
- lower and upper confidence range
- model confidence score
- residual-based uncertainty estimation

This helps users understand prediction reliability in real-world scenarios.

---

### AI Embassy Intelligence Report

Using generative AI, the platform generates a structured embassy advisory report including:

- embassy overview
- contact information
- visa processing insights
- delay risk assessment
- practical guidance for applicants
- tips to avoid delays

---

### Interactive Web Dashboard

Users interact with the system through a modern AI dashboard featuring:

- visa application input form
- AI prediction display
- confidence metrics
- AI advisory reports
- global analytics dashboard

---

### Explainable AI

Model predictions are supported with explainability techniques including:

- feature importance analysis
- SHAP-based model interpretation

This increases transparency of the AI system.

---

# System Architecture

The system uses a **microservice-based AI architecture** separating the frontend interface and prediction engine.

```
User
 │
 ▼
Streamlit AI Dashboard
 │
 ▼
Prediction Request
 │
 ├── FastAPI Prediction API (Render Cloud)
 │        │
 │        ▼
 │   Machine Learning Model (Stacking Ensemble)
 │        │
 │        ▼
 │   AI Insight Generator (Gemini)
 │
 └── Fallback Mechanism (If API Unavailable)
          │
          ▼
     Local Prediction Engine (Stacking Ensemble)
```

The Streamlit dashboard first sends prediction requests to the cloud-based FastAPI service. If the API is temporarily unavailable, the system automatically switches to a local prediction engine, ensuring uninterrupted visa processing time estimation for users.

This architecture enables:

- scalability
- reliability
- availability
- API integrations
- modular development
- cloud deployment

---

# Technology Stack

### Machine Learning

- XGBoost
- Random Forest
- Gradient Boosting
- Stacking Regressor
- Scikit-learn
- SHAP

---

### Backend

- FastAPI
- Python

---

### Frontend

- Streamlit
- Plotly
- Custom CSS dashboard UI

---

### AI Integration

- Google Gemini API for embassy intelligence reports

---

### Deployment

Frontend

```
Streamlit Community Cloud
```

Backend API

```
Render Cloud Platform
```

---

### Monitoring

- API health endpoints
- Better Stack uptime monitoring
- request logging
- latency tracking
- model performance monitoring (MAE, confidence)
- drift detection (KS statistic)

---

# API Endpoints

### Prediction

```
POST /predict
```

Returns predicted visa processing time.

Example request:

```json
{
 "fiscal_year": 2025,
 "application_month": 6,
 "region": "AS",
 "processing_office": "NWD",
 "visa_type": "Diversity Visa (DV)"
}
```

---

### Health Check

```
GET /health
```
Returns:
- API status
- model type
- model performance (MAE)

Checks if the API service is running.

---


# Machine Learning Pipeline

The machine learning pipeline includes:

1. Data ingestion
2. Data preprocessing
3. Feature engineering
4. Time-aware model training (no data leakage)
5. Hyperparameter tuning
6. Model evaluation
7. Model explainability
8. Model deployment
9. Model monitoring & drift detection
---

# Model Performance

Multiple regression models were evaluated:

| Model             | Description                |
|-------------------|----------------------------|
| Linear Regression | baseline model             |
| Random Forest     | ensemble model             |
| Gradient Boosting | boosting algorithm         |
| XGBoost           | optimized gradient boosting|
| Stacking Regressor| final production model     |

The **Stacking Ensemble model** was selected as the final model due to improved generalization and real-world stability.
---

# Project Structure

```
app/
 ├── web_app.py
 ├── api_service.py
 ├── estimator_engine.py
 ├── ai_embassy_assistant.py
 ├── sample_request.py
 ├── ui_config.py
 ├── charts.py
 ├── assets/
 │   ├── logo.png
 │   ├── style.css
 │   └── ai_background.html
 │  
 ├── data/
 │   └── offices.py
 │  
 └── ui/
     └── ai_pipeline.py

data/
 ├── raw/
 │   └── FY2013–FY2025 CEAC datasets
 │
 └── processed/
     ├── 2013_2025_raw_dataset.csv
     └── cleaned_dataset.csv

models/
 ├── best_model.pkl
 ├── preprocessor.pkl
 ├── feature_schema.json
 ├── model_metadata.json
 ├── model_report.json
 └── drift_report.json

notebooks/scripts/
 ├── combine_datasets.py
 ├── prepare_dataset.py
 ├── eda_feature_engineering.py
 └── model_training.py

outputs/
plots/
documentation/

.env.example
.gitignore
requirements.txt
Milestone_1_README.md
Milestone_2_README.md
Milestone_3_README.md
Milestone_4_README.md
README.md
```

---

# Future Improvements

Possible enhancements for future versions:

- real-time visa processing data integration
- automated model retraining pipeline
- advanced global analytics dashboard
- additional visa categories
- mobile application interface
- multilingual support
- personalized applicant recommendations

---

# MIT License

Copyright (c) 2026 Vidzai Digital

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

# Acknowledgements

This project was developed to explore the application of **machine learning and generative AI in public service analytics** and demonstrate modern AI system deployment techniques.
