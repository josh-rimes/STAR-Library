# Backend (FastAPI)

This folder contains the FastAPI backend. It uses SQLModel for models/ORM and supports PostgreSQL via `DATABASE_URL`. If no `DATABASE_URL` is provided the app falls back to a local SQLite file `dev.db`.

Features

- Creates database tables on startup
- Seeds example data (4 authors, 15 books, 5 readers) on first run
- Exposes CRUD endpoints for Authors, Books, Readers, and BookReader associations

Quick start (Windows PowerShell)

```powershell
cd backend
# create & activate venv (recommended)
python -m venv .venv
# may need to allow script execution once:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1

# install deps
python -m pip install --upgrade pip
pip install -r requirements.txt

# copy .env.example -> .env and edit DATABASE_URL for Postgres if desired
# default: use SQLite at ./dev.db

# run the server (use python -m to avoid PATH issues)
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Seeding & troubleshooting

- On first successful startup the app will insert seed data automatically. If you want to run seeding manually (and see errors) use:

```powershell
python -c "from app.db import seed_data; seed_data()"
```

- If seeding fails with Postgres connection errors, check `backend/.env` and ensure Postgres is running and credentials are correct.

API docs

- Open the interactive docs at: http://127.0.0.1:8000/docs
