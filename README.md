# Legal Document Analyzer ⚖️

AI-powered legal contract review tool that turns dense legal documents into clear, actionable insights.

Live app: https://legal-document-analysis-alpha.vercel.app

## What it does

Upload any legal contract (PDF/TXT) and get instant analysis:

- Clause extraction across 12 categories (Payment, Termination, Liability, Confidentiality, IP, etc.)
- Red-flag detection for 9 high-risk patterns (unlimited liability, auto-renewal, non-compete, unilateral termination, and more)
- ML-based risk scoring with confidence scores per clause
- Executive summary in English and Hindi
- Risk-based recommendations
- Ask follow-up questions about the document with RAG-powered chat
- Compare two contracts side by side
- 21 professional clause templates for reference

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, Vite, React Router, Tailwind CSS |
| Backend | FastAPI, SQLAlchemy, SQLite |
| ML | scikit-learn (TF-IDF + LinearSVC), rule-based fallback |
| RAG | FAISS vector search, sentence-transformers embeddings |
| LLM | HuggingFace Inference API, fine-tuned Qwen2.5-0.5B + LoRA |
| Auth | JWT (python-jose), pbkdf2_sha256 password hashing |
| Deploy | Render (backend), Vercel (frontend) |

## Architecture

```
User ──→ React Frontend (Vercel)
              │
              ▼
         FastAPI Backend (Render)
              │
     ┌────────┼────────┐
     ▼        ▼        ▼
  SQLite   ML Model   RAG Pipeline
  (users,  (risk      (embed → FAISS →
   docs,    scoring)   retrieve → LLM)
   clauses)
```

## Key Features

### Document Analysis
- Upload PDF or TXT contracts
- Automatic clause splitting and categorization into 12 types
- Red-flag detection for risky language patterns
- Per-clause risk classification (High/Medium/Low) with confidence scores
- Overall document risk assessment
- Bilingual summaries (English + Hindi)
- Actionable advice based on risk level

### RAG Chat
- Ask questions about your uploaded contract
- Retrieves relevant chunks using vector similarity search
- Generates grounded answers using LLM (no hallucination)
- General legal Q&A without document upload
- Conversation history support

### Document Comparison
- Upload two contracts and compare side by side
- Risk levels, summaries, and clause-by-clause breakdown

### Clause Templates
- 21 professionally drafted templates across 7 clause types
- Three versions each: standard, pro-vendor, pro-client
- Useful for understanding what fair terms look like

## API Endpoints

```
POST   /auth/register          Register new user
POST   /auth/login             Login
GET    /auth/me                Get current user
POST   /analyze/analyze-risk   Upload & analyze document
GET    /documents/             List user's documents
GET    /documents/{id}         Get document clauses
DELETE /documents/{id}         Delete document
POST   /chat/ask               Ask a question
GET    /chat/status            Get assistant status
POST   /compare/               Compare two documents
POST   /translate/             Translate to Hindi
GET    /health                 Health check
GET    /docs                   Swagger API docs
```

## Deployment

Backend: https://legal-document-analysis.onrender.com
Frontend: https://legal-document-analysis-alpha.vercel.app
API Docs: https://legal-document-analysis.onrender.com/docs

## Local Development

```powershell
# Backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
uvicorn backend.app:app --reload

# Frontend
npm --prefix frontend install
cp frontend/.env.example frontend/.env
npm --prefix frontend run dev
```

## What I Learned

- Building a full-stack AI app with RAG (Retrieval-Augmented Generation)
- Fine-tuning a Qwen2.5 LLM with LoRA for legal domain-specific responses
- Designing graceful fallback chains (API LLM → local model → rule-based)
- Deploying a monorepo with separate frontend (Vercel) and backend (Render)
- Handling CORS, environment variables, and production configuration
- Writing comprehensive E2E tests for API validation

## Future Improvements

- Postgres for multi-user production
- DOCX file support
- PDF export with highlighted risk clauses
- User collaboration and sharing
- E-signature integration

---

GitHub: https://github.com/RiyaShekhawat14/legal-document-analysis
