# ============================================================
# AI CAREER INTELLIGENCE PLATFORM
# MILESTONE 3 - FASTAPI REST API
# ============================================================

import json
import logging
from pathlib import Path
from typing import List, Optional

import joblib
import mlflow
import numpy as np
import spacy

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODELS_DIR = BASE_DIR / "models"

ADVANCED_MODELS_DIR = BASE_DIR / "advanced_models"

MLFLOW_DB = BASE_DIR / "mlflow.db"


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="AI Career Intelligence API",
    description="Milestone 3 REST API",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# MLFLOW CONFIGURATION
# ============================================================

try:

    mlflow.set_tracking_uri(
        f"sqlite:///{MLFLOW_DB}"
    )

    mlflow.set_experiment(
        "AI-Career-Intelligence-Milestone-3"
    )

    logger.info("MLflow configured successfully.")

except Exception as error:

    logger.warning(
        "MLflow configuration warning: %s",
        error
    )


# ============================================================
# REQUEST SCHEMAS
# ============================================================

class PredictRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=10,
        description="Resume or candidate text"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10
    )


class RecommendationRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=10
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10
    )


class SkillGapRequest(BaseModel):

    role: str

    skills: List[str]


class ReportRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=10
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10
    )


# ============================================================
# ROLE-SKILL PROFILES
# ============================================================

ROLE_SKILL_PROFILES = {

    "Data Scientist": [
        "Python",
        "Machine Learning",
        "SQL",
        "Statistics",
        "Pandas",
        "Deep Learning",
        "Data Visualization"
    ],

    "Software Engineer": [
        "Python",
        "Java",
        "Git",
        "REST API",
        "Docker",
        "CI/CD"
    ],

    "Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "TensorFlow",
        "PyTorch",
        "Deep Learning",
        "Docker",
        "AWS"
    ],

    "Data Analyst": [
        "SQL",
        "Excel",
        "Data Analysis",
        "Data Visualization",
        "Tableau",
        "Power BI",
        "Statistics"
    ],

    "Product Manager": [
        "Product Management",
        "Stakeholder Management",
        "Agile",
        "Business Analysis",
        "Communication",
        "Strategic Planning"
    ],

    "DevOps Engineer": [
        "Docker",
        "Kubernetes",
        "CI/CD",
        "AWS",
        "Azure",
        "Git",
        "Microservices"
    ],

    "Business Analyst": [
        "Business Analysis",
        "SQL",
        "Excel",
        "Stakeholder Management",
        "Communication",
        "Data Analysis"
    ],

    "Marketing Manager": [
        "Digital Marketing",
        "SEO",
        "Content Marketing",
        "Social Media Marketing",
        "Communication"
    ],

    "Backend Developer": [
        "Python",
        "Java",
        "SQL",
        "REST API",
        "Docker",
        "Git"
    ],

    "Frontend Developer": [
        "JavaScript",
        "TypeScript",
        "React",
        "HTML",
        "CSS",
        "Git"
    ],

    "Full Stack Developer": [
        "JavaScript",
        "React",
        "Node.js",
        "HTML",
        "CSS",
        "SQL",
        "REST API"
    ],

    "Cloud Engineer": [
        "AWS",
        "Azure",
        "Docker",
        "Kubernetes",
        "CI/CD",
        "Linux"
    ],

    "Project Manager": [
        "Project Management",
        "Agile",
        "Scrum",
        "Leadership",
        "Communication",
        "Stakeholder Management"
    ]

}


# ============================================================
# SKILLS GAZETTEER
# ============================================================

SKILLS = [

    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "C++",
    "C#",
    "SQL",
    "R",
    "Go",
    "Rust",
    "Scala",
    "PHP",
    "Ruby",
    "Swift",
    "Kotlin",
    "MATLAB",

    "Machine Learning",
    "Deep Learning",
    "Data Analysis",
    "Data Science",
    "Natural Language Processing",
    "Computer Vision",

    "TensorFlow",
    "PyTorch",
    "scikit-learn",
    "Pandas",
    "NumPy",
    "Data Visualization",
    "Statistics",

    "A/B Testing",
    "Tableau",
    "Power BI",
    "Excel",

    "React",
    "Angular",
    "Vue.js",
    "Node.js",
    "Django",
    "Flask",
    "FastAPI",

    "REST API",
    "GraphQL",

    "HTML",
    "CSS",

    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "Google Cloud Platform",
    "CI/CD",
    "Git",
    "Microservices",

    "Agile",
    "Scrum",

    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Redis",
    "Snowflake",
    "BigQuery",

    "Spark",
    "Hadoop",

    "Project Management",
    "Product Management",
    "Leadership",
    "Communication",
    "Stakeholder Management",
    "Business Analysis",
    "Strategic Planning",
    "Negotiation",
    "Team Management",
    "Public Speaking",
    "Problem Solving",
    "Critical Thinking",

    "Digital Marketing",
    "SEO",
    "Content Marketing",
    "Social Media Marketing",
    "Salesforce",
    "CRM",
    "Lead Generation",

    "UX Design",
    "UI Design",
    "Figma",
    "Adobe Photoshop",
    "Adobe Illustrator",

    "Linux"
]


