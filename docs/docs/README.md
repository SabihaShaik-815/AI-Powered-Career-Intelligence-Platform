# CareerCast Documentation

Welcome to the documentation for CareerCast — an AI-Powered Career Intelligence Platform for resume analysis, career prediction, career recommendations, and skill-gap analysis.

## 1. Project Overview

CareerCast analyzes a user's resume and provides:

- Resume parsing
- Skill extraction
- Education extraction
- Career prediction
- Top-K career recommendations
- Confidence scores
- Skill alignment analysis
- Skill-gap analysis
- Career comparison
- Cohort analytics
- PDF report export

The platform combines Natural Language Processing (NLP), Machine Learning (ML), and recommendation techniques to help users understand suitable career paths.

---

## 2. Project Architecture

The project contains several major components:

```text
CareerCast
│
├── app.py
│
├── careercast/
│   ├── __init__.py
│   ├── parser.py
│   ├── models.py
│   ├── predictor.py
│   ├── recommender.py
│   └── cli.py
│
├── api/
│   └── main.py
│
├── models/
│   ├── role_classifier.joblib
│   ├── role_tfidf_vectorizer.joblib
│   ├── role_classes.json
│   └── role_metrics.json
│
├── advanced_models/
│   ├── random_forest_model.pkl
│   ├── xgboost_model.pkl
│   ├── label_encoder.pkl
│   ├── tfidf_vectorizer.joblib
│   └── advanced_metrics.json
│
├── tests/
│   ├── test_parser.py
│   ├── test_prediction.py
│   ├── test_recommendation.py
│   └── test_integration.py
│
├── docs/
│   ├── README.md
│   ├── API_REFERENCE.md
│   ├── CLI_REFERENCE.md
│   ├── DATASET_CARD.md
│   └── MODEL_CARD.md
│
└── streamlit_app.py