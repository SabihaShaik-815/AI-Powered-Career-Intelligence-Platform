"""
CareerCast Career Recommendation Module

This module provides:

- Top-K career recommendations
- Career ranking
- Confidence scores
- Recommendation explanations
"""

from careercast.predictor import predict_top_k


# ============================================================
# ROLE DESCRIPTIONS
# ============================================================

ROLE_DESCRIPTIONS = {

    "Software Engineer":
        "Designs, develops, tests and maintains software applications.",

    "Data Scientist":
        "Analyzes data and builds machine learning models to solve problems.",

    "Machine Learning Engineer":
        "Develops and deploys machine learning systems and models.",

    "Data Analyst":
        "Analyzes data and creates insights to support business decisions.",

    "AI Engineer":
        "Builds artificial intelligence applications and intelligent systems."
}


# ============================================================
# CONFIDENCE LEVEL
# ============================================================

def get_confidence_level(confidence_percentage):
    """
    Convert confidence percentage into
    a readable confidence level.
    """

    try:
        confidence_percentage = float(
            confidence_percentage
        )
    except (
        ValueError,
        TypeError
    ):
        confidence_percentage = 0

    if confidence_percentage >= 80:
        return "Very High"

    elif confidence_percentage >= 60:
        return "High"

    elif confidence_percentage >= 40:
        return "Medium"

    elif confidence_percentage >= 20:
        return "Low"

    return "Very Low"


# ============================================================
# RECOMMENDATION EXPLANATION
# ============================================================

def generate_explanation(role, confidence):
    """
    Generate an explanation for the
    recommended career.
    """

    description = ROLE_DESCRIPTIONS.get(

        role,

        f"{role} is a suitable career recommendation "
        "based on the skills and information found in your resume."
    )

    confidence_level = get_confidence_level(
        confidence
    )

    return (
        f"{role} is recommended based on your resume. "
        f"The prediction confidence is {confidence}% "
        f"({confidence_level} confidence). "
        f"{description}"
    )


# ============================================================
# TOP-K CAREER RECOMMENDATIONS
# ============================================================

def get_career_recommendations(
    resume_text,
    top_k=5,
    model_name="xgboost"
):
    """
    Generate Top-K career recommendations.

    Parameters
    ----------
    resume_text : str
        Resume content.

    top_k : int
        Number of recommendations.

    model_name : str
        ML model to use.

    Returns
    -------
    list
        Ranked career recommendations.
    """

    try:
        top_k = int(top_k)
    except (
        ValueError,
        TypeError
    ):
        top_k = 5

    if top_k < 1:
        top_k = 1

    predictions = predict_top_k(

        resume_text=resume_text,

        model_name=model_name,

        top_k=top_k
    )

    recommendations = []


    for prediction in predictions:

        role = prediction.get(
            "role",
            "Unknown"
        )

        confidence = prediction.get(
            "confidence_percentage",
            0
        )

        rank = prediction.get(
            "rank",
            0
        )


        recommendation = {

            "rank":
                rank,

            "role":
                role,

            "confidence":
                confidence,

            "confidence_level":
                get_confidence_level(
                    confidence
                ),

            "description":
                ROLE_DESCRIPTIONS.get(

                    role,

                    "Career recommendation generated "
                    "from your resume analysis."
                ),

            "explanation":
                generate_explanation(

                    role,

                    confidence
                )
        }


        recommendations.append(
            recommendation
        )


    return recommendations


# ============================================================
# BEST CAREER RECOMMENDATION
# ============================================================

def get_best_recommendation(
    resume_text,
    model_name="xgboost"
):
    """
    Get the best career recommendation.
    """

    recommendations = get_career_recommendations(

        resume_text=resume_text,

        top_k=1,

        model_name=model_name
    )


    if not recommendations:

        return {

            "success":
                False,

            "message":
                "Could not generate a career recommendation."
        }


    best = recommendations[0]


    return {

        "success":
            True,

        "rank":
            best["rank"],

        "role":
            best["role"],

        "confidence":
            best["confidence"],

        "confidence_level":
            best["confidence_level"],

        "description":
            best["description"],

        "explanation":
            best["explanation"]
    }


# ============================================================
# COMPLETE RECOMMENDATION RESULT
# ============================================================

def get_recommendation_result(
    resume_text,
    top_k=5,
    model_name="xgboost"
):
    """
    Generate the complete recommendation result.
    """

    recommendations = get_career_recommendations(

        resume_text=resume_text,

        top_k=top_k,

        model_name=model_name
    )


    if not recommendations:

        return {

            "success":
                False,

            "top_k":
                top_k,

            "best_role":
                "Not Available",

            "recommendations":
                []
        }


    best_recommendation = recommendations[0]


    return {

        "success":
            True,

        "top_k":
            len(recommendations),

        "model":
            model_name,

        "best_role":
            best_recommendation["role"],

        "best_confidence":
            best_recommendation["confidence"],

        "recommendations":
            recommendations
    }


# ============================================================
# DISPLAY RECOMMENDATIONS
# ============================================================

def format_recommendations(
    recommendations
):
    """
    Format recommendations for CLI display.
    """

    if not recommendations:

        return (
            "No career recommendations available."
        )


    output = []

    output.append(
        "\n========== CAREER RECOMMENDATIONS ==========\n"
    )


    for item in recommendations:

        output.append(
            f"Rank #{item['rank']}"
        )

        output.append(
            f"Career Role: {item['role']}"
        )

        output.append(
            f"Confidence: {item['confidence']}%"
        )

        output.append(
            f"Confidence Level: "
            f"{item['confidence_level']}"
        )

        output.append(
            f"Description: "
            f"{item['description']}"
        )

        output.append(
            f"Explanation: "
            f"{item['explanation']}"
        )

        output.append(
            "-" * 45
        )


    return "\n".join(
        output
    )


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [

    "ROLE_DESCRIPTIONS",

    "get_confidence_level",

    "generate_explanation",

    "get_career_recommendations",

    "get_best_recommendation",

    "get_recommendation_result",

    "format_recommendations",

]