"""
CareerCast Recommendation Tests

Tests for:
- Confidence level calculation
- Recommendation generation
- Top-K career recommendations
- Best career recommendation
- Recommendation result formatting
"""

from careercast import recommender


# ============================================================
# SAMPLE RESUME
# ============================================================

SAMPLE_RESUME = """
Python Developer with experience in Python, SQL, Flask,
Machine Learning, Data Analysis and Git.
Bachelor of Technology in Computer Science.
"""


# ============================================================
# SAMPLE PREDICTIONS
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
# MOCK PREDICTION FUNCTION
# ============================================================

def fake_predictions(
    resume_text=None,
    text=None,
    model_name="xgboost",
    top_k=5
):
    """
    Mock predict_top_k function.

    Accepts resume_text because recommender.py
    calls predict_top_k using the resume_text keyword.
    """

    try:
        top_k = int(top_k)
    except (ValueError, TypeError):
        top_k = 5

    if top_k < 1:
        top_k = 1

    return SAMPLE_PREDICTIONS[:top_k]


# ============================================================
# TEST CONFIDENCE LEVEL - HIGH
# ============================================================

def test_get_confidence_level_high():

    result = recommender.get_confidence_level(
        0.85
    )

    assert isinstance(
        result,
        str
    )

    assert len(result) > 0


# ============================================================
# TEST CONFIDENCE LEVEL - MEDIUM
# ============================================================

def test_get_confidence_level_medium():

    result = recommender.get_confidence_level(
        0.60
    )

    assert isinstance(
        result,
        str
    )

    assert len(result) > 0


# ============================================================
# TEST CONFIDENCE LEVEL - LOW
# ============================================================

def test_get_confidence_level_low():

    result = recommender.get_confidence_level(
        0.30
    )

    assert isinstance(
        result,
        str
    )

    assert len(result) > 0


# ============================================================
# TEST ROLE DESCRIPTIONS
# ============================================================

def test_role_descriptions_exist():

    assert isinstance(
        recommender.ROLE_DESCRIPTIONS,
        dict
    )

    assert len(
        recommender.ROLE_DESCRIPTIONS
    ) > 0


# ============================================================
# TEST EXPLANATION GENERATION
# ============================================================

def test_generate_explanation():

    result = recommender.generate_explanation(
        "Data Scientist",
        0.85
    )

    assert isinstance(
        result,
        str
    )

    assert len(result) > 0


# ============================================================
# TEST CAREER RECOMMENDATIONS
# ============================================================

