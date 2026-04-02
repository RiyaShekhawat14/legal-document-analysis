from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import engine
from database.models import Base

from routes import analyze, chat, compare, translate, documents
from auth import auth_routes

from rag.rag_routes import router as rag_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Legal Document Analysis API",
    description="API for analyzing legal documents, providing insights, and facilitating communication.",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(analyze.router, prefix="/analyze", tags=["Analyze"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(compare.router, prefix="/compare", tags=["Compare"])
app.include_router(translate.router, prefix="/translate", tags=["Translate"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(rag_router, prefix="/rag", tags=["RAG"]) 
@app.get("/")

def root():
    return {"message": "Welcome to the Legal Document Analysis API"}