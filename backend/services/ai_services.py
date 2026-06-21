from utils.logger import logger


def summarize_text(text):
    if not text:
        return "No text available."
    return _extractive_summary(text[:3000])


def _extractive_summary(text: str, max_sentences: int = 4) -> str:
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if len(s.strip()) > 20]
    if not sentences:
        return text[:300].strip() + "..." if len(text) > 300 else text.strip()

    word_freq = {}
    words = text.lower().split()
    for word in words:
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
