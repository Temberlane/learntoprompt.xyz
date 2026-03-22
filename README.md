# learntoprompt.xyz

A website for those who are too scared (or a bit stubborn) to learn to how to use AI to make their lives easier.

## Project Structure

```
.
├── backend/   # FastAPI + SQLAlchemy + PostgreSQL
└── frontend/  # React + TypeScript + Vite
```

## Backend

Built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

### Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

### Configuration

Set the `DATABASE_URL` environment variable (defaults to a local PostgreSQL instance):

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/learntoprompt"
```

### Run

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

### Database Migrations

```bash
cd backend
alembic upgrade head
```

### Tests

```bash
cd backend
pytest
```

Tests use an in-memory SQLite database — no PostgreSQL required.

---

## Frontend

Built with **React**, **TypeScript**, and **Vite**.

### Setup

```bash
cd frontend
npm install
```

### Run

```bash
npm run dev
```

The app will be available at `http://localhost:5173`.  
API requests are proxied to `http://localhost:8000` automatically.

### Build

```bash
npm run build
```

### Tests

```bash
npm test
```

