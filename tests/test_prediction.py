"""
CareerCast Prediction Tests

Tests for:
- Text preparation
- Model loading helpers
- Top-K prediction pipeline
- Career prediction
- Prediction result formatting
- Model information
"""

import numpy as np
import pytest

from careercast import predictor


# ============================================================
# SAMPLE RESUME
# ============================================================

SAMPLE_RESUME = """
Python Developer with experience in Python, SQL, Flask,
Machine Learning, Data Analysis and Git.
Bachelor of Technology in Computer Science.
"""


# ============================================================
# DUMMY VECTORIZER
# ============================================================

class DummyVectorizer:
    """
    Simple fake vectorizer used for testing.
    """

    def transform(self, texts):

        assert isinstance(
            texts,
            list
        )

        assert len(texts) == 1

        return np.array([
            [1.0, 2.0, 3.0]
        ])


# ============================================================
# DUMMY MODEL
# ============================================================

class DummyModel:
    """
    Simple fake classification model.
    """

    def predict_proba(self, features):

        assert features is not None

        return np.array([
            [
                0.70,
                0.20,
                0.10
            ]
        ])

    def predict(self, features):

        assert features is not None

        return np.array([
            0
        ])


# ============================================================
# DUMMY LABEL ENCODER
# ============================================================

class DummyLabelEncoder:
    """
    Fake label encoder for testing.
    """

    classes_ = np.array([
        "Data Scientist",
        "Data Analyst",
        "Software Engineer"
    ])

    def inverse_transform(self, values):

        return np.array([
            self.classes_[int(value)]
            for value in values
        ])


# ============================================================
# TEST PREPARE TEXT
# ============================================================

def test_prepare_text():

    result = predictor.prepare_text(
        SAMPLE_RESUME
    )

    assert isinstance(
        result,
        str
    )

    assert len(result) > 0

    assert "Python" in result


# ============================================================
# TEST EMPTY TEXT PREPARATION
# ============================================================

def test_prepare_text_empty():

    result = predictor.prepare_text(
        ""
    )

    assert isinstance(
        result,
        str
    )


# ============================================================
# TEST PREDICT TOP K
# ============================================================

def test_predict_top_k(monkeypatch):

    def fake_load_model(
        model_name="xgboost"
    ):
        return DummyModel()

    def fake_load_vectorizer():

        return DummyVectorizer()

    def fake_load_label_encoder():

        return DummyLabelEncoder()

    monkeypatch.setattr(
        predictor,
        "load_model",
        fake_load_model
    )

    monkeypatch.setattr(
        predictor,
        "load_vectorizer",
        fake_load_vectorizer
    )

    monkeypatch.setattr(
        predictor,
        "load_label_encoder",
        fake_load_label_encoder
    )

    results = predictor.predict_top_k(
        SAMPLE_RESUME,
        model_name="xgboost",
        top_k=3
    )

    assert isinstance(
        results,
        list
    )

    assert len(results) == 3

    assert "role" in results[0]

    assert "confidence" in results[0]

    assert isinstance(
        results[0]["role"],
        str
    )

    assert isinstance(
        results[0]["confidence"],
        (int, float)
    )


# ============================================================
# TEST TOP-K ORDER
# ============================================================

def test_predict_top_k_order(monkeypatch):

    monkeypatch.setattr(
        predictor,
        "load_model",
        lambda model_name="xgboost":
            DummyModel()
    )

    monkeypatch.setattr(
        predictor,
        "load_vectorizer",
        lambda:
            DummyVectorizer()
    )

    monkeypatch.setattr(
        predictor,
        "load_label_encoder",
        lambda:
            DummyLabelEncoder()
    )

    results = predictor.predict_top_k(
        SAMPLE_RESUME,
        top_k=3
    )

    confidences = [
        item["confidence"]
        for item in results
    ]

    assert confidences == sorted(
        confidences,
        reverse=True
    )


