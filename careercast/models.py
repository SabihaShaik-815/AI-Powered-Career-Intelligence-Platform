"""
CareerCast Model Utilities

This module provides reusable utilities for:

- Loading trained CareerCast models
- Loading TF-IDF vectorizers
- Loading label encoders
- Loading model metrics
- Predicting career classes
- Calculating prediction confidence
"""

from pathlib import Path
import json
import warnings

warnings.filterwarnings("ignore")


# ============================================================
# PATH CONFIGURATION
# ============================================================

PACKAGE_DIR = Path(__file__).resolve().parent

PROJECT_DIR = PACKAGE_DIR.parent

MODELS_DIR = PROJECT_DIR / "models"

ADVANCED_MODELS_DIR = (
    PROJECT_DIR / "advanced_models"
)


# ============================================================
# MODEL FILES
# ============================================================

ROLE_MODEL_PATH = (
    MODELS_DIR /
    "role_classifier.joblib"
)

ROLE_VECTORIZER_PATH = (
    MODELS_DIR /
    "role_tfidf_vectorizer.joblib"
)

ROLE_CLASSES_PATH = (
    MODELS_DIR /
    "role_classes.json"
)

ROLE_METRICS_PATH = (
    MODELS_DIR /
    "role_metrics.json"
)

RANDOM_FOREST_MODEL_PATH = (
    ADVANCED_MODELS_DIR /
    "random_forest_model.pkl"
)

XGBOOST_MODEL_PATH = (
    ADVANCED_MODELS_DIR /
    "xgboost_model.pkl"
)

LABEL_ENCODER_PATH = (
    ADVANCED_MODELS_DIR /
    "label_encoder.pkl"
)

ADVANCED_METRICS_PATH = (
    ADVANCED_MODELS_DIR /
    "advanced_metrics.json"
)

ADVANCED_VECTORIZER_PATH = (
    ADVANCED_MODELS_DIR /
    "tfidf_vectorizer.joblib"
)


# ============================================================
# JOBLIB IMPORT
# ============================================================

try:

    import joblib

except ImportError:

    joblib = None


# ============================================================
# MODEL LOADING
# ============================================================

def load_joblib_model(path):
    """
    Load a joblib model from disk.

    Parameters
    ----------
    path : Path
        Path to the saved model.

    Returns
    -------
    object or None
        Loaded model.
    """

    if joblib is None:

        raise ImportError(
            "joblib is not installed. "
            "Run: pip install joblib"
        )

    path = Path(path)

    if not path.exists():

        return None

    try:

        return joblib.load(path)

    except Exception as error:

        raise RuntimeError(
            f"Could not load model from "
            f"{path}: {error}"
        )


def load_model(path):
    """
    Generic model loader.

    Supports joblib/pickle files.
    """

    return load_joblib_model(path)


# ============================================================
# LOAD ROLE CLASSIFIER
# ============================================================

def load_role_classifier():
    """
    Load the primary CareerCast role classifier.
    """

    return load_joblib_model(
        ROLE_MODEL_PATH
    )


# ============================================================
# LOAD ROLE VECTORIZER
# ============================================================

def load_role_vectorizer():
    """
    Load the TF-IDF vectorizer used by
    the primary role classifier.
    """

    return load_joblib_model(
        ROLE_VECTORIZER_PATH
    )


# ============================================================
# LOAD RANDOM FOREST
# ============================================================

def load_random_forest():
    """
    Load the trained Random Forest model.
    """

    return load_joblib_model(
        RANDOM_FOREST_MODEL_PATH
    )


# ============================================================
# LOAD XGBOOST
# ============================================================

def load_xgboost():
    """
    Load the trained XGBoost model.
    """

    return load_joblib_model(
        XGBOOST_MODEL_PATH
    )


# ============================================================
# LOAD LABEL ENCODER
# ============================================================

def load_label_encoder():
    """
    Load the label encoder used by the
    advanced models.
    """

    return load_joblib_model(
        LABEL_ENCODER_PATH
    )


# ============================================================
# LOAD ADVANCED VECTORIZER
# ============================================================

def load_advanced_vectorizer():
    """
    Load the TF-IDF vectorizer used by
    the advanced model pipeline.
    """

    return load_joblib_model(
        ADVANCED_VECTORIZER_PATH
    )


# ============================================================
# LOAD JSON FILE
# ============================================================