# ============================================================
# LOAD MODELS
# ============================================================

logger.info("=" * 65)
logger.info("AI CAREER INTELLIGENCE API")
logger.info("MILESTONE 3")
logger.info("=" * 65)


# ------------------------------------------------------------
# spaCy
# ------------------------------------------------------------

logger.info("Loading spaCy model...")

try:

    nlp = spacy.load(
        "en_core_web_sm"
    )

    logger.info(
        "spaCy model loaded successfully."
    )

except Exception as error:

    logger.error(
        "Could not load spaCy model: %s",
        error
    )

    nlp = None


# ------------------------------------------------------------
# Role classifier
# ------------------------------------------------------------

logger.info("Loading role classifier...")

ROLE_CLASSIFIER_PATH = (
    MODELS_DIR /
    "role_classifier.joblib"
)

ROLE_TFIDF_PATH = (
    MODELS_DIR /
    "role_tfidf_vectorizer.joblib"
)


try:

    role_classifier = joblib.load(
        ROLE_CLASSIFIER_PATH
    )

    role_tfidf = joblib.load(
        ROLE_TFIDF_PATH
    )

    logger.info(
        "Role classifier loaded successfully."
    )

except Exception as error:

    logger.error(
        "Could not load role classifier: %s",
        error
    )

    role_classifier = None
    role_tfidf = None


# ------------------------------------------------------------
# XGBoost
# ------------------------------------------------------------

logger.info("Loading XGBoost model...")

XGB_PATH = (
    ADVANCED_MODELS_DIR /
    "xgboost_model.pkl"
)


try:

    xgb_model = joblib.load(
        XGB_PATH
    )

    logger.info(
        "XGBoost model loaded successfully."
    )

except Exception as error:

    logger.error(
        "Could not load XGBoost model: %s",
        error
    )

    xgb_model = None


# ------------------------------------------------------------
# Random Forest
# ------------------------------------------------------------

logger.info("Loading Random Forest model...")

RF_PATH = (
    ADVANCED_MODELS_DIR /
    "random_forest_model.pkl"
)


try:

    rf_model = joblib.load(
        RF_PATH
    )

    logger.info(
        "Random Forest model loaded successfully."
    )

except Exception as error:

    logger.error(
        "Could not load Random Forest model: %s",
        error
    )

    rf_model = None


# ------------------------------------------------------------
# Advanced TF-IDF
# ------------------------------------------------------------

logger.info("Loading advanced TF-IDF...")

ADVANCED_TFIDF_PATH = (
    ADVANCED_MODELS_DIR /
    "tfidf_vectorizer.joblib"
)


try:

    advanced_tfidf = joblib.load(
        ADVANCED_TFIDF_PATH
    )

    logger.info(
        "Advanced TF-IDF loaded successfully."
    )

except Exception as error:

    logger.error(
        "Could not load advanced TF-IDF: %s",
        error
    )

    advanced_tfidf = None


# ------------------------------------------------------------
# Label Encoder
# ------------------------------------------------------------

logger.info("Loading label encoder...")

LABEL_ENCODER_PATH = (
    ADVANCED_MODELS_DIR /
    "label_encoder.pkl"
)


try:

    label_encoder = joblib.load(
        LABEL_ENCODER_PATH
    )

    logger.info(
        "Label encoder loaded successfully."
    )

except Exception as error:

    logger.error(
        "Could not load label encoder: %s",
        error
    )

    label_encoder = None


# ------------------------------------------------------------
# Advanced metrics
# ------------------------------------------------------------

METRICS_PATH = (
    ADVANCED_MODELS_DIR /
    "advanced_metrics.json"
)

advanced_metrics = {}

