from services.ai_services import summarize_text

def generate_summary(text):
    if not text:
        return "No text available for summary."

    summary = summarize_text(text)
    return summary