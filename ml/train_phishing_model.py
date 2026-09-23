"""
Phishing Email ML Model Training

Trains a TF-IDF + Logistic Regression classifier
using the phishing_email.csv dataset.
"""

import os

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

import joblib


# ==========================================================
# Configuration
# ==========================================================

DATASET_PATH = "ml/dataset/phishing_email.csv"

MODEL_DIR = "ml/models"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "phishing_model.pkl",
)

VECTORIZER_PATH = os.path.join(
    MODEL_DIR,
    "tfidf_vectorizer.pkl",
)


# ==========================================================
# Load Dataset
# ==========================================================

print("=" * 60)
print("Loading phishing email dataset...")
print("=" * 60)

df = pd.read_csv(
    DATASET_PATH,
    usecols=["text_combined", "label"],
)

print(f"Total emails loaded: {len(df)}")


# ==========================================================
# Clean Dataset
# ==========================================================

print("\nCleaning dataset...")

df = df.dropna(
    subset=["text_combined", "label"]
)

df["text_combined"] = (
    df["text_combined"]
    .astype(str)
    .str.strip()
)

df = df[
    df["text_combined"] != ""
]

print(
    f"Emails after cleaning: {len(df)}"
)


# ==========================================================
# Features and Labels
# ==========================================================

X = df["text_combined"]

y = df["label"]


# ==========================================================
# Train/Test Split
# ==========================================================

print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

print(
    f"Training samples: {len(X_train)}"
)

print(
    f"Testing samples: {len(X_test)}"
)


# ==========================================================
# TF-IDF Vectorization
# ==========================================================

print("\nCreating TF-IDF vectors...")

vectorizer = TfidfVectorizer(
    max_features=100000,
    stop_words="english",
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.98,
    sublinear_tf=True,
)

X_train_tfidf = vectorizer.fit_transform(
    X_train
)

X_test_tfidf = vectorizer.transform(
    X_test
)

print(
    f"TF-IDF training shape: {X_train_tfidf.shape}"
)


# ==========================================================
# Train Logistic Regression
# ==========================================================

print("\nTraining Logistic Regression model...")

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42,
)

model.fit(
    X_train_tfidf,
    y_train,
)

print("Model training completed.")


# ==========================================================
# Predictions
# ==========================================================

print("\nEvaluating model...")

y_pred = model.predict(
    X_test_tfidf
)


# ==========================================================
# Evaluation
# ==========================================================

accuracy = accuracy_score(
    y_test,
    y_pred,
)

print("\n" + "=" * 60)
print("MODEL RESULTS")
print("=" * 60)

print(
    f"\nAccuracy: {accuracy:.4f}"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Legitimate",
            "Phishing",
        ],
    )
)

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred,
    )
)


# ==========================================================
# Save Model
# ==========================================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True,
)

joblib.dump(
    model,
    MODEL_PATH,
)

joblib.dump(
    vectorizer,
    VECTORIZER_PATH,
)


print("\n" + "=" * 60)
print("MODEL SAVED")
print("=" * 60)

print(
    f"\nModel: {MODEL_PATH}"
)

print(
    f"Vectorizer: {VECTORIZER_PATH}"
)

print("\nTraining complete! 🎣🤖")