def test_get_career_recommendations(
    monkeypatch
):

    monkeypatch.setattr(
        recommender,
        "predict_top_k",
        fake_predictions
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
# TEST RECOMMENDATION STRUCTURE
# ============================================================

def test_recommendation_structure(
    monkeypatch
):

    monkeypatch.setattr(
        recommender,
        "predict_top_k",
        fake_predictions
    )

    results = recommender.get_career_recommendations(
        SAMPLE_RESUME,
        top_k=3
    )

    assert len(results) > 0

    first = results[0]

    assert isinstance(
        first,
        dict
    )

    assert "role" in first

    assert "confidence" in first

    assert "rank" in first

    assert "confidence_level" in first

    assert "description" in first


# ============================================================
# TEST TOP-K LIMIT
# ============================================================

def test_recommendation_top_k(
    monkeypatch
):

    monkeypatch.setattr(
        recommender,
        "predict_top_k",
        fake_predictions
    )

    results = recommender.get_career_recommendations(
        SAMPLE_RESUME,
        top_k=2
    )

    assert len(results) <= 2


# ============================================================
# TEST BEST RECOMMENDATION
# ============================================================

def test_get_best_recommendation(
    monkeypatch
):

    monkeypatch.setattr(
        recommender,
        "predict_top_k",
        fake_predictions
    )

    result = recommender.get_best_recommendation(
        SAMPLE_RESUME
    )

    assert result is not None

    assert isinstance(
        result,
        dict
    )

    assert "role" in result

    assert "confidence" in result


# ============================================================
# TEST RECOMMENDATION RESULT
# ============================================================

def test_get_recommendation_result(
    monkeypatch
):

    monkeypatch.setattr(
        recommender,
        "predict_top_k",
        fake_predictions
    )

    result = recommender.get_recommendation_result(
        SAMPLE_RESUME
    )

    assert isinstance(
        result,
        dict
    )


# ============================================================
# TEST FORMAT RECOMMENDATIONS
# ============================================================

def test_format_recommendations():

    recommendations = [
        {
            "rank": 1,
            "role": "Data Scientist",
            "confidence": 85.0,
            "confidence_level": "High",
            "description": (
                "Analyzes data and builds machine learning models."
            )
        },
        {
            "rank": 2,
            "role": "Data Analyst",
            "confidence": 70.0,
            "confidence_level": "High",
            "description": (
                "Analyzes data and creates business insights."
            )
        },
        {
            "rank": 3,
            "role": "Software Engineer",
            "confidence": 55.0,
            "confidence_level": "Medium",
            "description": (
                "Designs and develops software applications."
            )
        }
    ]

    result = recommender.format_recommendations(
        recommendations
    )

    assert isinstance(
        result,
        str
    )

    assert "Data Scientist" in result

    assert "Data Analyst" in result

    assert "Software Engineer" in result

    assert "Confidence" in result

    assert "Confidence Level" in result

    assert "Description" in result


# ============================================================
# TEST EMPTY RECOMMENDATIONS
# ============================================================

def test_empty_recommendations():

    result = recommender.format_recommendations(
        []
    )

    assert isinstance(
        result,
        str
    )

    assert "No career recommendations available." in result


# ============================================================
# TEST EMPTY RESUME
# ============================================================

def test_empty_resume(
    monkeypatch
):

    monkeypatch.setattr(
        recommender,
        "predict_top_k",
        fake_predictions
    )

    result = recommender.get_career_recommendations(
        "",
        top_k=5
    )

    assert isinstance(
        result,
        list
    )


# ============================================================
# TEST RECOMMENDATION ORDER
# ============================================================

def test_recommendation_order(
    monkeypatch
):

    monkeypatch.setattr(
        recommender,
        "predict_top_k",
        fake_predictions
    )

    results = recommender.get_career_recommendations(
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
# TEST RANDOM FOREST RECOMMENDATION
# ============================================================

def test_random_forest_recommendation(
    monkeypatch
):

    monkeypatch.setattr(
        recommender,
        "predict_top_k",
        fake_predictions
    )

    results = recommender.get_career_recommendations(
        SAMPLE_RESUME,
        model_name="random_forest",
        top_k=3
    )

    assert isinstance(
        results,
        list
    )

    assert len(results) == 3


# ============================================================
# TEST RECOMMENDATION RANKS
# ============================================================

def test_format_recommendations():

    recommendations = [
        {
            "rank": 1,
            "role": "Data Scientist",
            "confidence": 85.0,
            "confidence_level": "High",
            "description": (
                "Analyzes data and builds machine learning models."
            ),
            "explanation": (
                "Strong match based on Python, SQL, "
                "Machine Learning and Data Analysis skills."
            )
        },
        {
            "rank": 2,
            "role": "Data Analyst",
            "confidence": 70.0,
            "confidence_level": "High",
            "description": (
                "Analyzes data and creates business insights."
            ),
            "explanation": (
                "Good match based on SQL, Python "
                "and Data Analysis skills."
            )
        },
        {
            "rank": 3,
            "role": "Software Engineer",
            "confidence": 55.0,
            "confidence_level": "Medium",
            "description": (
                "Designs and develops software applications."
            ),
            "explanation": (
                "Moderate match based on Python, Flask "
                "and software development experience."
            )
        }
    ]

    result = recommender.format_recommendations(
        recommendations
    )

    assert isinstance(
        result,
        str
    )

    assert "Data Scientist" in result

    assert "Data Analyst" in result

    assert "Software Engineer" in result

    assert "Confidence" in result

    assert "Confidence Level" in result

    assert "Description" in result

    assert "Explanation" in result