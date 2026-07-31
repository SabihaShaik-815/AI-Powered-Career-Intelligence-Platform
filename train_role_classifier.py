import argparse
import os
import re
import zipfile
import gc
import json

import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

ROLE_PATTERNS = {
    "Data Scientist": r"\bdata scientist\b",
    "Data Analyst": r"\bdata analyst\b",
    "Machine Learning Engineer": r"\bmachine learning engineer\b|\bml engineer\b",
    "Backend Developer": r"\bbackend (developer|engineer)\b|\bback[- ]end (developer|engineer)\b",
    "Frontend Developer": r"\bfrontend (developer|engineer)\b|\bfront[- ]end (developer|engineer)\b",
    "Full Stack Developer": r"\bfull[- ]?stack (developer|engineer)\b",
    "Software Engineer": r"\bsoftware engineer\b|\bsoftware developer\b",
    "DevOps Engineer": r"\bdevops engineer\b",
    "Product Manager": r"\bproduct manager\b",
    "Project Manager": r"\bproject manager\b",
    "Business Analyst": r"\bbusiness analyst\b",
    "Marketing Manager": r"\bmarketing manager\b",
    "Sales Representative": r"\bsales (representative|associate|executive)\b|\bsalesperson\b",
    "Accountant": r"\baccountant\b|\bstaff accountant\b|\bsenior accountant\b",
    "Registered Nurse": r"\bregistered nurse\b",
    "Customer Service Representative": r"\bcustomer service representative\b",
    "Administrative Assistant": r"\badministrative assistant\b|\bexecutive assistant\b",
}


def label_title(title):
    t = str(title).lower()
    for role, pattern in ROLE_PATTERNS.items():
        if re.search(pattern, t):
            return role
    return None


def ensure_postings_csv(data_arg, extract_dir):
    if data_arg.lower().endswith(".csv") and os.path.exists(data_arg):
        return data_arg
    postings_path = os.path.join(extract_dir, "postings.csv")
    if os.path.exists(postings_path):
        return postings_path
    if data_arg.lower().endswith(".zip") and os.path.exists(data_arg):
        print(f"Extracting {data_arg} ...")
        with zipfile.ZipFile(data_arg, "r") as z:
            z.extractall(extract_dir)
        if os.path.exists(postings_path):
            return postings_path
    raise FileNotFoundError(f"Could not resolve postings.csv from '{data_arg}'.")


def train(postings_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    print("Loading data...")
    df = pd.read_csv(postings_path, usecols=["title", "description"])
    df["role"] = df["title"].apply(label_title)
    df = df.dropna(subset=["role", "description"])
    print(f"Labeled {len(df)} rows across {df['role'].nunique()} roles")
    print(df["role"].value_counts())

    df["description"] = df["description"].astype(str).str.slice(0, 1000)
    df["text"] = (df["title"].astype(str) + " ") * 2 + df["description"]

    # FIX: use to_numpy(dtype=object) instead of .values — avoids the
    # pyarrow-backed string array indexing bug in newer pandas versions
    X = df["text"].to_numpy(dtype=object)
    y = df["role"].to_numpy(dtype=object)
    del df
    gc.collect()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Fitting TF-IDF...")
    tfidf = TfidfVectorizer(
        max_features=8000, stop_words="english", min_df=3,
        ngram_range=(1, 1), dtype=np.float32,
    )
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    print("Training Logistic Regression...")
    clf = LogisticRegression(max_iter=500, C=10)
    clf.fit(X_train_tfidf, y_train)

    y_pred = clf.predict(X_test_tfidf)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    print(f"\nAccuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))

    joblib.dump(clf, os.path.join(out_dir, "role_classifier.joblib"))
    joblib.dump(tfidf, os.path.join(out_dir, "role_tfidf_vectorizer.joblib"))
    with open(os.path.join(out_dir, "role_classes.json"), "w") as f:
        json.dump(sorted(clf.classes_.tolist()), f, indent=2)
    with open(os.path.join(out_dir, "role_metrics.json"), "w") as f:
        json.dump({"accuracy": acc, "classification_report": report}, f, indent=2)

    print(f"\nSaved role_classifier.joblib, role_tfidf_vectorizer.joblib to {out_dir}")
    return acc


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Path to postings.csv or archive.zip")
    parser.add_argument("--out", default="./models")
    parser.add_argument("--extract-dir", default="./data")
    args = parser.parse_args()

    postings_path = ensure_postings_csv(args.data, args.extract_dir)
    train(postings_path, args.out)