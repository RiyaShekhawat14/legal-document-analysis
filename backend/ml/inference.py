import os
import re
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "artifacts", "risk_model.pkl")
TFIDF_PATH = os.path.join(BASE_DIR, "artifacts", "tfidf.pkl")
LABEL_ENCODER_PATH = os.path.join(BASE_DIR, "artifacts", "label_encoder.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(TFIDF_PATH, "rb") as f:
    tfidf = pickle.load(f)

with open(LABEL_ENCODER_PATH, "rb") as f:
    label_encoder = pickle.load(f)


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def predict_risk(text: str) -> dict:
    if not text:
        return {"risk": "Unknown", "confidence": None}

    cleaned_text = clean_text(text)
    vector = tfidf.transform([cleaned_text])
    prediction = model.predict(vector)[0]

    confidence = _compute_confidence(vector)

    risk_label = label_encoder.inverse_transform([prediction])[0]

    return {
        "risk": risk_label,
        "confidence": confidence
    }


def _compute_confidence(vector) -> float | None:
    try:
        if hasattr(model, "predict_proba"):
            return round(float(model.predict_proba(vector).max()), 2)

        if hasattr(model, "decision_function"):
            scores = model.decision_function(vector)[0]
            if hasattr(scores, '__iter__'):
                import numpy as np
                exp_scores = np.exp(scores - scores.max())
                probs = exp_scores / exp_scores.sum()
                return round(float(probs.max()), 2)
            return round(float(1 / (1 + abs(scores))), 2)
    except Exception:
        pass
    return None