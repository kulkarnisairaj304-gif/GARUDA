"""
Phishing AI Predictor

Loads the trained phishing detection model
and predicts whether an email is phishing.
"""

import os
import joblib


# -------------------------------------------------------
# Model Paths
# -------------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "phishing_model.pkl",
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "tfidf_vectorizer.pkl",
)


# -------------------------------------------------------
# Load Model
# -------------------------------------------------------

model = joblib.load(
    MODEL_PATH
)

vectorizer = joblib.load(
    VECTORIZER_PATH
)


# -------------------------------------------------------
# Prediction
# -------------------------------------------------------

def predict_phishing(
    text: str,
):

    # Convert email text into TF-IDF features
    text_vector = vectorizer.transform(
        [text]
    )

    # Predict class
    prediction = model.predict(
        text_vector
    )[0]

    # Get probability
    probabilities = model.predict_proba(
        text_vector
    )[0]

    phishing_probability = float(
        probabilities[1]
    )

    legitimate_probability = float(
        probabilities[0]
    )

    # Classification
    if prediction == 1:

        classification = "Phishing"

    else:

        classification = "Safe"

    return {
        "classification": classification,
        "phishing_probability": phishing_probability,
        "legitimate_probability": legitimate_probability,
    }