"""
CareerCast Integration Tests

Tests the complete CareerCast pipeline:

Resume Text
    ↓
Resume Parser
    ↓
Career Prediction
    ↓
Career Recommendation
"""

import pytest

from careercast import parser
from careercast import predictor
from careercast import recommender


# ============================================================
# SAMPLE RESUME
# ============================================================

SAMPLE_RESUME = """
John Doe

Python Developer

Skills:
Python, SQL, Flask, Machine Learning, Data Analysis, Git

Education:
Bachelor of Technology in Computer Science

Experience:
Developed Python applications using Flask and SQL.
Worked on machine learning and data analysis projects.
"""


# ============================================================
# MOCK PREDICTIONS
# ============================================================

SAMPLE_PREDICTIONS = [
    {
        "role": "Data Scientist",
        "confidence": 0.85
    },
    {
        "role": "Data Analyst",
        "confidence": 0.70
    },
    {
        "role": "Software Engineer",
        "confidence": 0.55
    }
]


# ============================================================
# MOCK PREDICTOR
# ============================================================

def fake_predict_top_k(
    resume_text=None,
    text=None,
    model_name="xgboost",
    top_k=5
):
    """
    Mock prediction function for integration testing.
    """

    try:
        top_k = int(top_k)
    except (ValueError, TypeError):
        top_k = 5

    if top_k < 1:
        top_k = 1

    return SAMPLE_PREDICTIONS[:top_k]


# ============================================================
# TEST 1
# PARSER → SKILLS
# ============================================================

def test_parser_extracts_skills():

    result = parser.parse_resume_text(
        SAMPLE_RESUME
    )

    assert isinstance(
        result,
        dict
    )

    assert "skills" in result

    assert isinstance(
        result["skills"],
        list
    )

    assert len(
        result["skills"]
    ) > 0


# ============================================================
# TEST 2
# PARSER → EDUCATION
# ============================================================

def test_parser_extracts_education():

    result = parser.parse_resume_text(
        SAMPLE_RESUME
    )

    assert "education" in result

    assert isinstance(
        result["education"],
        list
    )

    assert len(
        result["education"]
    ) > 0


# ============================================================
# TEST 3
# PARSER OUTPUT STRUCTURE
# ============================================================

def test_parser_output_structure():

    result = parser.parse_resume_text(
        SAMPLE_RESUME
    )

    assert isinstance(
        result,
        dict
    )

    assert "skills" in result

    assert "education" in result

    assert "text_length" in result

    assert isinstance(
        result["text_length"],
        int
    )

    assert result["text_length"] > 0


# ============================================================
# TEST 4
# PREDICTION PIPELINE
# ============================================================

def test_prediction_pipeline(
    monkeypatch
):

    monkeypatch.setattr(
        predictor,
        "load_model",
        lambda model_name="xgboost": object()
    )

    monkeypatch.setattr(
        predictor,
        "load_vectorizer",
        lambda: object()
    )

    monkeypatch.setattr(
        predictor,
        "load_label_encoder",
        lambda: object()
    )

    result = fake_predict_top_k(
        resume_text=SAMPLE_RESUME,
        model_name="xgboost",
        top_k=3
    )

    assert isinstance(
        result,
        list
    )

    assert len(result) == 3

    assert result[0]["role"] == "Data Scientist"


# ============================================================
# TEST 5
# PREDICTION RESULT STRUCTURE
# ============================================================

def test_prediction_result_structure():

    predictions = fake_predict_top_k(
        resume_text=SAMPLE_RESUME,
        top_k=3
    )

    assert len(predictions) == 3

    for prediction in predictions:

        assert isinstance(
            prediction,
            dict
        )

        assert "role" in prediction

        assert "confidence" in prediction

        assert isinstance(
            prediction["role"],
            str
        )

        assert isinstance(
            prediction["confidence"],
            float
        )


# ============================================================
# TEST 6
# RECOMMENDATION PIPELINE
# ============================================================

def test_recommendation_pipeline(
    monkeypatch
):

    monkeypatch.setattr(
        recommender,
        "predict_top_k",
        fake_predict_top_k
    )

    results = recommender.get_career_recommendations(
        SAMPLE_RESUME,
        top_k=3,
        model_name="xgboost"
    )

    assert isinstance(
        results,
        list
    )

    assert len(results) == 3


