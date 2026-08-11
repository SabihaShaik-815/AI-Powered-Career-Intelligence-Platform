import os
import re
import json
import warnings
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from xgboost import XGBClassifier

warnings.filterwarnings("ignore")


# ============================================================
# 1. SETTINGS
# ============================================================

DATA_PATH = r"data\postings.csv"
MODEL_DIR = r"advanced_models"

os.makedirs(MODEL_DIR, exist_ok=True)

RANDOM_STATE = 42


print("=" * 75)
print("AI-POWERED CAREER INTELLIGENCE PLATFORM")
print("MILESTONE 2 - ADVANCED ML MODEL TRAINING")
print("=" * 75)


# ============================================================
# 2. CAREER ROLE PATTERNS
# ============================================================

ROLE_PATTERNS = {

    "Data Scientist":
        r"\bdata scientist\b",

    "Data Analyst":
        r"\bdata analyst\b",

    "Machine Learning Engineer":
        r"\bmachine learning engineer\b|\bml engineer\b",

    "Backend Developer":
        r"\bbackend (developer|engineer)\b|"
        r"\bback[- ]end (developer|engineer)\b",

    "Frontend Developer":
        r"\bfrontend (developer|engineer)\b|"
        r"\bfront[- ]end (developer|engineer)\b",

    "Full Stack Developer":
        r"\bfull[- ]?stack (developer|engineer)\b",

    "Software Engineer":
        r"\bsoftware engineer\b|\bsoftware developer\b",

    "DevOps Engineer":
        r"\bdevops engineer\b",

    "Product Manager":
        r"\bproduct manager\b",

    "Project Manager":
        r"\bproject manager\b",

    "Business Analyst":
        r"\bbusiness analyst\b",

    "Marketing Manager":
        r"\bmarketing manager\b",

    "Sales Representative":
        r"\bsales (representative|associate|executive)\b|"
        r"\bsalesperson\b",

    "Accountant":
        r"\baccountant\b|\bstaff accountant\b|\bsenior accountant\b",

    "Registered Nurse":
        r"\bregistered nurse\b",

    "Customer Service Representative":
        r"\bcustomer service representative\b",

    "Administrative Assistant":
        r"\badministrative assistant\b|\bexecutive assistant\b",
}


def label_title(title):

    title = str(title).lower()

    for role, pattern in ROLE_PATTERNS.items():

        if re.search(pattern, title):

            return role

    return None


# ============================================================
# 3. LOAD DATASET
# ============================================================

print("\nLoading dataset...")

if not os.path.exists(DATA_PATH):

    raise FileNotFoundError(
        f"\nDataset not found:\n{DATA_PATH}"
    )

df = pd.read_csv(DATA_PATH)

print("Original dataset shape:", df.shape)


# ============================================================
# 4. CHECK COLUMNS
# ============================================================

required_columns = [
    "title",
    "description"
]

for column in required_columns:

    if column not in df.columns:

        raise ValueError(
            f"Required column missing: {column}"
        )


# ============================================================
# 5. CREATE CAREER ROLE LABEL
# ============================================================

print("\nCreating career-role labels...")

df["career_role"] = df["title"].apply(label_title)

df = df.dropna(
    subset=[
        "career_role",
        "description"
    ]
).copy()

print(
    "\nLabeled dataset:",
    len(df)
)

print(
    "Number of career roles:",
    df["career_role"].nunique()
)

print("\nRole distribution:")

print(
    df["career_role"].value_counts()
)


# ============================================================
# 6. CLEAN TEXT
# ============================================================

df["title"] = (
    df["title"]
    .fillna("")
    .astype(str)
)

df["description"] = (
    df["description"]
    .fillna("")
    .astype(str)
)


# Include skills if available

if "skills_desc" in df.columns:

    df["skills_desc"] = (
        df["skills_desc"]
        .fillna("")
        .astype(str)
    )

    df["combined_text"] = (
        df["title"] + " " +
        df["title"] + " " +
        df["description"] + " " +
        df["skills_desc"]
    )

else:

    df["combined_text"] = (
        df["title"] + " " +
        df["title"] + " " +
        df["description"]
    )


# Limit extremely long descriptions

df["combined_text"] = (
    df["combined_text"]
    .str.slice(0, 6000)
)


# ============================================================
# 7. TRAIN / TEST SPLIT
# ============================================================

X = df["combined_text"]

y = df["career_role"]


label_encoder = LabelEncoder()

y_encoded = label_encoder.fit_transform(y)


print("\nEncoded classes:")

for index, role in enumerate(
    label_encoder.classes_
):

    print(
        index,
        "=",
        role
    )