def load_json(path):
    """
    Load a JSON file safely.

    Parameters
    ----------
    path : Path
        JSON file path.

    Returns
    -------
    dict or list
        Loaded JSON data.
    """

    path = Path(path)

    if not path.exists():

        return {}

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {}


# ============================================================
# LOAD ROLE CLASSES
# ============================================================

def load_role_classes():
    """
    Load career-role class names.

    Supports both a JSON list and a JSON
    object containing a classes field.
    """

    data = load_json(
        ROLE_CLASSES_PATH
    )

    if isinstance(data, list):

        return data

    if isinstance(data, dict):

        classes = (
            data.get("classes")
            or data.get("role_classes")
            or data.get("labels")
        )

        if isinstance(classes, list):

            return classes

    return []


# ============================================================
# LOAD ROLE METRICS
# ============================================================

def load_role_metrics():
    """
    Load primary classifier metrics.
    """

    return load_json(
        ROLE_METRICS_PATH
    )


# ============================================================
# LOAD ADVANCED METRICS
# ============================================================

def load_advanced_metrics():
    """
    Load Random Forest/XGBoost metrics.
    """

    return load_json(
        ADVANCED_METRICS_PATH
    )


# ============================================================
# GET MODEL CLASSES
# ============================================================

def get_model_classes(model):
    """
    Extract class labels from a trained model.

    Returns
    -------
    list
        Model class labels.
    """

    if model is None:

        return []

    classes = getattr(
        model,
        "classes_",
        None
    )

    if classes is None:

        return []

    try:

        return list(classes)

    except Exception:

        return []


# ============================================================
# PREDICTION CONFIDENCE
# ============================================================

def get_prediction_confidence(
    model,
    features
):
    """
    Calculate prediction confidence.

    If the model provides predict_proba(),
    the highest class probability is returned.

    Returns
    -------
    float
        Confidence between 0 and 1.
    """

    if model is None:

        return 0.0

    if not hasattr(
        model,
        "predict_proba"
    ):

        return 0.0

    try:

        probabilities = (
            model.predict_proba(features)
        )

        if probabilities is None:

            return 0.0

        if len(probabilities) == 0:

            return 0.0

        first_row = probabilities[0]

        if len(first_row) == 0:

            return 0.0

        return float(
            max(first_row)
        )

    except Exception:

        return 0.0


# ============================================================
# PREDICT CLASS
# ============================================================

def predict_class(
    model,
    features
):
    """
    Predict a single career class.

    Returns
    -------
    object or None
        Predicted class.
    """

    if model is None:

        return None

    try:

        prediction = model.predict(
            features
        )

        if prediction is None:

            return None

        if len(prediction) == 0:

            return None

        return prediction[0]

    except Exception:

        return None


# ============================================================
# PREDICT WITH CONFIDENCE
# ============================================================

def predict_with_confidence(
    model,
    features
):
    """
    Predict a class and calculate its confidence.

    Returns
    -------
    dict
        {
            "prediction": ...,
            "confidence": ...
        }
    """

    prediction = predict_class(
        model,
        features
    )

    confidence = (
        get_prediction_confidence(
            model,
            features
        )
    )

    return {
        "prediction": prediction,
        "confidence": confidence
    }


# ============================================================
# GET MODEL INFORMATION
# ============================================================

def get_model_info(model):
    """
    Return basic information about a model.
    """

    if model is None:

        return {
            "available": False,
            "model_type": None,
            "classes": [],
            "class_count": 0
        }

    classes = (
        get_model_classes(model)
    )

    return {
        "available": True,
        "model_type": type(model).__name__,
        "classes": classes,
        "class_count": len(classes)
    }


# ============================================================
# MODEL AVAILABILITY
# ============================================================

def get_available_models():
    """
    Check which CareerCast models are
    currently available.
    """

    return {
        "role_classifier":
            file_exists(
                ROLE_MODEL_PATH
            ),

        "role_vectorizer":
            file_exists(
                ROLE_VECTORIZER_PATH
            ),

        "random_forest":
            file_exists(
                RANDOM_FOREST_MODEL_PATH
            ),

        "xgboost":
            file_exists(
                XGBOOST_MODEL_PATH
            ),

        "label_encoder":
            file_exists(
                LABEL_ENCODER_PATH
            ),

        "advanced_vectorizer":
            file_exists(
                ADVANCED_VECTORIZER_PATH
            )
    }


