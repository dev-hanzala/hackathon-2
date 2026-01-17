# Todo API Backend

RESTful API backend for the Todo application built with FastAPI, SQLModel, and PostgreSQL.

## Features

- **JWT Authentication**: Secure user registration and signin
- **Task Management**: Full CRUD operations for todo tasks
- **Data Isolation**: Users can only access their own tasks
- **High Performance**: Optimized database queries with composite indexes
- **Production Ready**: Comprehensive logging and health checks
- **Auto-Generated Docs**: Interactive API documentation at `/api/v1/docs`

## Tech Stack

- **Framework**: FastAPI 0.115.0+
- **ORM**: SQLModel 0.0.16+ (built on SQLAlchemy 2.0+)
- **Database**: PostgreSQL (Neon serverless in production)
- **Driver**: psycopg 3.3.2
- **Auth**: JWT with python-jose[cryptography]
- **Password Hashing**: passlib with bcrypt 4.3.0
- **Migrations**: Alembic 1.14.0+
- **Testing**: pytest 8.0.0+, pytest-asyncio
- **Package Manager**: uv (modern pip/venv replacement)

## Prerequisites

- Python 3.11+
- uv (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- PostgreSQL database (local or Neon cloud)

## Quick Start

### 1. Installation

```bash
# Clone repository (if not already)
cd backend

# Install dependencies
uv sync

# Or manually:
uv pip install -e .
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

**Required environment variables:**
```bash
DATABASE_URL=postgresql+psycopg://user:pass@host:port/db?sslmode=require
BETTER_AUTH_SECRET=<32+ character secret>
DEBUG=true
ENVIRONMENT=development
ALLOWED_ORIGINS=["http://localhost:3000"]
```

**Generate auth secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Database Setup

```bash
# Run migrations (automatically creates tables)
uv run alembic upgrade head

# Or migrations run automatically on app startup
```

### 4. Run Development Server

```bash
# Start server with hot reload
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or use the main script
uv run python -m src.main
```

Server runs at: **http://localhost:8000**

### 5. Verify Setup

```bash
# Health check
curl http://localhost:8000/health

# Interactive API docs
open http://localhost:8000/api/v1/docs
```

## Project Structure

```
backend/
├── src/
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Environment configuration
│   ├── api/
│   │   ├── health.py           # Health check endpoint
│   │   ├── schemas.py          # Pydantic request/response models
│   │   └── v1/
│   │       ├── __init__.py     # API v1 router setup
│   │       ├── auth.py         # Authentication endpoints
│   │       └── tasks.py        # Task CRUD endpoints
│   ├── db/
│   │   ├── database.py         # Database connection & session
│   │   └── models.py           # SQLModel ORM models
│   ├── middleware/
│   │   ├── auth.py             # JWT auth middleware
│   │   └── logging_middleware.py  # Request/response logging
│   └── services/
│       ├── auth_service.py     # Authentication business logic
│       ├── task_service.py     # Task business logic
│       └── db_service.py       # Database access patterns
├── alembic/
│   ├── versions/               # Database migrations
│   └── env.py                  # Alembic configuration
├── tests/
│   ├── conftest.py             # Test fixtures
│   ├── contract/               # OpenAPI contract tests
│   ├── integration/            # Integration tests
│   └── unit/                   # Unit tests
├── docs/
│   └── database-performance.md # Database index documentation
├── pyproject.toml              # Project dependencies & config
├── .env.example                # Development environment template
└── .env.production.example     # Production environment template
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/signin` | Sign in user |
| POST | `/api/v1/auth/logout` | Logout user |

### Tasks (Requires Authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/tasks` | List active tasks |
| POST | `/api/v1/tasks` | Create task |
| PUT | `/api/v1/tasks/{id}` | Update task title |
| PATCH | `/api/v1/tasks/{id}/complete` | Mark task complete |
| PATCH | `/api/v1/tasks/{id}/incomplete` | Mark task incomplete |
| DELETE | `/api/v1/tasks/{id}` | Delete task |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/docs` | Interactive API docs |
| GET | `/api/v1/redoc` | ReDoc documentation |

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src tests/

# Run specific test file
uv run pytest tests/integration/test_auth_flow.py -v

# Run contract tests only
uv run pytest tests/contract/ -v
```

**Test categories:**
- **Contract tests** (`tests/contract/`): Validate OpenAPI spec compliance
- **Integration tests** (`tests/integration/`): Test full request/response flows
- **Unit tests** (`tests/unit/`): Test service logic in isolation

### Code Quality

```bash
# Format code
uv run ruff format src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type checking
uv run mypy src/
```

### Database Migrations

```bash
# Create new migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1

# Show current version
uv run alembic current
```

## Production Deployment

### Environment Configuration

1. Copy production template:
   ```bash
   cp .env.production.example .env
   ```

2. Configure required variables:
   ```bash
   DATABASE_URL=postgresql+psycopg://... # Neon/production DB
   BETTER_AUTH_SECRET=<secure-32-char-secret>
   DEBUG=false
   ENVIRONMENT=production
   ALLOWED_ORIGINS=["https://your-domain.com"]
   ```

### Deployment Options

**Option 1: Docker** (Coming in Phase III)
```bash
docker build -t todo-api .
docker run -p 8000:8000 --env-file .env todo-api
```

**Option 2: Serverless** (Railway, Render, Fly.io)
- Use `.env.production.example` as template
- Set environment variables in platform dashboard
- Platform auto-runs migrations on startup

**Option 3: Traditional Server**
```bash
# Install dependencies
uv sync --no-dev

# Run with production server
uv run gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Database Setup (Production)

**Using Neon (Recommended):**
1. Create database at neon.tech
2. Copy connection string to `DATABASE_URL`
3. Migrations run automatically on startup

**Using Traditional PostgreSQL:**
```bash
# Connect to production database
psql $DATABASE_URL

# Run migrations manually
uv run alembic upgrade head
```

## Monitoring & Logging

### Logging

Logs are output to stdout with structured format:
```
2026-01-15 12:00:00 - src.services.auth_service - INFO - ✅ User registered: ...
```

**Log Levels:**
- `DEBUG`: Detailed debugging (development only)
- `INFO`: General information (default)
- `WARNING`: Warnings and potential issues
- `ERROR`: Errors and exceptions

### Performance Monitoring

- Request/response times logged by middleware
- Slow requests (>1s) automatically flagged
- Database query performance tracked via indexes

## Troubleshooting

### Common Issues

**Issue: `bcrypt` compatibility error**
```bash
# Solution: Downgrade bcrypt
uv pip install "bcrypt>=4.0.0,<5.0.0"
```

**Issue: Database connection fails**
```bash
# Check DATABASE_URL format
# For psycopg: postgresql+psycopg://user:pass@host/db
# For psycopg2: postgresql://user:pass@host/db

# Verify database is reachable
psql $DATABASE_URL
```

**Issue: ALLOWED_ORIGINS error**
```bash
# Must be JSON array format
ALLOWED_ORIGINS=["http://localhost:3000"]  # ✅ Correct
ALLOWED_ORIGINS=http://localhost:3000      # ❌ Wrong
```

**Issue: Migrations fail**
```bash
# Reset migrations (development only!)
uv run alembic downgrade base
uv run alembic upgrade head

# Or drop/recreate tables
psql $DATABASE_URL -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
uv run alembic upgrade head
```

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Write tests for new functionality
3. Ensure all tests pass: `uv run pytest`
4. Run linter: `uv run ruff check src/`
5. Format code: `uv run ruff format src/`
6. Create pull request

## License

MIT License - See LICENSE file for details

## Support

- **Documentation**: http://localhost:8000/api/v1/docs
- **Issues**: GitHub Issues
- **Wiki**: Project Wiki (Coming soon)

## Related

- **Frontend**: `../frontend/README.md`
- **Deployment Guide**: `./docs/deployment.md` (Coming in Phase III)
- **Database Performance**: `./docs/database-performance.md`
