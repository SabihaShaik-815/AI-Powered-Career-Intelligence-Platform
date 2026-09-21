"""
CareerCast Model Evaluator

This module evaluates career prediction models
using the metrics module.
"""

from evaluation.metrics import (
    calculate_all_metrics,
    get_classification_report,
    print_metrics
)


# ============================================================
# EVALUATE MODEL
# ============================================================

def evaluate_model(
    y_true,
    y_pred,
    model_name="Career Prediction Model"
):
    """
    Evaluate a career prediction model.
    """

    metrics = calculate_all_metrics(
        y_true,
        y_pred
    )

    report = get_classification_report(
        y_true,
        y_pred
    )

    result = {

        "model_name": model_name,

        "metrics": metrics,

        "classification_report": report
    }

    return result


# ============================================================
# DISPLAY EVALUATION
# ============================================================

def display_evaluation(result):
    """
    Display model evaluation results.
    """

    print("\n==========================================")

    print("     CAREERCAST MODEL EVALUATION")

    print("==========================================")

    print(
        "Model:",
        result["model_name"]
    )

    print_metrics(
        result["metrics"]
    )


# ============================================================
# COMPARE MODELS
# ============================================================

def compare_models(model_results):
    """
    Compare multiple career prediction models.

    Example:

    model_results = {
        "Logistic Regression": {...},
        "Random Forest": {...},
        "XGBoost": {...}
    }
    """

    comparison = []

    for model_name, result in model_results.items():

        metrics = result.get(
            "metrics",
            {}
        )

        comparison.append({

            "model": model_name,

            "accuracy":
                metrics.get(
                    "accuracy",
                    0
                ),

            "precision":
                metrics.get(
                    "precision",
                    0
                ),

            "recall":
                metrics.get(
                    "recall",
                    0
                ),

            "f1_score":
                metrics.get(
                    "f1_score",
                    0
                )
        })


    comparison = sorted(

        comparison,

        key=lambda x: x["accuracy"],

        reverse=True
    )


    return comparison


# ============================================================
# GET BEST MODEL
# ============================================================

def get_best_model(comparison):

    """
    Get the model with the highest accuracy.
    """

    if not comparison:

        return None


    return comparison[0]


# ============================================================
# TEST EVALUATOR
# ============================================================

if __name__ == "__main__":

    # Sample actual roles

    y_true = [

        "Software Engineer",

        "Data Scientist",

        "Data Analyst",

        "AI Engineer",

        "Software Engineer",

        "Machine Learning Engineer"
    ]


    # Sample predictions

    y_pred = [

        "Software Engineer",

        "Data Scientist",

        "Data Analyst",

        "Machine Learning Engineer",

        "Software Engineer",

        "Machine Learning Engineer"
    ]


    result = evaluate_model(

        y_true,

        y_pred,

        model_name="XGBoost Career Classifier"
    )


    display_evaluation(
        result
    )


    print("\nEvaluation completed successfully!")