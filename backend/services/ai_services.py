import requests
import time
from config.settings import settings

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"

headers = {
    "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}


def summarize_text(text):
    try:
        if not text:
            return "No text available."

        payload = {
            "inputs": text[:1000],
            "parameters": {
                "max_length": 120,
                "min_length": 30
            }
        }

        for _ in range(3):
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            result = response.json()

            print("HF Summary Response:", result)

            if isinstance(result, list) and "summary_text" in result[0]:
                return result[0]["summary_text"]

            if isinstance(result, dict) and "error" in result:
                time.sleep(5)

        return "Summary not available"

    except Exception as e:
        print("Summary Error:", e)
        return "Summary not available"