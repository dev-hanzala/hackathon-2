# Developer Quickstart: Phase II

**Date**: 2026-01-10  
**Phase**: 1 (Design)  
**Purpose**: Get the development environment set up and running first task

---

## Prerequisites

Ensure you have these installed:
- **Python**: 3.13+ (`python --version`)
- **Node.js**: 20+ (`node --version`)
- **npm/pnpm**: 10+ (`npm --version`)
- **Git**: Latest (`git --version`)
- **Docker & Docker Compose**: For local PostgreSQL (optional; can use Neon directly)

---

## Environment Setup

### 1. Clone Repository & Create Branch

```bash
cd /path/to/hackathon-2

# Switch to feature branch
git checkout 002-phase2-webapp

# Create local feature branch for your work (if not already on it)
git pull origin 002-phase2-webapp
```

### 2. Backend Setup

```bash
cd backend/

# Create Python virtual environment
python3.13 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r pyproject.toml

# Create .env file for local development
cat > .env.local << 'EOF'
DATABASE_URL=postgresql://postgres:password@localhost:5432/todo_dev
BETTER_AUTH_SECRET=dev-secret-key-change-in-production
ENVIRONMENT=development
DEBUG=true
EOF

# Run database migrations
alembic upgrade head

# Start backend server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend running at**: http://localhost:8000  
**API docs**: http://localhost:8000/api/v1/docs

### 3. Database Setup (Local PostgreSQL)

Option A: Using Docker Compose (easiest)

```bash
# From repo root
docker-compose up -d

# Verify database is running
psql postgresql://postgres:password@localhost:5432/todo_dev -c "SELECT 1"
```

Option B: Using Neon (cloud, skip local database)

```bash
# Update .env.local with Neon connection string from dashboard
DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/todo_dev
```

### 4. Frontend Setup

```bash
cd frontend/

# Install dependencies
npm install  # or pnpm install

# Create .env.local
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
EOF

# Start development server
npm run dev  # or pnpm dev
```

**Frontend running at**: http://localhost:3000

---

## First Run: Manual Testing

### 1. Test Backend API

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Register new user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123"}'

# Sign in
curl -X POST http://localhost:8000/api/v1/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123"}' \
  -c cookies.txt  # Save session cookies

# Create task (using cookie auth)
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title":"Buy groceries"}'

# List tasks
curl http://localhost:8000/api/v1/tasks -b cookies.txt

# View API docs
# Open browser to http://localhost:8000/api/v1/docs
```

### 2. Test Frontend

1. Open http://localhost:3000 in browser
2. Click "Sign Up"
3. Register with email `test@example.com`, password `SecurePass123`
4. Should redirect to task list (empty)
5. Add task: type "Buy groceries" → click "Add Task"
6. Task appears in list
7. Click checkbox to mark complete
8. Task moves to archive

---

## Running Tests

### Backend Unit Tests

```bash
cd backend/

# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_models.py

# Run integration tests
pytest tests/integration/
```

### Backend API Contract Tests

```bash
cd backend/

# Validate API against OpenAPI schema
pytest tests/contract/test_api_contracts.py

# Generate coverage report
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

### Frontend Tests

```bash
cd frontend/

# Run all tests
npm run test

# Watch mode (re-run on file changes)
npm run test -- --watch

