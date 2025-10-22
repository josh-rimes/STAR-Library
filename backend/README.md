# Backend (FastAPI)

This folder contains a minimal FastAPI backend using SQLModel and PostgreSQL (configurable via DATABASE_URL).

Quick start (Windows PowerShell):

1. Create and activate a virtual environment (optional but recommended):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set `DATABASE_URL` to your Postgres URL, e.g.:

```
DATABASE_URL=postgresql://user:password@localhost:5432/starlib
```

If you don't set `DATABASE_URL`, the app falls back to a local SQLite file `dev.db`.

4. Run the app:

```powershell
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/docs for the interactive API docs.
