"""
CareerCast Evaluation Metrics Module

This module calculates evaluation metrics for
career prediction models.
"""

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)


# ============================================================
# CALCULATE ACCURACY
# ============================================================

def calculate_accuracy(y_true, y_pred):
    """
    Calculate prediction accuracy.
    """

    return round(
        accuracy_score(y_true, y_pred) * 100,
        2
    )


# ============================================================
# CALCULATE PRECISION
# ============================================================

def calculate_precision(y_true, y_pred):
    """
    Calculate weighted precision.
    """

    return round(
        precision_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0
        ) * 100,
        2
    )


# ============================================================
# CALCULATE RECALL
# ============================================================

def calculate_recall(y_true, y_pred):
    """
    Calculate weighted recall.
    """

    return round(
        recall_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0
        ) * 100,
        2
    )


# ============================================================
# CALCULATE F1 SCORE
# ============================================================

def calculate_f1_score(y_true, y_pred):
    """
    Calculate weighted F1 score.
    """

    return round(
        f1_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0
        ) * 100,
        2
    )


# ============================================================
# CALCULATE ALL METRICS
# ============================================================

def calculate_all_metrics(y_true, y_pred):
    """
    Calculate all major evaluation metrics.
    """

    accuracy = calculate_accuracy(
        y_true,
        y_pred
    )

    precision = calculate_precision(
        y_true,
        y_pred
    )

    recall = calculate_recall(
        y_true,
        y_pred
    )

    f1 = calculate_f1_score(
        y_true,
        y_pred
    )

    return {

        "accuracy": accuracy,

        "precision": precision,

        "recall": recall,

        "f1_score": f1
    }


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

def get_classification_report(
    y_true,
    y_pred
):
    """
    Generate a detailed classification report.
    """

    return classification_report(

        y_true,

        y_pred,

        zero_division=0,

        output_dict=True
    )


# ============================================================
# DISPLAY METRICS
# ============================================================

def print_metrics(metrics):
    """
    Display metrics in a clean format.
    """

    print("\n==========================================")

    print("       CAREERCAST MODEL EVALUATION")

    print("==========================================")

    print(
        f"Accuracy  : {metrics['accuracy']}%"
    )

    print(
        f"Precision : {metrics['precision']}%"
    )

    print(
        f"Recall    : {metrics['recall']}%"
    )

    print(
        f"F1 Score  : {metrics['f1_score']}%"
    )

    print("==========================================\n")


# ============================================================
# TEST MODULE
# ============================================================

if __name__ == "__main__":

    # Sample actual career roles

    y_true = [

        "Software Engineer",

        "Data Scientist",

        "Data Analyst",

        "AI Engineer",

        "Software Engineer"
    ]


    # Sample predicted career roles

    y_pred = [

        "Software Engineer",

        "Data Scientist",

        "Data Analyst",

        "Machine Learning Engineer",

        "Software Engineer"
    ]


    metrics = calculate_all_metrics(

        y_true,

        y_pred
    )


    print_metrics(
        metrics
    )