# Coverage report
npm run test -- --coverage
```

---

## Project Layout Reference

```
backend/
├── src/
│   ├── main.py              # FastAPI app initialization
│   ├── models/
│   │   ├── user.py          # User SQLModel
│   │   └── task.py          # Task SQLModel
│   ├── services/
│   │   ├── auth_service.py  # Auth business logic
│   │   └── task_service.py  # Task CRUD logic
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py      # Auth endpoints
│   │       ├── tasks.py     # Task endpoints
│   │       └── health.py    # Health check
│   ├── db/
│   │   ├── database.py      # DB connection, session
│   │   ├── models.py        # SQLModel ORM definitions
│   │   └── migrations/      # Alembic scripts
│   └── config.py            # Config, env vars
├── tests/
│   ├── unit/                # Service logic tests
│   ├── integration/         # API + DB tests
│   └── contract/            # OpenAPI validation
└── pyproject.toml           # Dependencies

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home page
│   │   ├── auth/
│   │   │   ├── signin/page.tsx
│   │   │   └── signup/page.tsx
│   │   ├── tasks/
│   │   │   └── page.tsx     # Main task list
│   │   └── api/             # Next.js server routes
│   ├── components/
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   └── TaskForm.tsx
│   ├── lib/
│   │   ├── api-client.ts    # Fetch wrapper
│   │   ├── hooks/
│   │   │   ├── useTasks.ts
│   │   │   └── useAuth.ts
│   │   └── types.ts         # Shared types
│   └── styles/
│       └── globals.css      # TailwindCSS
├── tests/
│   ├── unit/
│   └── integration/
└── package.json
```

---

## Common Development Tasks

### Add a New Endpoint

1. **Define schema** (if needed): `backend/src/api/schemas.py`
2. **Add database model**: `backend/src/models/`
3. **Add service logic**: `backend/src/services/`
4. **Add endpoint**: `backend/src/api/v1/tasks.py` (or new file)
5. **Write tests**: `backend/tests/integration/` (test the endpoint)
6. **Test manually**: `curl` or use OpenAPI docs at `/api/v1/docs`
7. **Update OpenAPI spec**: `specs/002-phase2-webapp/contracts/tasks-api.openapi.yaml`

### Add a New Frontend Component

1. **Create component**: `frontend/src/components/MyComponent.tsx`
2. **Write unit test**: `frontend/tests/unit/components/MyComponent.test.tsx`
3. **Use in page**: Import and integrate into `frontend/src/app/tasks/page.tsx`
4. **Test manually**: Load page in browser, verify rendering and interaction
5. **Test integration**: Add integration test if component interacts with API

### Run Type Checking

```bash
# Backend (mypy)
cd backend/
mypy src/

# Frontend (TypeScript compiler)
cd frontend/
npm run type-check
```

### Lint & Format Code

```bash
# Backend (ruff)
cd backend/
ruff check src/
ruff format src/  # Auto-format

# Frontend (ESLint + Prettier)
cd frontend/
npm run lint
npm run format
```

---

## Debugging

### Backend Debugging

```bash
# Using Python debugger (pdb)
# Add this line where you want to debug:
breakpoint()

# Run with pytest
pytest tests/integration/test_task_api.py -s  # -s shows print output

# Check logs
# Look at DEBUG=true in .env.local for verbose logs
```

### Frontend Debugging

```bash
# Browser DevTools
# Open http://localhost:3000 → Right-click → Inspect
# Go to Console tab to see logs (use console.log in components)

# React DevTools browser extension (recommended)
# Install React Developer Tools from Chrome Web Store
```

### API Testing with Postman

1. Import OpenAPI spec: `specs/002-phase2-webapp/contracts/tasks-api.openapi.yaml`
2. Set base URL: `http://localhost:8000/api/v1`
3. Create requests for each endpoint
4. Save requests in collection for reuse

---

## Troubleshooting

**Problem**: "psycopg2.OperationalError: could not connect to server"  
**Solution**: Ensure PostgreSQL is running (`docker-compose up -d` or Neon connection string is correct)

**Problem**: "ModuleNotFoundError: No module named 'fastapi'"  
**Solution**: Activate virtual environment and run `pip install -r pyproject.toml`

**Problem**: "NEXT_PUBLIC_API_URL is not defined"  
**Solution**: Create `.env.local` in frontend/ directory with `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`

**Problem**: "Port 8000 already in use"  
**Solution**: Kill process using port 8000: `lsof -i :8000` then `kill -9 <PID>` (or use different port: `uvicorn src.main:app --port 8001`)

**Problem**: "Type errors in TypeScript"  
**Solution**: Run `npm run type-check` to see all type errors; fix by ensuring proper types in components

---

## Next Steps

1. **Run `/sp.tasks`** to generate implementation task list
2. **Pick first task** from list (likely auth service or data model)
3. **Write tests first** (Red phase: test fails)
4. **Get user approval** on test approach
5. **Implement to pass tests** (Green phase)
6. **Refactor** if needed (Refactor phase)
7. **Create PHR** for each task completed

---

## Quick Links

- **API Documentation (live)**: http://localhost:8000/api/v1/docs
- **OpenAPI Spec**: `specs/002-phase2-webapp/contracts/tasks-api.openapi.yaml`
- **Data Model**: `specs/002-phase2-webapp/data-model.md`
- **Implementation Plan**: `specs/002-phase2-webapp/plan.md`
- **Feature Spec**: `specs/002-phase2-webapp/spec.md`

---

## Getting Help

- Check Constitution: `.specify/memory/constitution.md`
- Review research: `specs/002-phase2-webapp/research.md`
- Look at tests as examples: `backend/tests/`, `frontend/tests/`
- Read docstrings in code: `backend/src/`, `frontend/src/`
