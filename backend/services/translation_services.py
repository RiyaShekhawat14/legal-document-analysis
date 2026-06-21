import requests

from config.settings import settings
from utils.logger import logger


def translate_text(text, target_language="hi"):
    if not text:
        return ""

    hf_key = settings.HUGGINGFACE_API_KEY
    if hf_key and hf_key not in ("", "your_openai_key_here"):
        try:
            r = requests.post(
                f"https://router.huggingface.co/hf-inference/models/{settings.HF_TRANSLATION_MODEL}",
                headers={"Authorization": f"Bearer {hf_key}"},
                json={"inputs": text[:500]},
                timeout=30,
            )
            result = r.json()
            if isinstance(result, list) and "translation_text" in result[0]:
                return result[0]["translation_text"]
            logger.warning("HF translation API: %s", result)
        except Exception as exc:
            logger.warning("HF translation API failed: %s", exc)

    return text
