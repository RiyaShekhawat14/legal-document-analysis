"""
API-based LLM service for deployment without local models.
Supports HuggingFace Inference API and OpenAI API.
"""
import requests

from config.settings import settings
from utils.logger import logger


class ApiLlmService:
    def __init__(self):
        self._hf_checked = False
        self._hf_available = False

    def _check_hf(self) -> bool:
        if self._hf_checked:
            return self._hf_available
        self._hf_checked = True
        key = settings.HUGGINGFACE_API_KEY
        if not key or key in ("", "your_openai_key_here"):
            return False
        try:
            r = requests.post(
                "https://router.huggingface.co/hf-inference/models/Qwen/Qwen2.5-0.5B-Instruct",
                headers={"Authorization": f"Bearer {key}"},
                json={"inputs": "Hi"},
                timeout=10,
            )
            self._hf_available = r.status_code == 200
        except Exception:
            self._hf_available = False
        return self._hf_available

    def _call_hf_chat(self, question: str, context_chunks: list[str], history=None) -> str:
        context_text = "\n\n".join(
            f"[Context {i+1}]\n{chunk}" for i, chunk in enumerate(context_chunks)
        ) or "No document context available."

        messages = [{"role": "system", "content": (
            "You are a legal document assistant. Answer accurately using the "
            "retrieved context. If not supported, say so. Be concise."
        )}]
        for item in history or []:
            role = item.get("role", "").lower()
            content = item.get("content", "").strip()
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": (
            f"Document context:\n{context_text}\n\n"
            f"Question: {question}\n\nAnswer:"
        )})

        prompt = "\n".join(f"[{m['role']}] {m['content']}" for m in messages)

        r = requests.post(
            f"https://router.huggingface.co/hf-inference/models/{settings.HF_CHAT_MODEL}",
            headers={"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"},
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": settings.LEGAL_AI_MAX_NEW_TOKENS,
                    "temperature": settings.LEGAL_AI_TEMPERATURE,
                    "return_full_text": False,
                },
            },
            timeout=60,
        )
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0].get("generated_text", "").strip()
        return ""

    def _call_openai_chat(self, question: str, context_chunks: list[str], history=None) -> str:
        context_text = "\n\n".join(
            f"[Context {i+1}]\n{chunk}" for i, chunk in enumerate(context_chunks)
        ) or "No document context available."

        messages = [{"role": "system", "content": (
            "You are a legal document assistant. Answer accurately using the "
            "retrieved document context. Be concise and professional."
        )}]
        for item in history or []:
            role = item.get("role", "").lower()
            content = item.get("content", "").strip()
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": (
            f"Retrieved document context:\n{context_text}\n\n"
            f"Question: {question}"
        )})

        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.OPENAI_MODEL,
                "messages": messages,
                "max_tokens": settings.LEGAL_AI_MAX_NEW_TOKENS,
                "temperature": settings.LEGAL_AI_TEMPERATURE,
            },
            timeout=60,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()

    def answer_question(self, question: str, context_chunks: list[str], history=None) -> dict:
        answer = None
        mode = "retrieval_fallback"

        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY not in ("", "your_openai_key_here"):
            try:
                answer = self._call_openai_chat(question, context_chunks, history)
                mode = "openai"
            except Exception as exc:
                logger.warning("OpenAI chat failed: %s", exc)

        if not answer and self._check_hf():
            try:
                answer = self._call_hf_chat(question, context_chunks, history)
                mode = "huggingface_api"
            except Exception as exc:
                logger.warning("HuggingFace chat API failed: %s", exc)

        if not answer:
            answer = self._build_fallback(question, context_chunks)
            mode = "retrieval_fallback"

        return {
            "answer": answer,
            "mode": mode,
            "used_context_chunks": len(context_chunks),
        }

    def _build_fallback(self, question: str, context_chunks: list[str]) -> str:
        if not context_chunks:
            return "I could not find relevant information. Please upload a document first."
        question_words = {
            w.strip(".,:;!?()[]{}'\"").lower()
            for w in question.split() if len(w) > 2
        }
        sentences = []
        for chunk in context_chunks:
            sentences.extend(s.strip() for s in chunk.replace("\n", " ").split(".") if s.strip())
        ranked = sorted(
            sentences,
            key=lambda s: len({w.strip(".,:;!?()[]{}'\"").lower() for w in s.split() if len(w) > 2} & question_words),
            reverse=True,
        )
        best = ranked[:3] or [context_chunks[0].strip()]
        if len(best) == 1:
            return f"Based on the document, {best[0].rstrip('.')}."
        return "Based on the document: " + " ".join(f"{s.rstrip('.')}." for s in best)

    def get_status(self) -> dict:
        hf_ok = self._check_hf()
        openai_ok = bool(settings.OPENAI_API_KEY and settings.OPENAI_API_KEY not in ("", "your_openai_key_here"))

        if openai_ok:
            mode = "openai"
            message = f"Using OpenAI API ({settings.OPENAI_MODEL})."
        elif hf_ok:
            mode = "huggingface_api"
            message = f"Using HuggingFace Inference API ({settings.HF_CHAT_MODEL})."
        else:
            mode = "retrieval_fallback"
            message = "No API key configured. Using retrieval fallback. Set HUGGINGFACE_API_KEY or OPENAI_API_KEY."

        return {
            "available": openai_ok or hf_ok,
            "mode": mode,
            "message": message,
            "huggingface_available": hf_ok,
            "openai_available": openai_ok,
            "hf_chat_model": settings.HF_CHAT_MODEL,
            "openai_model": settings.OPENAI_MODEL,
        }


api_llm_service = ApiLlmService()
