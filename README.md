# STAR-library

This repository contains a minimal STAR Library demo: a FastAPI backend (SQLModel) and a Vite + React frontend.

Overview

- Backend: `backend` (FastAPI, SQLModel). Seeds the DB on startup when empty.
- Frontend: `frontend` (React, Vite). Assumes backend is available at http://127.0.0.1:8000.

Recommended local setup (Windows PowerShell)

1. Backend — create a venv, install deps, set env, run

```powershell
cd backend
# create & activate venv (recommended)
python -m venv .venv
# If PowerShell blocks activation, run once:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1

# install Python deps
python -m pip install --upgrade pip
pip install -r requirements.txt

# copy .env.example -> .env and edit DATABASE_URL if you want Postgres
# default (no .env) falls back to sqlite: DATABASE_URL=sqlite:///./dev.db

# run the server (use module form to avoid PATH issues)
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Notes:

- On startup the backend will create tables and seed sample data (4 authors, 15 books, 5 readers) if the DB is empty.

2. Frontend — install deps and run dev server

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 to view the app. The frontend queries the backend at http://127.0.0.1:8000 by default.

Quick checks:

- API docs: http://127.0.0.1:8000/docs
- Check seeded counts (PowerShell):

```powershell
# after backend is running
(Invoke-RestMethod http://127.0.0.1:8000/authors).Count
(Invoke-RestMethod http://127.0.0.1:8000/books).Count
(Invoke-RestMethod http://127.0.0.1:8000/readers).Count
(Invoke-RestMethod http://127.0.0.1:8000/book-readers).Count
```
