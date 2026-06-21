# Legal Document Analyzer

Legal Document Analyzer is a full-stack legal review app with:

- secure authentication
- document upload and clause risk analysis
- English and Hindi summaries
- side-by-side document comparison
- RAG-based chat over the latest analyzed document
- a fine-tuned legal assistant fallback path when the full model is unavailable

## Stack

- Backend: FastAPI, SQLAlchemy, SQLite, Qdrant or FAISS, sentence-transformers
- Frontend: React, Vite, React Router
- ML/RAG: local classifier for clause risk, embedding-based retrieval, optional fine-tuned legal LLM

## App Workflow

1. A user registers or logs in.
2. The frontend stores the bearer token and sends it on protected API requests.
3. The user uploads a legal document from the home page.
4. The backend extracts text, splits clauses, predicts clause risk, builds summaries, and stores the document under that user.
5. The same upload is indexed into that user’s RAG session.
6. The result page shows summary, overall risk, clause insights, and advice.
7. The user can open chat and ask follow-up questions grounded in the latest indexed document.
8. The user can view history, inspect stored clause results, compare two documents, or delete prior uploads.

## Run Locally

### Backend

1. Create and activate a virtual environment.
2. Install dependencies:

```powershell
pip install -r backend/requirements.txt
```

3. Copy env values:

```powershell
Copy-Item backend/.env.example backend/.env
```

4. Start the API:

```powershell
uvicorn backend.app:app --reload
```

Backend health endpoint:

```text
GET /health
```

### Frontend

1. Copy env values:

```powershell
Copy-Item frontend/.env.example frontend/.env
```

2. Install dependencies:

```powershell
npm --prefix frontend install
```

3. Start the client:

```powershell
npm --prefix frontend run dev
```

## Repo Scripts

From the repo root:

```powershell
npm run frontend:dev
npm run frontend:build
npm run frontend:lint
```

## Production Notes

- Set a strong `SECRET_KEY`.
- Set `CORS_ORIGINS` to your deployed frontend origin.
- Keep model artifacts out of Git unless you intentionally version them.
- The backend currently falls back gracefully when the full legal assistant model is unavailable.
- SQLite is fine for local and single-user deployments; move to Postgres for multi-user production.

## Verified Checks

- Auth register/login/me
- Protected route enforcement
- Analyze upload flow
- History listing and delete flow
- Compare flow
- RAG chat flow
- Frontend lint
- Frontend production build