X_train, X_test, y_train, y_test = train_test_split(

    X,
    y_encoded,

    test_size=0.20,

    random_state=RANDOM_STATE,

    stratify=y_encoded
)


print("\nTraining samples:", len(X_train))

print("Testing samples :", len(X_test))


# ============================================================
# 8. TF-IDF
# ============================================================

print("\n" + "=" * 75)

print("CREATING TF-IDF FEATURES")

print("=" * 75)


tfidf = TfidfVectorizer(

    lowercase=True,

    stop_words="english",

    ngram_range=(1, 2),

    min_df=2,

    max_df=0.95,

    max_features=20000,

    sublinear_tf=True,

    dtype=np.float32
)


print("\nFitting TF-IDF...")

X_train_tfidf = tfidf.fit_transform(X_train)

X_test_tfidf = tfidf.transform(X_test)


print(
    "TF-IDF training shape:",
    X_train_tfidf.shape
)

print(
    "TF-IDF testing shape :",
    X_test_tfidf.shape
)


# ============================================================
# 9. RANDOM FOREST
# ============================================================

print("\n" + "=" * 75)

print("RANDOM FOREST")

print("=" * 75)


rf = RandomForestClassifier(

    random_state=RANDOM_STATE,

    n_jobs=-1,

    class_weight="balanced_subsample"
)


rf_params = {

    "n_estimators": [
        200,
        300,
        400
    ],

    "max_depth": [
        20,
        30,
        40,
        None
    ],

    "min_samples_split": [
        2,
        5,
        10
    ],

    "min_samples_leaf": [
        1,
        2,
        4
    ],

    "max_features": [
        "sqrt",
        "log2"
    ]
}


rf_search = RandomizedSearchCV(

    estimator=rf,

    param_distributions=rf_params,

    n_iter=10,

    cv=3,

    scoring="accuracy",

    random_state=RANDOM_STATE,

    n_jobs=-1,

    verbose=1
)


print(
    "\nTraining Random Forest..."
)

rf_search.fit(
    X_train_tfidf,
    y_train
)


rf_model = rf_search.best_estimator_


print(
    "\nBest Random Forest parameters:"
)

print(
    rf_search.best_params_
)


rf_pred = rf_model.predict(
    X_test_tfidf
)


# ============================================================
# 10. RANDOM FOREST METRICS
# ============================================================

rf_accuracy = accuracy_score(
    y_test,
    rf_pred
)

rf_precision = precision_score(
    y_test,
    rf_pred,
    average="weighted",
    zero_division=0
)

rf_recall = recall_score(
    y_test,
    rf_pred,
    average="weighted",
    zero_division=0
)

rf_f1 = f1_score(
    y_test,
    rf_pred,
    average="weighted",
    zero_division=0
)


print("\n" + "-" * 60)

print("RANDOM FOREST RESULTS")

print("-" * 60)

print(
    f"Accuracy  : {rf_accuracy * 100:.2f}%"
)

print(
    f"Precision : {rf_precision * 100:.2f}%"
)

print(
    f"Recall    : {rf_recall * 100:.2f}%"
)

print(
    f"F1 Score  : {rf_f1 * 100:.2f}%"
)


# ============================================================
# 11. XGBOOST
# ============================================================

print("\n" + "=" * 75)

print("XGBOOST")

print("=" * 75)


xgb = XGBClassifier(

    objective="multi:softprob",

    num_class=len(
        label_encoder.classes_
    ),

    eval_metric="mlogloss",

    random_state=RANDOM_STATE,

    n_jobs=-1,

    tree_method="hist"
)


xgb_params = {

    "n_estimators": [
        200,
        300,
        400
    ],

    "max_depth": [
        4,
        6,
        8
    ],

    "learning_rate": [
        0.03,
        0.05,
        0.1
    ],

    "subsample": [
        0.8,
        1.0
    ],

    "colsample_bytree": [
        0.8,
        1.0
    ]
}


xgb_search = RandomizedSearchCV(

    estimator=xgb,

    param_distributions=xgb_params,

    n_iter=10,

    cv=3,

    scoring="accuracy",

    random_state=RANDOM_STATE,

    n_jobs=-1,

    verbose=1
)


print(
    "\nTraining XGBoost..."
)


xgb_search.fit(

    X_train_tfidf,

    y_train
)


xgb_model = (
    xgb_search.best_estimator_
)


print(
    "\nBest XGBoost parameters:"
)

print(
    xgb_search.best_params_
)


xgb_pred = xgb_model.predict(
    X_test_tfidf
)


# ============================================================
# 12. XGBOOST METRICS
# ============================================================

xgb_accuracy = accuracy_score(
    y_test,
    xgb_pred
)

