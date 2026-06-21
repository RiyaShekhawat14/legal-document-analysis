import os
import json
import sqlite3
import tempfile
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


def _resolve_data_dir():
    candidates = [BASE_DIR / "data"]
    local_appdata = os.getenv("LOCALAPPDATA")

    if local_appdata:
        candidates.append(Path(local_appdata) / "LegalEasyAI")

    candidates.append(Path(tempfile.gettempdir()) / "LegalEasyAI")

    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            probe = candidate / ".sqlite_probe.db"
            with sqlite3.connect(probe) as connection:
                connection.execute("CREATE TABLE IF NOT EXISTS probe (id INTEGER PRIMARY KEY)")
            try:
                probe.unlink(missing_ok=True)
            except OSError:
                pass
            return candidate
        except (OSError, sqlite3.Error):
            continue

    fallback = BASE_DIR / "data"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


DATA_DIR = _resolve_data_dir()
RUNTIME_SETTINGS_PATH = DATA_DIR / "runtime_settings.json"


def _build_sqlite_url(path: Path):
    return f"sqlite:///{path.as_posix()}"


def _sqlite_path_from_url(url: str):
    prefix = "sqlite:///"
    if not url.startswith(prefix):
        return None
    return Path(url.replace(prefix, "", 1))


def _is_sqlite_path_usable(path: Path):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(path) as connection:
            connection.execute("CREATE TABLE IF NOT EXISTS startup_probe (id INTEGER PRIMARY KEY)")
            connection.execute("INSERT INTO startup_probe DEFAULT VALUES")
            connection.execute("DELETE FROM startup_probe")
            connection.commit()
        return True
    except sqlite3.Error:
        return False


def _resolve_writable_directory(path: Path):
    candidates = [
        path,
        BASE_DIR / "data" / path.name,
        Path(tempfile.gettempdir()) / "LegalEasyAI" / path.name,
    ]

    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            probe = candidate / ".write_probe"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink(missing_ok=True)
            return candidate
        except OSError:
            continue

    fallback = BASE_DIR / "data" / path.name
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


PRIMARY_SQLITE_PATH = DATA_DIR / "legal_docs.db"
FALLBACK_SQLITE_PATH = Path(tempfile.gettempdir()) / "LegalEasyAI" / "legal_docs_runtime.db"
DEFAULT_SQLITE_URL = _build_sqlite_url(
    PRIMARY_SQLITE_PATH if _is_sqlite_path_usable(PRIMARY_SQLITE_PATH) else FALLBACK_SQLITE_PATH
)


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Legal Document Analyzer"
    VERSION: str = "1.0.0"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: str = os.getenv(
        "CORS_ORIGINS",
        ",".join(
            [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "http://[::1]:5173",
                "http://localhost:5174",
                "http://127.0.0.1:5174",
                "http://[::1]:5174",
                "http://localhost:4173",
                "http://127.0.0.1:4173",
                "http://[::1]:4173",
                "https://legal-document-analysis-alpha.vercel.app",
                "https://legal-document-analysis.vercel.app",
            ]
        ),
    )

    # Uploads
    UPLOAD_DIR: str = "uploads"

    # Vector DB
    VECTOR_DB_BACKEND: str = "qdrant"
    VECTOR_DB_COLLECTION: str = "legal_document_chunks"
    VECTOR_DB_PATH: str = str(DATA_DIR / "qdrant")

    # Legal assistant
    LEGAL_AI_MODEL_PATH: str = "models/legal_lora_model"
    LEGAL_AI_BASE_MODEL: str | None = None
    LEGAL_AI_MAX_NEW_TOKENS: int = 256
    LEGAL_AI_TEMPERATURE: float = 0.2
    LEGAL_AI_TOP_K: int = 4
    LEGAL_AI_ALLOW_FALLBACK: bool = True
    LEGAL_AI_CPU_SAFE_MODE: bool = True
    LEGAL_AI_ENABLE_FINE_TUNED_ON_CPU: bool = False
    LEGAL_AI_PREFERRED_LLM: str = os.getenv("LEGAL_AI_PREFERRED_LLM", "ollama")

    # Ollama (local LLM backend for RAG chat)
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3:8b")
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "90"))
    OLLAMA_ENABLED: bool = False

    # API-based inference (for deployment without local models)
    HF_CHAT_MODEL: str = os.getenv("HF_CHAT_MODEL", "Qwen/Qwen2.5-0.5B-Instruct")
    HF_SUMMARY_MODEL: str = os.getenv("HF_SUMMARY_MODEL", "facebook/bart-large-cnn")
    HF_TRANSLATION_MODEL: str = os.getenv("HF_TRANSLATION_MODEL", "Helsinki-NLP/opus-mt-en-hi")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    USE_API_LLM: bool = True

    # ML Models
    MODEL_PATH: str = "ml/artifacts/risk_model.pkl"
    TFIDF_PATH: str = "ml/artifacts/tfidf.pkl"
    LABEL_ENCODER_PATH: str = "ml/artifacts/label_encoder.pkl"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

    # API Keys
    OPENAI_API_KEY: str | None = None
    HUGGINGFACE_API_KEY: str | None = None

    class Config:
        env_file = str(BASE_DIR / ".env")
        extra = "allow"   # Important fix


