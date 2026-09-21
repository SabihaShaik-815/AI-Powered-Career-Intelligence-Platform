"""
CareerCast Career Prediction Module

Provides:
- Career role prediction
- Model loading
- Confidence score calculation
- Top-K career predictions
- Model information
- Compatibility with advanced CareerCast models

Supported advanced models:
- XGBoost
- Random Forest

Legacy model:
- role_classifier
"""

import os
import json

import joblib
import numpy as np


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ============================================================
# MODEL DIRECTORIES
# ============================================================

ADVANCED_MODELS_DIR = os.path.join(
    BASE_DIR,
    "advanced_models"
)

MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)


# ============================================================
# MODEL FILES
# ============================================================

ADVANCED_MODEL_FILES = {
    "random_forest": os.path.join(
        ADVANCED_MODELS_DIR,
        "random_forest_model.pkl"
    ),

    "xgboost": os.path.join(
        ADVANCED_MODELS_DIR,
        "xgboost_model.pkl"
    ),
}

LEGACY_MODEL_FILES = {
    "role_classifier": os.path.join(
        MODELS_DIR,
        "role_classifier.joblib"
    )
}


# ============================================================
# LOAD MODEL
# ============================================================

def load_model(model_name="xgboost"):
    """
    Load a trained CareerCast model.

    Parameters
    ----------
    model_name : str
        Supported values:
        - xgboost
        - random_forest
        - role_classifier

    Returns
    -------
    object
        Loaded model.
    """

    model_name = str(
        model_name
    ).lower().strip()

    model_files = {}

    model_files.update(
        ADVANCED_MODEL_FILES
    )

    model_files.update(
        LEGACY_MODEL_FILES
    )

    model_path = model_files.get(
        model_name
    )

    if not model_path:
        raise ValueError(
            f"Unknown model: {model_name}. "
            f"Supported models: "
            f"{', '.join(model_files.keys())}"
        )

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found: {model_path}"
        )

    return joblib.load(
        model_path
    )


# ============================================================
# LOAD ADVANCED TF-IDF VECTORIZER
# ============================================================

def load_vectorizer():
    """
    Load the TF-IDF vectorizer used by the
    advanced XGBoost and Random Forest models.
    """

    vectorizer_path = os.path.join(
        ADVANCED_MODELS_DIR,
        "tfidf_vectorizer.joblib"
    )

    if not os.path.exists(
        vectorizer_path
    ):
        raise FileNotFoundError(
            f"Vectorizer not found: "
            f"{vectorizer_path}"
        )

    return joblib.load(
        vectorizer_path
    )


# ============================================================
# LOAD LEGACY MODEL PIPELINE
# ============================================================

def load_legacy_model():
    """
    Load the original role classifier.

    This model contains its own preprocessing
    pipeline and must NOT be given the advanced
    TF-IDF feature matrix.
    """

    model_path = os.path.join(
        MODELS_DIR,
        "role_classifier.joblib"
    )

    if not os.path.exists(
        model_path
    ):
        raise FileNotFoundError(
            f"Legacy model not found: "
            f"{model_path}"
        )

    return joblib.load(
        model_path
    )


# ============================================================
# LOAD LABEL ENCODER
# ============================================================

def load_label_encoder():
    """
    Load the label encoder used by the
    advanced career prediction models.
    """

    encoder_path = os.path.join(
        ADVANCED_MODELS_DIR,
        "label_encoder.pkl"
    )

    if not os.path.exists(
        encoder_path
    ):
        raise FileNotFoundError(
            f"Label encoder not found: "
            f"{encoder_path}"
        )

    return joblib.load(
        encoder_path
    )


# ============================================================
# LOAD MODEL METRICS
# ============================================================