try:

    if METRICS_PATH.exists():

        with open(
            METRICS_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            advanced_metrics = json.load(
                file
            )

        logger.info(
            "Advanced metrics loaded successfully."
        )

except Exception as error:

    logger.warning(
        "Could not load advanced metrics: %s",
        error
    )


logger.info("=" * 65)


# ============================================================
# HELPER: MODEL STATUS
# ============================================================

def model_status():

    return {

        "role_classifier":
            role_classifier is not None,

        "xgboost":
            xgb_model is not None,

        "random_forest":
            rf_model is not None,

        "advanced_tfidf":
            advanced_tfidf is not None,

        "label_encoder":
            label_encoder is not None,

        "spacy":
            nlp is not None
    }


# ============================================================
# HELPER: EXTRACT SKILLS
# ============================================================

def extract_skills(text: str):

    found_skills = []

    text_lower = text.lower()

    for skill in SKILLS:

        skill_lower = skill.lower()

        if skill_lower in text_lower:

            found_skills.append(
                skill
            )

    return sorted(
        set(found_skills)
    )


# ============================================================
# HELPER: ROLE PREDICTION
# ============================================================

def predict_with_role_classifier(
    text: str,
    top_k: int = 5
):

    if (
        role_classifier is None
        or role_tfidf is None
    ):

        raise HTTPException(
            status_code=503,
            detail="Role classifier is not available."
        )

    try:

        X = role_tfidf.transform(
            [text]
        )

        probabilities = (
            role_classifier
            .predict_proba(X)[0]
        )

        classes = (
            role_classifier.classes_
        )

        ranked = sorted(
            zip(
                classes,
                probabilities
            ),
            key=lambda item: item[1],
            reverse=True
        )[:top_k]

        results = []

        for role, probability in ranked:

            results.append(
                {
                    "role": str(role),
                    "confidence": round(
                        float(probability),
                        4
                    ),
                    "confidence_percentage":
                        round(
                            float(probability) * 100,
                            2
                        )
                }
            )

        return results

    except Exception as error:

        logger.error(
            "Role prediction failed: %s",
            error
        )

        raise HTTPException(
            status_code=500,
            detail="Role prediction failed."
        )


# ============================================================
# HELPER: ADVANCED MODEL PREDICTION
# ============================================================

def predict_with_advanced_model(
    model,
    text: str,
    top_k: int = 5
):

    if model is None:

        return []

    if advanced_tfidf is None:

        return []

    if label_encoder is None:

        return []

    try:

        X = advanced_tfidf.transform(
            [text]
        )

        probabilities = (
            model.predict_proba(X)[0]
        )

        class_ids = np.argsort(
            probabilities
        )[::-1][:top_k]

        results = []

        for class_id in class_ids:

            probability = (
                probabilities[class_id]
            )

            try:

                role = label_encoder.inverse_transform(
                    [int(class_id)]
                )[0]

            except Exception:

                role = str(class_id)

            results.append(
                {
                    "role": str(role),
                    "confidence": round(
                        float(probability),
                        4
                    ),
                    "confidence_percentage":
                        round(
                            float(probability) * 100,
                            2
                        )
                }
            )

        return results

    except Exception as error:

        logger.error(
            "Advanced model prediction failed: %s",
            error
        )

        return []


# ============================================================
# HELPER: SKILL GAP
# ============================================================

def calculate_gap(
    role: str,
    skills: List[str]
):

    required = ROLE_SKILL_PROFILES.get(
        role,
        []
    )

    user_skills = {
        skill.lower().strip()
        for skill in skills
    }

    matched = []

    missing = []

    for skill in required:

        if skill.lower() in user_skills:

            matched.append(
                skill
            )

        else:

            missing.append(
                skill
            )

    total = len(required)

    if total > 0:

        alignment = (
            len(matched) / total
        )

    else:

        alignment = 0.0

    return {

        "role":
            role,

        "required_skills":
            required,

        "matched_skills":
            matched,

        "missing_skills":
            missing,

        "skill_alignment":
            round(
                alignment,
                4
            ),

        "skill_alignment_percentage":
            round(
                alignment * 100,
                2
            )
    }


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {

        "application":
            "AI Career Intelligence API",

        "version":
            "1.0.0",

        "milestone":
            "Milestone 3 REST API",

        "status":
            "running",

        "documentation":
            "/docs"
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    status = model_status()

    all_models_loaded = all(
        status.values()
    )

    return {

        "status":
            "healthy"
            if all_models_loaded
            else "degraded",

        "service":
            "AI Career Intelligence API",

        "milestone":
            "Milestone 3",

        "models":
            status
    }


# ============================================================
# PREDICT
# ============================================================

@app.post("/predict")
def predict(request: PredictRequest):

    text = request.text.strip()

    predictions = (
        predict_with_role_classifier(
            text,
            request.top_k
        )
    )

    skills = extract_skills(
        text
    )

    advanced_xgb = (
        predict_with_advanced_model(
            xgb_model,
            text,
            request.top_k
        )
    )

    advanced_rf = (
        predict_with_advanced_model(
            rf_model,
            text,
            request.top_k
        )
    )

    return {

        "success":
            True,

        "model":
            "Role Classifier",

        "predictions":
            predictions,

        "top_role":
            predictions[0]["role"]
            if predictions
            else None,

        "skills":
            skills,

        "advanced_models": {

            "xgboost":
                advanced_xgb,

            "random_forest":
                advanced_rf
        }
    }


# ============================================================
# RECOMMEND
# ============================================================

@app.post("/recommend")
def recommend(
    request: RecommendationRequest
):

    text = request.text.strip()

    skills = extract_skills(
        text
    )

    predictions = (
        predict_with_advanced_model(
            xgb_model,
            text,
            request.top_k
        )
    )

    if not predictions:

        predictions = (
            predict_with_role_classifier(
                text,
                request.top_k
            )
        )

    recommendations = []

    for prediction in predictions:

        role = prediction["role"]

        gap = calculate_gap(
            role,
            skills
        )

        confidence = (
            prediction["confidence"]
        )

        alignment = (
            gap["skill_alignment"]
        )

        recommendation_score = (
            0.6 * confidence
            +
            0.4 * alignment
        )

        recommendations.append(
            {

                "role":
                    role,

                "confidence":
                    confidence,

                "confidence_percentage":
                    prediction[
                        "confidence_percentage"
                    ],

                "skill_alignment":
                    alignment,

                "skill_alignment_percentage":
                    gap[
                        "skill_alignment_percentage"
                    ],

                "recommendation_score":
                    round(
                        recommendation_score,
                        4
                    ),

                "matched_skills":
                    gap[
                        "matched_skills"
                    ],

                "missing_skills":
                    gap[
                        "missing_skills"
                    ]
            }
        )

    recommendations.sort(
        key=lambda item:
        item["recommendation_score"],
        reverse=True
    )

    return {

        "success":
            True,

        "skills":
            skills,

        "recommendations":
            recommendations
    }


# ============================================================
# SKILL GAP
# ============================================================

@app.post("/skill-gap")
def skill_gap(
    request: SkillGapRequest
):

    result = calculate_gap(
        request.role,
        request.skills
    )

    return {

        "success":
            True,

        **result
    }


# ============================================================
# REPORT
# ============================================================

@app.post("/report")
def generate_report(
    request: ReportRequest
):

    text = request.text.strip()

    skills = extract_skills(
        text
    )

    predictions = (
        predict_with_advanced_model(
            xgb_model,
            text,
            request.top_k
        )
    )

    if not predictions:

        predictions = (
            predict_with_role_classifier(
                text,
                request.top_k
            )
        )

    recommendations = []

    for prediction in predictions:

        role = prediction[
            "role"
        ]

        gap = calculate_gap(
            role,
            skills
        )

        recommendations.append(
            {

                "role":
                    role,

                "confidence":
                    prediction[
                        "confidence"
                    ],

                "skill_alignment":
                    gap[
                        "skill_alignment"
                    ],

                "matched_skills":
                    gap[
                        "matched_skills"
                    ],

                "missing_skills":
                    gap[
                        "missing_skills"
                    ]
            }
        )

    top_role = (
        recommendations[0]["role"]
        if recommendations
        else None
    )

    return {

        "success":
            True,

        "report": {

            "candidate_profile": {

                "extracted_skills":
                    skills,

                "skill_count":
                    len(skills)
            },

            "career_prediction": {

                "top_role":
                    top_role,

                "top_predictions":
                    predictions
            },

            "career_recommendations":
                recommendations,

            "model_information": {

                "primary_model":
                    "XGBoost",

                "fallback_model":
                    "Role Classifier",

                "milestone":
                    "Milestone 3"
            }
        }
    }


# ============================================================
# METRICS
# ============================================================

@app.get("/metrics")
def metrics():

    rf_accuracy = None

    xgb_accuracy = None

    best_model = None

    best_accuracy = None


    if advanced_metrics:

        rf_data = (
            advanced_metrics.get(
                "random_forest",
                {}
            )
        )

        xgb_data = (
            advanced_metrics.get(
                "xgboost",
                {}
            )
        )

        rf_accuracy = (
            rf_data.get(
                "accuracy"
            )
        )

        xgb_accuracy = (
            xgb_data.get(
                "accuracy"
            )
        )

        best_model = (
            advanced_metrics.get(
                "best_model"
            )
        )

        best_accuracy = (
            advanced_metrics.get(
                "best_accuracy"
            )
        )


    return {

        "success":
            True,

        "milestone":
            "Milestone 3",

        "models": {

            "random_forest": {

                "accuracy":
                    rf_accuracy
            },

            "xgboost": {

                "accuracy":
                    xgb_accuracy
            }
        },

        "best_model":
            best_model,

        "best_accuracy":
            best_accuracy,

        "mlflow": {

            "tracking_uri":
                f"sqlite:///{MLFLOW_DB}",

            "experiment":
                "AI-Career-Intelligence-Milestone-3"
        }
    }


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def startup_event():

    logger.info("=" * 65)
    logger.info(
        "Career Intelligence API startup complete."
    )
    logger.info(
        "Swagger: http://127.0.0.1:8000/docs"
    )
    logger.info(
        "OpenAPI: http://127.0.0.1:8000/openapi.json"
    )
    logger.info("=" * 65)


# ============================================================
# END
# ============================================================