# ============================================================
# FILE EXISTS HELPER
# ============================================================

def file_exists(path):
    """
    Check whether a file exists.
    """

    try:

        return (
            Path(path).exists()
            and Path(path).is_file()
        )

    except Exception:

        return False


# ============================================================
# MODEL SUMMARY
# ============================================================

def get_model_summary():
    """
    Return a complete summary of
    available CareerCast models.
    """

    available = (
        get_available_models()
    )

    role_metrics = (
        load_role_metrics()
    )

    advanced_metrics = (
        load_advanced_metrics()
    )

    return {

        "models": available,

        "role_metrics":
            role_metrics,

        "advanced_metrics":
            advanced_metrics,

        "paths": {

            "role_classifier":
                str(
                    ROLE_MODEL_PATH
                ),

            "role_vectorizer":
                str(
                    ROLE_VECTORIZER_PATH
                ),

            "random_forest":
                str(
                    RANDOM_FOREST_MODEL_PATH
                ),

            "xgboost":
                str(
                    XGBOOST_MODEL_PATH
                ),

            "label_encoder":
                str(
                    LABEL_ENCODER_PATH
                ),

            "advanced_vectorizer":
                str(
                    ADVANCED_VECTORIZER_PATH
                )
        }
    }


# ============================================================
# NORMALIZE ACCURACY
# ============================================================

def normalize_accuracy(value):
    """
    Normalize accuracy to a percentage.

    Examples
    --------
    0.75 -> 75.0
    75 -> 75.0
    """

    try:

        value = float(value)

    except (
        ValueError,
        TypeError
    ):

        return 0.0

    if value <= 1:

        return value * 100

    return value


# ============================================================
# EXTRACT ACCURACY
# ============================================================

def extract_accuracy(metrics):
    """
    Extract accuracy from a metric dictionary.

    Supports common metric names used
    in CareerCast model files.
    """

    if not isinstance(
        metrics,
        dict
    ):

        return 0.0

    possible_keys = [

        "accuracy",

        "test_accuracy",

        "validation_accuracy",

        "val_accuracy",

        "score",

        "test_score"

    ]

    for key in possible_keys:

        value = metrics.get(
            key
        )

        if value is not None:

            return normalize_accuracy(
                value
            )

    return 0.0


# ============================================================
# GET MODEL ACCURACIES
# ============================================================

def get_model_accuracies():
    """
    Return available model accuracies
    in percentage form.
    """

    role_metrics = (
        load_role_metrics()
    )

    advanced_metrics = (
        load_advanced_metrics()
    )

    accuracies = {

        "Logistic Regression":
            extract_accuracy(
                role_metrics
            ),

        "Random Forest":
            0.0,

        "XGBoost":
            0.0

    }

    if isinstance(
        advanced_metrics,
        dict
    ):

        rf_metrics = (
            advanced_metrics.get(
                "random_forest",
                {}
            )
        )

        xgb_metrics = (
            advanced_metrics.get(
                "xgboost",
                {}
            )
        )

        accuracies[
            "Random Forest"
        ] = extract_accuracy(
            rf_metrics
        )

        accuracies[
            "XGBoost"
        ] = extract_accuracy(
            xgb_metrics
        )

    return accuracies


# ============================================================
# BEST MODEL
# ============================================================

def get_best_model():
    """
    Determine the best available model
    using recorded accuracy.

    Returns
    -------
    dict
        Model name and accuracy.
    """

    accuracies = (
        get_model_accuracies()
    )

    if not accuracies:

        return {
            "model": None,
            "accuracy": 0.0
        }

    best_model = max(
        accuracies,
        key=accuracies.get
    )

    return {

        "model":
            best_model,

        "accuracy":
            accuracies[best_model]

    }


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [

    "load_model",

    "load_role_classifier",

    "load_role_vectorizer",

    "load_random_forest",

    "load_xgboost",

    "load_label_encoder",

    "load_advanced_vectorizer",

    "load_role_classes",

    "load_role_metrics",

    "load_advanced_metrics",

    "get_prediction_confidence",

    "predict_class",

    "predict_with_confidence",

    "get_model_info",

    "get_available_models",

    "get_model_summary",

    "get_model_accuracies",

    "get_best_model",

]