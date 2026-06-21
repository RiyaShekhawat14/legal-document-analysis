import requests

from config.settings import settings
from utils.logger import logger


class LegalAssistantUnavailable(RuntimeError):
    pass


class LegalAssistantService:
    def __init__(self):
        self._model = None
        self._tokenizer = None
        self._load_error = None
        self._resolved_base_model = None
        self._ollama_checked = False
        self._ollama_available = False

    @property
    def model_path(self):
        from pathlib import Path
        return Path(settings.LEGAL_AI_MODEL_PATH)

    def _check_ollama(self) -> bool:
        if self._ollama_checked:
            return self._ollama_available
        self._ollama_checked = True
        try:
            r = requests.get(
                f"{settings.OLLAMA_BASE_URL}/api/tags",
                timeout=5,
            )
            if r.status_code == 200:
                models = [m.get("name", "") for m in r.json().get("models", [])]
                if settings.OLLAMA_MODEL in models:
                    self._ollama_available = True
                    logger.info("Ollama available, model '%s' is loaded.", settings.OLLAMA_MODEL)
                else:
                    logger.warning(
                        "Ollama is running but model '%s' not found. Available: %s",
                        settings.OLLAMA_MODEL,
                        models,
                    )
        except Exception as exc:
            logger.warning("Ollama not reachable at %s: %s", settings.OLLAMA_BASE_URL, exc)
        return self._ollama_available

    def _call_ollama(self, question: str, context_chunks: list[str], history=None) -> str:
        context_text = "\n\n".join(
            f"[Context {i + 1}]\n{chunk}" for i, chunk in enumerate(context_chunks)
        ) or "No document context is currently available."

        system_message = (
            "You are a legal document assistant. Answer accurately using the retrieved "
            "document context. If the answer is not supported by the context, say so clearly "
            "and do not invent facts. Be concise and professional."
        )
        user_content = (
            f"Retrieved document context:\n{context_text}\n\n"
            f"Question: {question}\n\n"
            "Answer with clear legal reasoning grounded in the provided context."
        )

        messages = [{"role": "system", "content": system_message}]
        for item in history or []:
            role = item.get("role", "").strip().lower()
            content = item.get("content", "").strip()
            if role in {"user", "assistant"} and content:
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": user_content})

        payload = {
            "model": settings.OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": settings.LEGAL_AI_TEMPERATURE,
                "num_predict": settings.LEGAL_AI_MAX_NEW_TOKENS,
            },
        }

        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=settings.OLLAMA_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", "").strip()

    def _load_fine_tuned_model(self):
        if self._model is not None and self._tokenizer is not None:
            return

        import torch

        if (
            settings.LEGAL_AI_CPU_SAFE_MODE
            and not torch.cuda.is_available()
            and not settings.LEGAL_AI_ENABLE_FINE_TUNED_ON_CPU
        ):
            raise LegalAssistantUnavailable(
                "Laptop-safe mode is enabled on CPU, so the fine-tuned model is skipped."
            )

        model_path = self.model_path
        if not model_path.exists():
            raise LegalAssistantUnavailable(
                f"Fine-tuned model folder not found at {model_path}."
            )

        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise LegalAssistantUnavailable(
                "transformers is not installed."
            ) from exc

        try:
            from peft import PeftConfig, PeftModel
        except ImportError:
            PeftModel = None
            PeftConfig = None

        adapter_exists = (model_path / "adapter_config.json").exists()
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        model_kwargs = {
            "torch_dtype": dtype,
            "trust_remote_code": True,
            "low_cpu_mem_usage": True,
        }
        auth_token = settings.HUGGINGFACE_API_KEY or None
        if auth_token:
            model_kwargs["token"] = auth_token

        self._tokenizer = AutoTokenizer.from_pretrained(
            str(model_path),
            trust_remote_code=True,
            local_files_only=True,
        )
        if self._tokenizer.pad_token is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token

        if adapter_exists:
            if PeftModel is None or PeftConfig is None:
                raise LegalAssistantUnavailable(
                    "peft is required to load your LoRA adapter."
                )
            peft_config = PeftConfig.from_pretrained(str(model_path), local_files_only=True)
            base_model_name = settings.LEGAL_AI_BASE_MODEL or peft_config.base_model_name_or_path
            resolved_base = self._resolve_cached_repo_path(base_model_name)
            if resolved_base == base_model_name and "/" in str(base_model_name):
                raise LegalAssistantUnavailable(
                    f"Base model `{base_model_name}` not found in local HF cache. "
                    "Download it first with huggingface-cli or snapshot_download."
                )
            if not self._path_has_model_weights(resolved_base):
                raise LegalAssistantUnavailable(
                    f"Cached base model found but weight files are missing at {resolved_base}."
                )
            self._resolved_base_model = resolved_base
            self._model = AutoModelForCausalLM.from_pretrained(
                resolved_base, local_files_only=True, **model_kwargs,
            )
            self._model = PeftModel.from_pretrained(self._model, str(model_path), local_files_only=True)
        else:
            self._model = AutoModelForCausalLM.from_pretrained(
                str(model_path), local_files_only=True, **model_kwargs,
            )

        self._model = self._model.to("cuda" if torch.cuda.is_available() else "cpu")
        self._model.eval()
        self._load_error = None
        logger.info("Fine-tuned legal model loaded from %s", model_path)

    def _call_fine_tuned(self, question: str, context_chunks: list[str], history=None) -> str:
        import torch

        self._load_fine_tuned_model()

        context_text = "\n\n".join(
            f"[Context {i + 1}]\n{chunk}" for i, chunk in enumerate(context_chunks)
        ) or "No document context is currently available."

        messages = [{"role": "system", "content": (
            "You are a legal document assistant. Answer accurately using the retrieved "
            "document context. If the answer is not supported by the context, say so clearly "
            "and do not invent facts."
        )}]
        for item in history or []:
            role = item.get("role", "").strip().lower()
            content = item.get("content", "").strip()
            if role in {"user", "assistant"} and content:
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": (
            f"Retrieved document context:\n{context_text}\n\n"
            f"Question: {question}\n\n"
            "Answer with clear legal reasoning grounded in the provided context."
        )})

        try:
            import torch as _torch

            prompt_text = None
            if hasattr(self._tokenizer, "apply_chat_template"):
                try:
                    rendered = self._tokenizer.apply_chat_template(
                        messages, add_generation_prompt=True, tokenize=False,
                        truncation=True, max_length=4096,
                    )
                    if isinstance(rendered, str):
                        prompt_text = rendered
                except Exception:
                    prompt_text = None

            if prompt_text is None:
                prompt_text = f"### Context:\n{context_text}\n\n### Question:\n{question}\n\n### Response:\n"

            encoded = self._tokenizer(
                prompt_text, return_tensors="pt", truncation=True, max_length=4096,
            )
            input_ids = encoded["input_ids"]

            if not isinstance(input_ids, _torch.Tensor):
                input_ids = _torch.tensor(input_ids, dtype=_torch.long)

            if input_ids.dim() == 1:
                input_ids = input_ids.unsqueeze(0)

            device = next(self._model.parameters()).device
            input_ids = input_ids.to(device)
            pad_id = self._tokenizer.pad_token_id
            if pad_id is None:
                pad_id = self._tokenizer.eos_token_id
            attention_mask = encoded.get("attention_mask")
            if attention_mask is None or not isinstance(attention_mask, _torch.Tensor):
                attention_mask = _torch.ones_like(input_ids)
            attention_mask = attention_mask.to(device)

            with torch.inference_mode():
                outputs = self._model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    max_new_tokens=settings.LEGAL_AI_MAX_NEW_TOKENS,
                    temperature=settings.LEGAL_AI_TEMPERATURE,
                    do_sample=settings.LEGAL_AI_TEMPERATURE > 0,
                    pad_token_id=pad_id,
                    eos_token_id=self._tokenizer.eos_token_id,
                )
            prompt_length = input_ids.shape[-1]
            generated = outputs[0][prompt_length:]
            return self._tokenizer.decode(generated, skip_special_tokens=True).strip()
        except Exception as exc:
            logger.exception("Fine-tuned model generation failed: %s", exc)
            self._model = None
            self._tokenizer = None
            raise LegalAssistantUnavailable(f"Fine-tuned model generation failed: {exc}") from exc

    def _keyword_overlap(self, sentence: str, question_words: set[str]):
        sentence_words = {
            word.strip(".,:;!?()[]{}'\"").lower()
            for word in sentence.split()
            if len(word) > 2
        }
        return len(sentence_words & question_words)

    def _build_extraction_answer(self, question: str, context_chunks: list[str]) -> str:
        if not context_chunks:
            return (
                "I could not find relevant information in the uploaded document. "
                "Upload and analyze a document first, or ask a more specific question."
            )

        question_words = {
            word.strip(".,:;!?()[]{}'\"").lower()
            for word in question.split()
            if len(word) > 2
        }
        sentences = []
        for chunk in context_chunks:
            pieces = [part.strip() for part in chunk.replace("\n", " ").split(".") if part.strip()]
            sentences.extend(pieces)

        ranked = sorted(
            sentences,
            key=lambda s: self._keyword_overlap(s, question_words),
            reverse=True,
        )
        best = [s for s in ranked[:3] if s] or [context_chunks[0].strip()]

        if len(best) == 1:
            return f"Based on the uploaded document, {best[0].rstrip('.')}."
        return "Based on the uploaded document, the key points are: " + " ".join(
            f"{s.rstrip('.')}." for s in best
        )

    def get_status(self):
        from pathlib import Path
        import os

        model_path = self.model_path
        model_exists = model_path.exists()
        adapter_exists = (model_path / "adapter_config.json").exists()
        tokenizer_exists = any(
            (model_path / name).exists()
            for name in ("tokenizer.json", "tokenizer_config.json")
        )

        peft_available = self._is_dependency_available("peft")
        accelerate_available = self._is_dependency_available("accelerate")

        ollama_available = self._check_ollama() if settings.OLLAMA_ENABLED else False
        base_model = settings.LEGAL_AI_BASE_MODEL or "from adapter config"
        preferred = getattr(settings, "LEGAL_AI_PREFERRED_LLM", "fine_tuned").lower()

        if preferred == "fine_tuned" and model_exists:
            mode = "fine_tuned_model"
            if self._model is not None:
                message = "Fine-tuned legal model is loaded and ready."
            else:
                message = "Fine-tuned legal model is ready to be loaded on first question."
        elif settings.OLLAMA_ENABLED and ollama_available:
            mode = "ollama"
            message = f"Using local Ollama model '{settings.OLLAMA_MODEL}' for RAG-grounded answers."
        else:
            mode = "retrieval_fallback"
            if not model_exists:
                message = f"Model folder not found at {model_path}. Using retrieval fallback."
            else:
                message = "Using retrieval fallback for answers."

        return {
            "available": ollama_available or model_exists,
            "loaded": self._model is not None and self._tokenizer is not None,
            "adapter": adapter_exists,
            "tokenizer": tokenizer_exists,
            "peft": peft_available,
            "accelerate": accelerate_available,
            "path": str(model_path),
            "base_model": base_model,
            "resolved_base_model": self._resolved_base_model or base_model,
            "ollama_enabled": settings.OLLAMA_ENABLED,
            "ollama_available": ollama_available,
            "ollama_model": settings.OLLAMA_MODEL,
            "ollama_base_url": settings.OLLAMA_BASE_URL,
            "preferred_llm": getattr(settings, "LEGAL_AI_PREFERRED_LLM", "ollama"),
            "device": "cpu",
            "mode": mode,
            "message": message,
        }

    def reset_model(self):
        self._model = None
        self._tokenizer = None
        self._load_error = None
        self._resolved_base_model = None
        self._ollama_checked = False
        self._ollama_available = False

    def _is_dependency_available(self, module_name: str):
        try:
            __import__(module_name)
            return True
        except Exception:
            return False

    def _resolve_cached_repo_path(self, model_name: str | None):
        import os
        from pathlib import Path

        if not model_name or "/" not in model_name:
            return model_name

        owner, repo = model_name.split("/", 1)
        cache_roots = [Path.home() / ".cache" / "huggingface" / "hub"]

        hf_home = os.getenv("HF_HOME")
        if hf_home:
            cache_roots.insert(0, Path(hf_home) / "hub")

        local_appdata = os.getenv("LOCALAPPDATA")
        if local_appdata:
            cache_roots.append(Path(local_appdata) / "huggingface" / "hub")

        repo_dir_name = f"models--{owner}--{repo}"
        for cache_root in cache_roots:
            snapshots_dir = cache_root / repo_dir_name / "snapshots"
            if not snapshots_dir.exists():
                continue
            snapshot_paths = sorted(
                (p for p in snapshots_dir.iterdir() if p.is_dir()),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            for snap in snapshot_paths:
                if (snap / "config.json").exists():
                    return str(snap)
        return model_name

    def _path_has_model_weights(self, model_path):
        from pathlib import Path

        if not model_path:
            return False
        candidate = Path(model_path)
        return any(
            (candidate / f).exists()
            for f in (
                "model.safetensors",
                "model.safetensors.index.json",
                "pytorch_model.bin",
                "pytorch_model.bin.index.json",
            )
        )

    def answer_question(self, question: str, context_chunks: list[str], history=None):
        preferred = getattr(settings, "LEGAL_AI_PREFERRED_LLM", "fine_tuned").lower()

        if preferred == "fine_tuned":
            try:
                answer = self._call_fine_tuned(question, context_chunks, history=history)
                return {
                    "answer": answer,
                    "mode": "fine_tuned_model",
                    "used_context_chunks": len(context_chunks),
                }
            except LegalAssistantUnavailable as exc:
                logger.warning("Fine-tuned model unavailable (%s).", exc)
                if settings.OLLAMA_ENABLED and self._check_ollama():
                    logger.warning("Falling back to Ollama.")
                elif settings.LEGAL_AI_ALLOW_FALLBACK:
                    mode_name = "retrieval_fallback"
                    logger.warning("Ollama disabled. Using %s.", mode_name)
                    return {
                        "answer": self._build_extraction_answer(question, context_chunks),
                        "mode": mode_name,
                        "used_context_chunks": len(context_chunks),
                    }
                else:
                    raise

        if settings.OLLAMA_ENABLED and self._check_ollama():
            try:
                answer = self._call_ollama(question, context_chunks, history=history)
                if answer:
                    logger.info("Answer generated via Ollama for: %s", question[:50])
                    return {
                        "answer": answer,
                        "mode": "ollama",
                        "used_context_chunks": len(context_chunks),
                    }
            except Exception as exc:
                logger.warning("Ollama call failed, falling back: %s", exc)

        if preferred == "ollama":
            try:
                answer = self._call_fine_tuned(question, context_chunks, history=history)
                return {
                    "answer": answer,
                    "mode": "fine_tuned_model",
                    "used_context_chunks": len(context_chunks),
                }
            except LegalAssistantUnavailable as exc:
                if not settings.LEGAL_AI_ALLOW_FALLBACK:
                    raise

        mode_name = "retrieval_fallback"
        logger.warning("All LLM backends unavailable. Using %s.", mode_name)
        return {
            "answer": self._build_extraction_answer(question, context_chunks),
            "mode": mode_name,
            "used_context_chunks": len(context_chunks),
        }


legal_assistant_service = LegalAssistantService()
