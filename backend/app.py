import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from auth import auth_routes
from config.settings import get_cors_origins, settings
from database.db import engine, ensure_schema
from database.models import Base
from rag.rag_routes import router as rag_router
from routes import analyze, chat, compare, documents, translate

Base.metadata.create_all(bind=engine)
ensure_schema()
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Legal Document Analysis API",
    description="API for analyzing legal documents, providing insights, and facilitating communication.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=("*" not in get_cors_origins()),
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(analyze.router, prefix="/analyze", tags=["Analyze"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(compare.router, prefix="/compare", tags=["Compare"])
app.include_router(translate.router, prefix="/translate", tags=["Translate"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(rag_router, prefix="/rag", tags=["RAG"])


@app.get("/")
def root():
    return {
        "message": "Welcome to the Legal Document Analysis API",
        "version": app.version,
    }


@app.get("/health")
def health():
    return {"status": "ok"}