xgb_precision = precision_score(
    y_test,
    xgb_pred,
    average="weighted",
    zero_division=0
)

xgb_recall = recall_score(
    y_test,
    xgb_pred,
    average="weighted",
    zero_division=0
)

xgb_f1 = f1_score(
    y_test,
    xgb_pred,
    average="weighted",
    zero_division=0
)


print("\n" + "-" * 60)

print("XGBOOST RESULTS")

print("-" * 60)

print(
    f"Accuracy  : {xgb_accuracy * 100:.2f}%"
)

print(
    f"Precision : {xgb_precision * 100:.2f}%"
)

print(
    f"Recall    : {xgb_recall * 100:.2f}%"
)

print(
    f"F1 Score  : {xgb_f1 * 100:.2f}%"
)


# ============================================================
# 13. CLASSIFICATION REPORTS
# ============================================================

print("\n" + "=" * 75)

print("RANDOM FOREST CLASSIFICATION REPORT")

print("=" * 75)

print(
    classification_report(

        y_test,

        rf_pred,

        target_names=label_encoder.classes_,

        zero_division=0
    )
)


print("\n" + "=" * 75)

print("XGBOOST CLASSIFICATION REPORT")

print("=" * 75)

print(
    classification_report(

        y_test,

        xgb_pred,

        target_names=label_encoder.classes_,

        zero_division=0
    )
)


# ============================================================
# 14. MODEL COMPARISON
# ============================================================

print("\n" + "=" * 75)

print("MODEL COMPARISON")

print("=" * 75)


print(
    f"Random Forest : "
    f"{rf_accuracy * 100:.2f}%"
)

print(
    f"XGBoost       : "
    f"{xgb_accuracy * 100:.2f}%"
)


if rf_accuracy >= xgb_accuracy:

    best_name = "Random Forest"

    best_model = rf_model

    best_accuracy = rf_accuracy

else:

    best_name = "XGBoost"

    best_model = xgb_model

    best_accuracy = xgb_accuracy


print(
    f"\nBest Model: "
    f"{best_name}"
)

print(
    f"Best Accuracy: "
    f"{best_accuracy * 100:.2f}%"
)


# ============================================================
# 15. SAVE MODELS
# ============================================================

print("\n" + "=" * 75)

print("SAVING MODELS")

print("=" * 75)


joblib.dump(

    rf_model,

    os.path.join(
        MODEL_DIR,
        "random_forest_model.pkl"
    )
)


joblib.dump(

    xgb_model,

    os.path.join(
        MODEL_DIR,
        "xgboost_model.pkl"
    )
)


joblib.dump(

    tfidf,

    os.path.join(
        MODEL_DIR,
        "career_tfidf_vectorizer.pkl"
    )
)


joblib.dump(

    label_encoder,

    os.path.join(
        MODEL_DIR,
        "career_label_encoder.pkl"
    )
)


# ============================================================
# 16. SAVE METRICS
# ============================================================

metrics = {

    "random_forest": {

        "accuracy":
            round(
                rf_accuracy * 100,
                2
            ),

        "precision":
            round(
                rf_precision * 100,
                2
            ),

        "recall":
            round(
                rf_recall * 100,
                2
            ),

        "f1_score":
            round(
                rf_f1 * 100,
                2
            )
    },

    "xgboost": {

        "accuracy":
            round(
                xgb_accuracy * 100,
                2
            ),

        "precision":
            round(
                xgb_precision * 100,
                2
            ),

        "recall":
            round(
                xgb_recall * 100,
                2
            ),

        "f1_score":
            round(
                xgb_f1 * 100,
                2
            )
    },

    "best_model":
        best_name,

    "best_accuracy":
        round(
            best_accuracy * 100,
            2
        )
}


with open(

    os.path.join(
        MODEL_DIR,
        "advanced_metrics.json"
    ),

    "w"
) as file:

    json.dump(
        metrics,
        file,
        indent=4
    )


# ============================================================
# 17. FINAL OUTPUT
# ============================================================

print("\n" + "=" * 75)

print("FINAL MILESTONE 2 RESULTS")

print("=" * 75)

print(
    f"\nRandom Forest Accuracy : "
    f"{rf_accuracy * 100:.2f}%"
)

print(
    f"XGBoost Accuracy       : "
    f"{xgb_accuracy * 100:.2f}%"
)

print(
    f"\nBest Model             : "
    f"{best_name}"
)

print(
    f"Best Accuracy          : "
    f"{best_accuracy * 100:.2f}%"
)

print("\nModels saved in:")

print(
    os.path.abspath(MODEL_DIR)
)

print("\nTraining completed successfully!")

print("=" * 75)