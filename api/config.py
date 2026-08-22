from pathlib import Path


# ============================================================
# PROJECT BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# MODEL DIRECTORIES
# ============================================================

MODELS_DIR = BASE_DIR / "models"

ADVANCED_MODELS_DIR = BASE_DIR / "advanced_models"


# ============================================================
# EXISTING ROLE CLASSIFIER
# ============================================================

ROLE_MODEL = (
    MODELS_DIR /
    "role_classifier.joblib"
)

ROLE_TFIDF = (
    MODELS_DIR /
    "role_tfidf_vectorizer.joblib"
)


# ============================================================
# MILESTONE 2 ADVANCED MODELS
# ============================================================

XGBOOST_MODEL = (
    ADVANCED_MODELS_DIR /
    "xgboost_model.pkl"
)

RANDOM_FOREST_MODEL = (
    ADVANCED_MODELS_DIR /
    "random_forest_model.pkl"
)

ADVANCED_TFIDF = (
    ADVANCED_MODELS_DIR /
    "tfidf_vectorizer.joblib"
)

LABEL_ENCODER = (
    ADVANCED_MODELS_DIR /
    "label_encoder.pkl"
)


# ============================================================
# METRICS
# ============================================================

ADVANCED_METRICS = (
    ADVANCED_MODELS_DIR /
    "advanced_metrics.json"
)

ROLE_METRICS = (
    MODELS_DIR /
    "role_metrics.json"
)


# ============================================================
# DATABASE
# ============================================================

DATABASE_PATH = (
    BASE_DIR /
    "careercast.db"
)