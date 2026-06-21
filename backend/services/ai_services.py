import requests

from config.settings import settings
from utils.logger import logger


def summarize_text(text):
    if not text:
        return "No text available."

    hf_key = settings.HUGGINGFACE_API_KEY
    if hf_key and hf_key not in ("", "your_openai_key_here"):
        try:
            r = requests.post(
                f"https://router.huggingface.co/hf-inference/models/{settings.HF_SUMMARY_MODEL}",
                headers={"Authorization": f"Bearer {hf_key}"},
                json={
                    "inputs": text[:1000],
                    "parameters": {"max_length": 120, "min_length": 30},
                },
                timeout=30,
            )
            result = r.json()
            if isinstance(result, list) and "summary_text" in result[0]:
                return result[0]["summary_text"]
            logger.warning("HF summary API: %s", result)
        except Exception as exc:
            logger.warning("HF summary API failed: %s", exc)

    return _extractive_summary(text[:3000])


def _extractive_summary(text: str, max_sentences: int = 4) -> str:
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if len(s.strip()) > 20]
    if not sentences:
        return text[:300].strip() + "..." if len(text) > 300 else text.strip()

    word_freq = {}
    for word in text.lower().split():
        clean = word.strip(".,;:!?()[]{}'\"-")
        if len(clean) > 3:
            word_freq[clean] = word_freq.get(clean, 0) + 1

    scored = []
    for i, sentence in enumerate(sentences[:25]):
        score = sum(word_freq.get(w.strip(".,;:!?()[]{}'\"-").lower(), 0) for w in sentence.split())
        scored.append((score / max(len(sentence.split()), 1), i, sentence))

    scored.sort(reverse=True)
    top = sorted(scored[:max_sentences], key=lambda x: x[1])
    return ". ".join(s[2] for s in top) + "."