settings = Settings()

if settings.DATABASE_URL.startswith("sqlite:///./"):
    relative_path = settings.DATABASE_URL.replace("sqlite:///./", "", 1)
    if relative_path.endswith("legal_docs.db"):
        settings.DATABASE_URL = DEFAULT_SQLITE_URL
    else:
        settings.DATABASE_URL = _build_sqlite_url(BASE_DIR / relative_path)

sqlite_path = _sqlite_path_from_url(settings.DATABASE_URL)
if sqlite_path is not None and not _is_sqlite_path_usable(sqlite_path):
    settings.DATABASE_URL = _build_sqlite_url(FALLBACK_SQLITE_PATH)
    sqlite_path = _sqlite_path_from_url(settings.DATABASE_URL)

if sqlite_path is not None:
    RUNTIME_SETTINGS_PATH = sqlite_path.parent / "runtime_settings.json"

if not Path(settings.UPLOAD_DIR).is_absolute():
    settings.UPLOAD_DIR = str((BASE_DIR / settings.UPLOAD_DIR).resolve())

if not Path(settings.VECTOR_DB_PATH).is_absolute():
    settings.VECTOR_DB_PATH = str((BASE_DIR / settings.VECTOR_DB_PATH).resolve())

settings.VECTOR_DB_PATH = str(
    _resolve_writable_directory(Path(settings.VECTOR_DB_PATH)).resolve()
)

if not Path(settings.LEGAL_AI_MODEL_PATH).is_absolute():
    settings.LEGAL_AI_MODEL_PATH = str(
        (BASE_DIR / settings.LEGAL_AI_MODEL_PATH).resolve()
    )


def get_runtime_mode():
    return {
        "cpu_safe_mode": settings.LEGAL_AI_CPU_SAFE_MODE,
        "enable_fine_tuned_on_cpu": settings.LEGAL_AI_ENABLE_FINE_TUNED_ON_CPU,
    }


def _apply_runtime_mode(runtime_mode: dict):
    settings.LEGAL_AI_CPU_SAFE_MODE = bool(
        runtime_mode.get("cpu_safe_mode", settings.LEGAL_AI_CPU_SAFE_MODE)
    )
    settings.LEGAL_AI_ENABLE_FINE_TUNED_ON_CPU = bool(
        runtime_mode.get(
            "enable_fine_tuned_on_cpu",
            settings.LEGAL_AI_ENABLE_FINE_TUNED_ON_CPU,
        )
    )


def load_runtime_mode():
    if not RUNTIME_SETTINGS_PATH.exists():
        return get_runtime_mode()

    try:
        runtime_mode = json.loads(RUNTIME_SETTINGS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return get_runtime_mode()

    _apply_runtime_mode(runtime_mode)
    return get_runtime_mode()


def _persist_runtime_mode(runtime_mode: dict):
    global RUNTIME_SETTINGS_PATH

    candidate_paths = [
        RUNTIME_SETTINGS_PATH,
        Path(tempfile.gettempdir()) / "LegalEasyAI" / "runtime_settings.json",
        BASE_DIR / "data" / "runtime_settings.json",
    ]

    for candidate in candidate_paths:
        try:
            candidate.parent.mkdir(parents=True, exist_ok=True)
            candidate.write_text(
                json.dumps(runtime_mode, indent=2),
                encoding="utf-8",
            )
            RUNTIME_SETTINGS_PATH = candidate
            return
        except OSError:
            continue


def save_runtime_mode(cpu_safe_mode: bool, enable_fine_tuned_on_cpu: bool):
    runtime_mode = {
        "cpu_safe_mode": bool(cpu_safe_mode),
        "enable_fine_tuned_on_cpu": bool(enable_fine_tuned_on_cpu),
    }
    _apply_runtime_mode(runtime_mode)
    _persist_runtime_mode(runtime_mode)
    return get_runtime_mode()


load_runtime_mode()


def get_cors_origins():
    origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
    if "*" in origins:
        return ["*"]
    return origins
