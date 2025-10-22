# STAR-library

This project represents a simplified online library system. A single (already signed-in) user should be able to view book and author data and see some basic statistics.

Backend (FastAPI)

- Location: `backend`
- Run (Powershell):

```powershell
cd backend
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# create .env and set DATABASE_URL for Postgres, e.g.
# DATABASE_URL=postgresql://user:password@localhost:5432/starlib
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend (React + Vite)

- Location: `frontend`
- Run (Powershell):

```powershell
cd frontend
npm install
npm run dev
```

The frontend expects the backend at `http://127.0.0.1:8000` by default.