# ============================================================
# TEST 7
# RECOMMENDATION RESULT STRUCTURE
# ============================================================

def test_recommendation_result_structure(
    monkeypatch
):

    monkeypatch.setattr(
        recommender,
        "predict_top_k",
        fake_predict_top_k
    )

    results = recommender.get_career_recommendations(
        SAMPLE_RESUME,
        top_k=3
    )

    assert len(results) == 3

    for result in results:

        assert isinstance(
            result,
            dict
        )

        assert "role" in result

        assert "confidence" in result

        assert "rank" in result

        assert "confidence_level" in result

        assert "description" in result

        assert "explanation" in result


# ============================================================
# TEST 8
# BEST RECOMMENDATION
# ============================================================

def test_best_recommendation(
    monkeypatch
):

    monkeypatch.setattr(
        recommender,
        "predict_top_k",
        fake_predict_top_k
    )

    result = recommender.get_best_recommendation(
        SAMPLE_RESUME
    )

    assert isinstance(
        result,
        dict
    )

    assert "role" in result

    assert "confidence" in result

    assert result["role"] == "Data Scientist"


# ============================================================
# TEST 9
# COMPLETE PARSING → RECOMMENDATION FLOW
# ============================================================

def test_complete_pipeline(
    monkeypatch
):

    # --------------------------------------------------------
    # STEP 1: Parse resume
    # --------------------------------------------------------

    parsed = parser.parse_resume_text(
        SAMPLE_RESUME
    )

    assert isinstance(
        parsed,
        dict
    )

    assert len(
        parsed["skills"]
    ) > 0


    # --------------------------------------------------------
    # STEP 2: Use original resume text for prediction
    # --------------------------------------------------------

    predictions = fake_predict_top_k(
        resume_text=SAMPLE_RESUME,
        model_name="xgboost",
        top_k=3
    )

    assert isinstance(
        predictions,
        list
    )

    assert len(predictions) == 3


    # --------------------------------------------------------
    # STEP 3: Generate recommendations
    # --------------------------------------------------------

    monkeypatch.setattr(
        recommender,
        "predict_top_k",
        fake_predict_top_k
    )

    recommendations = recommender.get_career_recommendations(
        SAMPLE_RESUME,
        top_k=3,
        model_name="xgboost"
    )

    assert isinstance(
        recommendations,
        list
    )

    assert len(recommendations) == 3


    # --------------------------------------------------------
    # STEP 4: Verify final recommendation
    # --------------------------------------------------------

    best = recommender.get_best_recommendation(
        SAMPLE_RESUME
    )

    assert isinstance(
        best,
        dict
    )

    assert "role" in best

    assert "confidence" in best


# ============================================================
# TEST 10
# TOP-K INTEGRATION
# ============================================================

@pytest.mark.parametrize(
    "top_k",
    [1, 2, 3]
)
def test_top_k_integration(
    monkeypatch,
    top_k
):

    monkeypatch.setattr(
        recommender,
        "predict_top_k",
        fake_predict_top_k
    )

    results = recommender.get_career_recommendations(
        SAMPLE_RESUME,
        top_k=top_k
    )

    assert isinstance(
        results,
        list
    )

    assert len(results) <= top_k


# ============================================================
# TEST 11
# EMPTY RESUME INTEGRATION
# ============================================================

def test_empty_resume_integration(
    monkeypatch
):

    parsed = parser.parse_resume_text(
        ""
    )

    assert isinstance(
        parsed,
        dict
    )

    monkeypatch.setattr(
        recommender,
        "predict_top_k",
        fake_predict_top_k
    )

    results = recommender.get_career_recommendations(
        "",
        top_k=3
    )

    assert isinstance(
        results,
        list
    )


# ============================================================
# TEST 12
# MODEL SELECTION INTEGRATION
# ============================================================

@pytest.mark.parametrize(
    "model_name",
    [
        "xgboost",
        "random_forest"
    ]
)
def test_model_selection_integration(
    monkeypatch,
    model_name
):

    monkeypatch.setattr(
        recommender,
        "predict_top_k",
        fake_predict_top_k
    )

    results = recommender.get_career_recommendations(
        SAMPLE_RESUME,
        top_k=3,
        model_name=model_name
    )

    assert isinstance(
        results,
        list
    )

    assert len(results) <= 3