# REST API Endpoints

## Overview

FastAPI backend providing RESTful endpoints for task management with JWT authentication.

## Base Configuration

| Environment | Base URL |
|-------------|----------|
| Development | `http://localhost:8000` |
| Production | `https://api.your-domain.com` |

## Authentication

All endpoints require JWT token in Authorization header:

```
Authorization: Bearer <jwt_token>
```

Requests without valid token receive `401 Unauthorized`.

## Endpoints

### Tasks

#### GET /api/{user_id}/tasks

List all tasks for the authenticated user.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | User ID (must match JWT) |

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| status | string | No | "all" | Filter: "all", "pending", "completed" |
| sort | string | No | "created" | Sort by: "created", "title", "updated" |
| order | string | No | "desc" | Order: "asc", "desc" |

**Response 200:**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2025-01-10T10:00:00Z",
      "updated_at": "2025-01-10T10:00:00Z"
    }
  ],
  "total": 1
}
```

**Response 401:**
```json
{
  "detail": "Not authenticated"
}
```

**Response 403:**
```json
{
  "detail": "User ID mismatch"
}
```

---

#### POST /api/{user_id}/tasks

Create a new task.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | User ID (must match JWT) |

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| title | string | Yes | 1-200 characters |
| description | string | No | Max 1000 characters |

**Response 201:**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-01-10T10:00:00Z",
  "updated_at": "2025-01-10T10:00:00Z"
}
```

**Response 422:**
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

#### GET /api/{user_id}/tasks/{task_id}

Get a specific task by ID.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | User ID |
| task_id | integer | Yes | Task ID |

**Response 200:**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-01-10T10:00:00Z",
  "updated_at": "2025-01-10T10:00:00Z"
}
```

**Response 404:**
```json
{
  "detail": "Task not found"
}
```

---

#### PUT /api/{user_id}/tasks/{task_id}

Update a task.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | User ID |
| task_id | integer | Yes | Task ID |

**Request Body:**
```json
{
  "title": "Buy organic groceries",
  "description": "Organic milk, free-range eggs"
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| title | string | No | 1-200 characters |
| description | string | No | Max 1000 characters |

**Response 200:**
```json
{
  "id": 1,
  "title": "Buy organic groceries",
  "description": "Organic milk, free-range eggs",
  "completed": false,
  "created_at": "2025-01-10T10:00:00Z",
  "updated_at": "2025-01-10T11:00:00Z"
}
```

**Response 404:**
```json
{
  "detail": "Task not found"
}
```

---

#### DELETE /api/{user_id}/tasks/{task_id}

Delete a task.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | User ID |
| task_id | integer | Yes | Task ID |

**Response 204:** No content

**Response 404:**
```json
{
  "detail": "Task not found"
}
```

---

#### PATCH /api/{user_id}/tasks/{task_id}/complete

Toggle task completion status.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | User ID |
| task_id | integer | Yes | Task ID |

**Response 200:**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2025-01-10T10:00:00Z",
  "updated_at": "2025-01-10T12:00:00Z"
}
```

**Response 404:**
```json
{
  "detail": "Task not found"
}
```

---

### Health Check

#### GET /health

Health check endpoint (no auth required).

**Response 200:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message here"
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (successful deletion) |
| 400 | Bad Request |
| 401 | Unauthorized (missing/invalid token) |
| 403 | Forbidden (user ID mismatch) |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

## CORS Configuration

```python
CORS_ORIGINS = [
    "http://localhost:3000",        # Development
    "https://your-app.vercel.app",  # Production
]
```

## Rate Limiting

| Endpoint Pattern | Limit |
|------------------|-------|
| POST /api/*/tasks | 100/hour |
| GET /api/*/tasks | 1000/hour |
| All other | 500/hour |

## Request/Response Models (Pydantic)

```python
# schemas.py
from pydantic import BaseModel, Field
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)

class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime

class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int
```

## OpenAPI Documentation

FastAPI auto-generates OpenAPI docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Related Specifications

- [Database Schema](../database/schema.md)
- [Authentication](../features/003-authentication.md)
- [System Architecture](../architecture.md)