def load_model_metrics():
    """
    Load advanced model metrics.
    """

    metrics_path = os.path.join(
        ADVANCED_MODELS_DIR,
        "advanced_metrics.json"
    )

    if not os.path.exists(
        metrics_path
    ):
        return {}

    try:

        with open(
            metrics_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    except Exception:

        return {}


# ============================================================
# PREPARE RESUME TEXT
# ============================================================

def prepare_text(text):
    """
    Clean and normalize resume text.
    """

    if not text:
        return ""

    text = str(
        text
    )

    text = " ".join(
        text.split()
    )

    return text


# ============================================================
# GET TOP-K INDICES
# ============================================================

def _get_top_indices(
    probabilities,
    top_k
):
    """
    Return indices of the highest
    probability predictions.
    """

    probabilities = np.asarray(
        probabilities,
        dtype=float
    )

    if probabilities.ndim != 1:
        probabilities = probabilities.flatten()

    if len(probabilities) == 0:
        return []

    top_k = min(
        int(top_k),
        len(probabilities)
    )

    return np.argsort(
        probabilities
    )[::-1][:top_k]


# ============================================================
# ADVANCED MODEL PREDICTION
# ============================================================

def _predict_advanced_model(
    resume_text,
    model,
    vectorizer,
    label_encoder,
    top_k
):
    """
    Predict using the advanced XGBoost
    or Random Forest model.

    Pipeline:

        Resume Text
             ↓
        TF-IDF Vectorizer
             ↓
        ML Model
             ↓
        Probability Scores
             ↓
        Label Encoder
             ↓
        Top-K Careers
    """

    # --------------------------------------------------------
    # Transform resume text
    # --------------------------------------------------------

    features = vectorizer.transform(
        [resume_text]
    )

    # --------------------------------------------------------
    # Probability prediction
    # --------------------------------------------------------

    if hasattr(
        model,
        "predict_proba"
    ):

        probabilities = model.predict_proba(
            features
        )[0]

    else:

        prediction = model.predict(
            features
        )[0]

        class_count = len(
            label_encoder.classes_
        )

        probabilities = np.zeros(
            class_count,
            dtype=float
        )

        try:
            prediction_index = int(
                prediction
            )

        except (
            ValueError,
            TypeError
        ):
            prediction_index = 0

        if (
            0 <= prediction_index
            < class_count
        ):
            probabilities[
                prediction_index
            ] = 1.0

    # --------------------------------------------------------
    # Top-K
    # --------------------------------------------------------

    top_indices = _get_top_indices(
        probabilities,
        top_k
    )

    predictions = []

    # --------------------------------------------------------
    # Convert class indexes to career roles
    # --------------------------------------------------------

    for rank, index in enumerate(
        top_indices,
        start=1
    ):

        try:

            role = label_encoder.inverse_transform(
                [int(index)]
            )[0]

        except Exception:

            role = str(
                index
            )

        confidence = float(
            probabilities[index]
        )

        predictions.append({

            "rank":
                rank,

            "role":
                str(role),

            "confidence":
                round(
                    confidence,
                    4
                ),

            "confidence_percentage":
                round(
                    confidence * 100,
                    2
                )
        })

    return predictions


# ============================================================
# LEGACY MODEL PREDICTION
# ============================================================

def _predict_legacy_model(
    resume_text,
    model,
    top_k
):
    """
    Predict using the original
    role_classifier pipeline.

    The legacy model expects the original
    structured input features, not the
    advanced TF-IDF matrix.
    """

    # --------------------------------------------------------
    # Legacy model prediction
    # --------------------------------------------------------

    try:

        prediction = model.predict(
            [resume_text]
        )

    except Exception as error:

        raise RuntimeError(
            "The legacy role_classifier model "
            "expects structured input features "
            "rather than raw resume text. "
            "Use XGBoost or Random Forest "
            "for CLI resume-text prediction."
        ) from error

    if len(prediction) == 0:
        return []

    role = str(
        prediction[0]
    )

    confidence = 1.0

    if hasattr(
        model,
        "predict_proba"
    ):

        try:

            probabilities = model.predict_proba(
                [resume_text]
            )[0]

            if len(probabilities) > 0:

                confidence = float(
                    np.max(
                        probabilities
                    )
                )

        except Exception:
            confidence = 1.0

    return [{

        "rank":
            1,

        "role":
            role,

        "confidence":
            round(
                confidence,
                4
            ),

        "confidence_percentage":
            round(
                confidence * 100,
                2
            )

    }]


# ============================================================
# PREDICT TOP-K CAREERS
# ============================================================

def predict_top_k(
    resume_text,
    model_name="xgboost",
    top_k=5
):
    """
    Predict Top-K career roles.

    Parameters
    ----------
    resume_text : str
        Resume text.

    model_name : str
        xgboost or random_forest.

    top_k : int
        Number of career predictions.

    Returns
    -------
    list
        Career predictions sorted by confidence.
    """

    resume_text = prepare_text(
        resume_text
    )

    if not resume_text:
        return []

    # --------------------------------------------------------
    # Validate model name
    # --------------------------------------------------------

    model_name = str(
        model_name
    ).lower().strip()

    # --------------------------------------------------------
    # Validate Top-K
    # --------------------------------------------------------

    try:

        top_k = int(
            top_k
        )

    except (
        ValueError,
        TypeError
    ):

        top_k = 5

    if top_k < 1:
        top_k = 1

    try:

        # ====================================================
        # ADVANCED MODELS
        # ====================================================

        if model_name in {
            "xgboost",
            "random_forest"
        }:

            model = load_model(
                model_name
            )

            vectorizer = load_vectorizer()

            label_encoder = load_label_encoder()

            return _predict_advanced_model(
                resume_text=resume_text,
                model=model,
                vectorizer=vectorizer,
                label_encoder=label_encoder,
                top_k=top_k
            )

        # ====================================================
        # LEGACY MODEL
        # ====================================================

        elif model_name == "role_classifier":

            model = load_legacy_model()

            return _predict_legacy_model(
                resume_text=resume_text,
                model=model,
                top_k=top_k
            )

        # ====================================================
        # UNKNOWN MODEL
        # ====================================================

        else:

            raise ValueError(
                f"Unsupported model: {model_name}. "
                f"Use 'xgboost' or 'random_forest'."
            )

    except Exception as error:

        print(
            "CAREER PREDICTION ERROR:",
            str(error)
        )

        return []


# ============================================================
# PREDICT SINGLE CAREER
# ============================================================

def predict_career(
    resume_text,
    model_name="xgboost"
):
    """
    Predict the most suitable career role.
    """

    predictions = predict_top_k(
        resume_text=resume_text,
        model_name=model_name,
        top_k=1
    )

    if not predictions:

        return {

            "role":
                "Not Available",

            "confidence":
                0,

            "confidence_percentage":
                0
        }

    prediction = predictions[0]

    return {

        "role":
            prediction["role"],

        "confidence":
            prediction["confidence"],

        "confidence_percentage":
            prediction[
                "confidence_percentage"
            ]
    }


# ============================================================
# COMPLETE PREDICTION RESULT
# ============================================================

def get_prediction_result(
    resume_text,
    model_name="xgboost",
    top_k=5
):
    """
    Generate complete prediction result.
    """

    predictions = predict_top_k(
        resume_text=resume_text,
        model_name=model_name,
        top_k=top_k
    )

    if not predictions:

        return {

            "success":
                False,

            "top_role":
                "Not Available",

            "confidence":
                0,

            "predictions":
                [],

            "model":
                model_name
        }

    top_prediction = predictions[0]

    return {

        "success":
            True,

        "top_role":
            top_prediction["role"],

        "confidence":
            top_prediction[
                "confidence_percentage"
            ],

        "model":
            model_name,

        "predictions":
            predictions
    }


# ============================================================
# MODEL INFORMATION
# ============================================================

def get_model_information():
    """
    Return information about available
    CareerCast models.
    """

    metrics = load_model_metrics()

    available_models = []

    # --------------------------------------------------------
    # Random Forest
    # --------------------------------------------------------

    if os.path.exists(
        os.path.join(
            ADVANCED_MODELS_DIR,
            "random_forest_model.pkl"
        )
    ):

        available_models.append(
            "Random Forest"
        )

    # --------------------------------------------------------
    # XGBoost
    # --------------------------------------------------------

    if os.path.exists(
        os.path.join(
            ADVANCED_MODELS_DIR,
            "xgboost_model.pkl"
        )
    ):

        available_models.append(
            "XGBoost"
        )

    # --------------------------------------------------------
    # Recommended model
    # --------------------------------------------------------

    if "XGBoost" in available_models:

        recommended_model = "XGBoost"

    elif available_models:

        recommended_model = available_models[0]

    else:

        recommended_model = "Not Available"

    return {

        "available_models":
            available_models,

        "recommended_model":
            recommended_model,

        "metrics":
            metrics
    }


# ============================================================
# QUICK PREDICTION HELPER
# ============================================================

def predict(
    resume_text,
    model_name="xgboost",
    top_k=5
):
    """
    Convenience function for Top-K
    career prediction.
    """

    return predict_top_k(
        resume_text=resume_text,
        model_name=model_name,
        top_k=top_k
    )


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [

    "load_model",

    "load_vectorizer",

    "load_legacy_model",

    "load_label_encoder",

    "load_model_metrics",

    "prepare_text",

    "predict_top_k",

    "predict_career",

    "get_prediction_result",

    "get_model_information",

    "predict",

]