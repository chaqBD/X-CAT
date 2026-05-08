# X-CAT — Supply Chain Category Analysis Platform

A web-based procurement analytics platform. Upload CSV/Excel datasets and get interactive dashboards for spend, category, supplier, inventory, budget, and geographic analysis.

---

## Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL 15+ (or Docker)
- Docker + Docker Compose (recommended)

---

## Quick Start (Docker)

```bash
# 1. Clone and enter project
cd x-cat

# 2. Copy environment file
cp backend/.env.example backend/.env

# 3. Start all services
docker-compose up --build

# 4. Run migrations (first time only)
docker-compose exec backend alembic upgrade head

# 5. Open browser
# Frontend: http://localhost:5173
# API docs:  http://localhost:8000/docs
```

---

## Local Development (without Docker)

### Backend

```bash
cd backend

# Create & activate virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt

# Copy and configure env
cp .env.example .env
# Edit DATABASE_URL to point to your PostgreSQL instance

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Opens at http://localhost:5173
```

---

## Supported Dataset Types

| Type | Required Columns |
|---|---|
| Procurement Transactions | date, category, supplier, total_cost |
| Supplier Data | supplier_name, country |
| Inventory | product, stock_level, reorder_level |
| Budget | category, budget, actual_spend |

---

## User Roles

| Role | Permissions |
|---|---|
| Admin | Full access |
| Analyst | Upload data, view all dashboards |
| Viewer | Read-only dashboards |

---

## API Documentation

FastAPI auto-generates interactive docs at `http://localhost:8000/docs`

---

## Project Structure

```
x-cat/
├── backend/           FastAPI + SQLAlchemy + Pandas
├── frontend/          React + Vite + Tailwind CSS + Recharts
├── docker-compose.yml Local dev environment
└── railway.toml       Railway deployment config
```

---

## Deployment (Railway)

1. Create a new Railway project
2. Add a PostgreSQL service
3. Deploy the backend service pointing to `backend/Dockerfile`
4. Set environment variables: `DATABASE_URL`, `SECRET_KEY`
5. Deploy frontend separately (Vercel / Netlify recommended for static sites)