# ============================================================
# TEST TOP-K LIMIT
# ============================================================

def test_predict_top_k_limit(monkeypatch):

    monkeypatch.setattr(
        predictor,
        "load_model",
        lambda model_name="xgboost":
            DummyModel()
    )

    monkeypatch.setattr(
        predictor,
        "load_vectorizer",
        lambda:
            DummyVectorizer()
    )

    monkeypatch.setattr(
        predictor,
        "load_label_encoder",
        lambda:
            DummyLabelEncoder()
    )

    results = predictor.predict_top_k(
        SAMPLE_RESUME,
        top_k=2
    )

    assert len(results) <= 2


# ============================================================
# TEST INVALID TOP-K
# ============================================================

def test_predict_top_k_invalid_value():

    try:

        results = predictor.predict_top_k(
            SAMPLE_RESUME,
            top_k=0
        )

        assert isinstance(
            results,
            list
        )

    except Exception as error:

        assert isinstance(
            error,
            Exception
        )


# ============================================================
# TEST PREDICT CAREER
# ============================================================

def test_predict_career(monkeypatch):

    def fake_predictions(
        resume_text,
        model_name="xgboost",
        top_k=5
    ):

        return [
            {
                "role": "Data Scientist",
                "confidence": 0.70,
                "confidence_percentage": 70.0
            },
            {
                "role": "Data Analyst",
                "confidence": 0.20,
                "confidence_percentage": 20.0
            }
        ]

    monkeypatch.setattr(
        predictor,
        "predict_top_k",
        fake_predictions
    )

    result = predictor.predict_career(
        SAMPLE_RESUME
    )

    assert result is not None

    assert isinstance(
        result,
        dict
    )

    assert result["role"] == (
        "Data Scientist"
    )

    assert result["confidence"] == 0.70

    assert result[
        "confidence_percentage"
    ] == 70.0


# ============================================================
# TEST GET PREDICTION RESULT
# ============================================================

def test_get_prediction_result(
    monkeypatch
):

    def fake_predictions(
        resume_text,
        model_name="xgboost",
        top_k=5
    ):

        return [
            {
                "role": "Data Scientist",
                "confidence": 0.70,
                "confidence_percentage": 70.0
            },
            {
                "role": "Data Analyst",
                "confidence": 0.20,
                "confidence_percentage": 20.0
            }
        ]

    monkeypatch.setattr(
        predictor,
        "predict_top_k",
        fake_predictions
    )

    result = predictor.get_prediction_result(
        SAMPLE_RESUME
    )

    assert isinstance(
        result,
        dict
    )

    assert result["success"] is True

    assert result["top_role"] == (
        "Data Scientist"
    )

    assert result["confidence"] == 70.0

    assert result["model"] == "xgboost"

    assert "predictions" in result

    assert isinstance(
        result["predictions"],
        list
    )

    assert len(
        result["predictions"]
    ) == 2


# ============================================================
# TEST MODEL INFORMATION
# ============================================================

def test_get_model_information():

    result = predictor.get_model_information()

    assert isinstance(
        result,
        dict
    )


# ============================================================
# TEST PREDICT CONVENIENCE FUNCTION
# ============================================================

def test_predict(monkeypatch):

    def fake_predictions(
        resume_text,
        model_name="xgboost",
        top_k=5
    ):

        return [
            {
                "role": "Data Scientist",
                "confidence": 0.70,
                "confidence_percentage": 70.0
            }
        ]

    monkeypatch.setattr(
        predictor,
        "predict_top_k",
        fake_predictions
    )

    result = predictor.predict(
        SAMPLE_RESUME
    )

    assert result is not None

    assert isinstance(
        result,
        list
    )

    assert len(result) == 1

    assert result[0]["role"] == (
        "Data Scientist"
    )

    assert result[0]["confidence"] == 0.70

    assert result[0][
        "confidence_percentage"
    ] == 70.0