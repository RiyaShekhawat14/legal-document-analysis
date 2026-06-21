# Legal Document Analyzer

AI-powered legal contract review tool with clause extraction, risk scoring, bilingual summaries, and RAG-based chat.

## Features

- **Authentication** — JWT-based register/login with per-user document isolation
- **Upload & Analyze** — PDF/TXT contracts → clause splitting (12 categories), red-flag detection (9 patterns), ML risk scoring, English + Hindi summaries, risk-based advice
- **RAG Chat** — Ask questions about your uploaded contract; retrieves relevant chunks and generates grounded answers via HuggingFace API or OpenAI API
- **General Q&A** — Ask legal questions without any document (knowledge base of 10 legal topics)
- **Compare** — Upload two contracts side-by-side for risk/summary comparison
- **History** — View/delete past analyzed documents (user-scoped)
- **Clause Templates** — 21 professional clause templates (7 types x 3 versions)

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite, FAISS, sentence-transformers (optional)
- **Frontend:** React 19, Vite, React Router
- **LLM:** HuggingFace Inference API or OpenAI API (no local model required for deployment)
- **ML:** scikit-learn classifier with rule-based fallback

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login (JSON body) |
| GET | `/auth/me` | Get current user |
| POST | `/analyze/analyze-risk` | Upload & analyze document |
| GET | `/analyze/clause-templates/types` | List clause template types |
| GET | `/analyze/clause-templates/{type}` | Get specific template |
| GET | `/analyze/clause-templates/{type}/compare` | Compare template versions |
| POST | `/chat/ask` | Ask a question (general or document-specific) |
| GET | `/chat/status` | Get assistant + document status |
| POST | `/chat/mode` | Switch LLM mode |
| GET | `/documents/` | List user's documents |
| GET | `/documents/{id}` | Get document clauses |
| DELETE | `/documents/{id}` | Delete document |
| POST | `/compare/` | Compare two documents |
| POST | `/translate/` | Translate text to Hindi |
| GET | `/health` | Health check |

## Run Locally

### Backend

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend/requirements.txt
Copy-Item backend/.env.example backend/.env
uvicorn backend.app:app --reload
```

### Frontend

```powershell
npm --prefix frontend install
Copy-Item frontend/.env.example frontend/.env
npm --prefix frontend run dev
```

Open http://localhost:5173

## Deploy to Render

The repo includes a `render.yaml` for one-click deployment.

1. Go to [render.com](https://render.com) → New → Web Service
2. Connect your GitHub repo
3. Set environment variables:
   - `HUGGINGFACE_API_KEY` — your HF token (get one at https://huggingface.co/settings/tokens)
   - `SECRET_KEY` — a random string
   - `USE_API_LLM` — `true`
4. Deploy

The backend works without any API key (falls back to extractive summary and retrieval-based chat), but for full LLM chat you need a HuggingFace or OpenAI key.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `supersecretkey` | JWT signing key |
| `DATABASE_URL` | `sqlite:///./data/legal_docs.db` | Database URL |
| `HUGGINGFACE_API_KEY` | — | HuggingFace API token |
| `OPENAI_API_KEY` | — | OpenAI API key (optional) |
| `USE_API_LLM` | `true` | Use API-based LLM (no local model) |
| `OLLAMA_ENABLED` | `false` | Enable Ollama local LLM |
| `HF_CHAT_MODEL` | `Qwen/Qwen2.5-0.5B-Instruct` | HF model for chat |
| `HF_SUMMARY_MODEL` | `facebook/bart-large-cnn` | HF model for summary |
| `HF_TRANSLATION_MODEL` | `Helsinki-NLP/opus-mt-en-hi` | HF model for translation |
| `CORS_ORIGINS` | localhost origins | Allowed CORS origins |
| `VECTOR_DB_BACKEND` | `faiss` | Vector store backend |

## License

MIT
