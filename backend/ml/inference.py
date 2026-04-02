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

    try:
        confidence = model.predict_proba(vector).max()
        confidence = round(float(confidence), 2)
    except:
        confidence = None

    risk_label = label_encoder.inverse_transform([prediction])[0]

    return {
        "risk": risk_label,
        "confidence": confidence
    }