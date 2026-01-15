# Backend Service: FastAPI Todo API

## Service Overview

This is the backend service for the Todo Evolution application. It provides a RESTful API built with FastAPI, SQLModel ORM, and Neon PostgreSQL.

**Parent Constitution:** `../.specify/memory/constitution.md`

---

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | FastAPI | Latest |
| ORM | SQLModel | Latest |
| Database | Neon PostgreSQL | Serverless |
| Auth | Better Auth | JWT-based |
| Runtime | Python | 3.13+ |
| Package Manager | uv | Latest |
| Testing | pytest | Latest |
| Linting | ruff | Latest |

---

## Commands

```bash
# Navigate to backend directory
cd backend/

# Install dependencies
uv sync

# Run development server
uv run uvicorn src.todo_api.main:app --reload --port 8000

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src

# Lint code
uv run ruff check .

# Format code
uv run ruff format .

# Generate OpenAPI schema
uv run python -c "from src.todo_api.main import app; import json; print(json.dumps(app.openapi()))"
```

---

## Directory Structure

```
backend/
├── CLAUDE.md              # This file
├── pyproject.toml         # Python dependencies
├── src/
│   └── todo_api/
│       ├── __init__.py
│       ├── main.py        # FastAPI app entry point
│       ├── config.py      # Settings and environment
│       ├── database.py    # SQLModel + Neon connection
│       ├── models/        # SQLModel database models
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── todo.py
│       ├── schemas/       # Pydantic request/response schemas
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── todo.py
│       ├── routers/       # API route handlers
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   └── todos.py
│       ├── services/      # Business logic
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   └── todo.py
│       └── dependencies.py # Dependency injection
└── tests/
    ├── conftest.py        # pytest fixtures
    ├── test_auth.py
    └── test_todos.py
```

---

## API Endpoints

### Authentication (`/auth`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get JWT |
| POST | `/auth/logout` | Invalidate token |
| GET | `/auth/me` | Get current user |

### Todos (`/todos`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/todos` | List user's todos |
| POST | `/todos` | Create new todo |
| GET | `/todos/{id}` | Get specific todo |
| PUT | `/todos/{id}` | Update todo |
| DELETE | `/todos/{id}` | Delete todo |
| PATCH | `/todos/{id}/complete` | Mark as complete |

---

## Database Models

### User
```python
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime
    todos: list["Todo"] = Relationship(back_populates="user")
```

### Todo
```python
class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = None
    completed: bool = False
    created_at: datetime
    updated_at: datetime
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="todos")
```

---

## Environment Variables

```bash
# .env (DO NOT COMMIT)
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

---

## Coding Standards

### Models & Schemas
- **SQLModel** for database tables (inherits from SQLModel with `table=True`)
- **Pydantic** for API request/response schemas
- Separate models from schemas to avoid circular dependencies

### API Design
- Use dependency injection for database sessions and auth
- Return proper HTTP status codes (201 for create, 204 for delete)
- Use Pydantic models for request validation and response serialization
- Document all endpoints with OpenAPI docstrings

### Error Handling
- Use FastAPI's HTTPException for API errors
- Create custom exception handlers for domain errors
- Return consistent error response format

### Testing
- Use pytest with async support
- Mock database with in-memory SQLite for tests
- Test all API endpoints and edge cases
- Maintain 100% coverage for new code

---

## Authentication Flow

1. User registers with email/password
2. Password is hashed with bcrypt
3. User logs in, receives JWT token
4. Token included in `Authorization: Bearer <token>` header
5. Protected endpoints validate token via dependency
6. Token contains user_id claim for authorization
