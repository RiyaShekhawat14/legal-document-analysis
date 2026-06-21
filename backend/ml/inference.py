import os
import re
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "artifacts", "risk_model.pkl")
TFIDF_PATH = os.path.join(BASE_DIR, "artifacts", "tfidf.pkl")
LABEL_ENCODER_PATH = os.path.join(BASE_DIR, "artifacts", "label_encoder.pkl")

_model = None
_tfidf = None
_label_encoder = None
_model_loaded = False


def _load_models():
    global _model, _tfidf, _label_encoder, _model_loaded
    if _model_loaded:
        return
    _model_loaded = True
    try:
        if os.path.exists(MODEL_PATH) and os.path.exists(TFIDF_PATH) and os.path.exists(LABEL_ENCODER_PATH):
            with open(MODEL_PATH, "rb") as f:
                _model = pickle.load(f)
            with open(TFIDF_PATH, "rb") as f:
                _tfidf = pickle.load(f)
            with open(LABEL_ENCODER_PATH, "rb") as f:
                _label_encoder = pickle.load(f)
    except Exception:
        _model = None
        _tfidf = None
        _label_encoder = None


_load_models()


RISK_KEYWORDS = {
    "high": ["unlimited", "penalty", "automatic renewal", "non-compete", "perpetual",
             "indemnify all", "without cause", "sole discretion", "irrevocable",
             "waive", "non-negotiable", "as is", "no warranty"],
    "medium": ["liable", "indemnify", "terminate", "breach", "confidential",
               "arbitration", "jurisdiction", "default", "indemnification",
               "warranty", "obligation", "liability", "liquidated damages"],
}


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _rule_based_risk(text: str) -> dict:
    text_lower = text.lower()
    high_count = sum(1 for kw in RISK_KEYWORDS["high"] if kw in text_lower)
    medium_count = sum(1 for kw in RISK_KEYWORDS["medium"] if kw in text_lower)

    if high_count >= 2:
        risk = "High Risk"
        confidence = min(0.55 + high_count * 0.08, 0.95)
    elif high_count >= 1 or medium_count >= 3:
        risk = "Medium Risk"
        confidence = min(0.40 + medium_count * 0.06, 0.85)
    else:
        risk = "Low Risk"
        confidence = max(0.60 - medium_count * 0.05, 0.30)

    return {"risk": risk, "confidence": round(confidence, 2)}


def predict_risk(text: str) -> dict:
    if not text:
        return {"risk": "Unknown", "confidence": None}

    if _model is None or _tfidf is None or _label_encoder is None:
        return _rule_based_risk(text)

    try:
        cleaned_text = clean_text(text)
        vector = _tfidf.transform([cleaned_text])
        prediction = _model.predict(vector)[0]
        confidence = _compute_confidence(vector)
        risk_label = _label_encoder.inverse_transform([prediction])[0]
        return {"risk": risk_label, "confidence": confidence}
    except Exception:
        return _rule_based_risk(text)


def _compute_confidence(vector) -> float | None:
    try:
        if hasattr(_model, "predict_proba"):
            return round(float(_model.predict_proba(vector).max()), 2)
        if hasattr(_model, "decision_function"):
            scores = _model.decision_function(vector)[0]
            if hasattr(scores, '__iter__'):
                import numpy as np
                exp_scores = np.exp(scores - scores.max())
                probs = exp_scores / exp_scores.sum()
                return round(float(probs.max()), 2)
            return round(float(1 / (1 + abs(scores))), 2)
    except Exception:
        pass
    return None