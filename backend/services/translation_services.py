import requests
from config.settings import settings

API_URL = "https://router.huggingface.co/hf-inference/models/Helsinki-NLP/opus-mt-en-hi"

headers = {
    "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

def translate_text(text):
    try:
        if not text:
            return ""

        payload = {
            "inputs": text[:500]
        }

        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        result = response.json()

        print("Translation Response:", result)

        if isinstance(result, list) and "translation_text" in result[0]:
            return result[0]["translation_text"]

        return text

    except Exception as e:
        print("Translation Error:", e)
        return text