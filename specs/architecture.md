# System Architecture

## Overview

Phase II implements a full-stack web architecture with a decoupled frontend and backend, connected via RESTful APIs with JWT-based authentication.

## Architecture Diagram

```
                                    Phase II Architecture

+------------------+     HTTPS      +------------------+     HTTP      +------------------+
|                  |--------------->|                  |-------------->|                  |
|  Next.js 16+     |                |  FastAPI         |               |  Neon PostgreSQL |
|  (App Router)    |<---------------|  Backend         |<--------------|  (Serverless)    |
|                  |     JSON       |                  |     SQL       |                  |
+------------------+                +------------------+               +------------------+
        |                                   |
        |                                   |
        v                                   v
+------------------+                +------------------+
|  Better Auth     |                |  JWT Middleware  |
|  (Frontend)      |--------------->|  (Backend)       |
|                  |     JWT        |                  |
+------------------+                +------------------+
```

## Data Flow

### App Router Request Lifecycle

```
1. Browser Request
        |
        v
2. Next.js App Router
   - Server Components (default) - render on server
   - Route Handlers (/api/*) - BFF pattern
        |
        v
3. Data Fetching Strategy
   - Server Components: Direct fetch in component
   - Client Components: useEffect/SWR/React Query
   - Server Actions: Form mutations
        |
        v
4. FastAPI Backend
   - JWT validation middleware
   - Route handlers
   - SQLModel ORM
        |
        v
5. Neon PostgreSQL
   - User data (Better Auth managed)
   - Task data (application managed)
```

### Authentication Flow

```
1. User visits app
        |
        v
2. Better Auth checks session (client-side)
   - No session -> Redirect to /auth/signin
   - Has session -> Continue
        |
        v
3. Better Auth issues JWT token
        |
        v
4. Frontend attaches JWT to API requests
   Authorization: Bearer <token>
        |
        v
5. FastAPI validates JWT
   - Verify signature with BETTER_AUTH_SECRET
   - Extract user_id from token
   - Match with URL user_id parameter
        |
        v
6. Backend returns user-specific data
```

## Component Responsibilities

### Frontend (Next.js 16+ App Router)

| Component | Responsibility |
|-----------|----------------|
| `app/` | Route definitions using file-system routing |
| `app/layout.tsx` | Root layout with providers |
| `app/page.tsx` | Home page (Server Component) |
| `app/tasks/` | Task management routes |
| `app/auth/` | Authentication routes |
| `components/` | Reusable UI components |
| `lib/api.ts` | API client with JWT attachment |
| `lib/auth.ts` | Better Auth client configuration |

### Backend (FastAPI)

| Component | Responsibility |
|-----------|----------------|
| `main.py` | FastAPI app entry, CORS, middleware |
| `routes/tasks.py` | Task CRUD endpoints |
| `routes/auth.py` | Auth-related endpoints (if needed) |
| `models.py` | SQLModel database models |
| `schemas.py` | Pydantic request/response schemas |
| `db.py` | Database connection and session |
| `middleware/auth.py` | JWT validation middleware |

### Database (Neon PostgreSQL)

| Table | Owner | Description |
|-------|-------|-------------|
| `user` | Better Auth | User accounts, sessions |
| `session` | Better Auth | Active sessions |
| `account` | Better Auth | OAuth providers |
| `verification` | Better Auth | Email verification |
| `tasks` | Application | User todo items |

## App Router Patterns

### Server Components (Default)

```tsx
// app/tasks/page.tsx - Server Component
export default async function TasksPage() {
  // Direct data fetching - no useEffect needed
  const tasks = await fetchTasks();
  return <TaskList tasks={tasks} />;
}
```

### Client Components

```tsx
// components/task-form.tsx - Client Component
'use client';

import { useState } from 'react';

export function TaskForm() {
  const [title, setTitle] = useState('');
  // Interactive state management
}
```

### Server Actions

```tsx
// app/tasks/actions.ts - Server Actions
'use server';

export async function createTask(formData: FormData) {
  // Direct server-side mutation
  await api.post('/tasks', { title: formData.get('title') });
  revalidatePath('/tasks');
}
```

### Route Handlers (API Routes)

```tsx
// app/api/tasks/route.ts - Route Handler (BFF)
export async function GET(request: Request) {
  // Backend-for-Frontend pattern
  const data = await fetch(BACKEND_URL + '/tasks');
  return Response.json(data);
}
```

## Security Architecture

### JWT Token Flow

| Step | Component | Action |
|------|-----------|--------|
| 1 | Better Auth | User logs in, JWT issued |
| 2 | Frontend | Store JWT (httpOnly cookie preferred) |
| 3 | API Client | Attach `Authorization: Bearer <token>` |
| 4 | FastAPI | Validate JWT signature |
| 5 | FastAPI | Extract user_id, enforce ownership |

### Security Measures

- **HTTPS**: All traffic encrypted (Vercel + backend)
- **JWT Expiry**: Tokens expire (configurable, e.g., 7 days)
- **User Isolation**: API filters data by authenticated user
- **CORS**: Restrict origins to frontend domain
- **Input Validation**: Pydantic models validate all input

## Environment Configuration

### Frontend (.env.local)

```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://... # For Better Auth
```

### Backend (.env)

```
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-secret-key  # Same as frontend
CORS_ORIGINS=http://localhost:3000
```

## Deployment Architecture

### Development

```
localhost:3000 (Next.js) --> localhost:8000 (FastAPI) --> Neon DB
```

### Production

```
Vercel (Next.js) --> Railway/Render (FastAPI) --> Neon DB
     ^                       ^
     |                       |
     +--- HTTPS ------------+
```

## Related Specifications

- [REST API Endpoints](./api/rest-endpoints.md)
- [Database Schema](./database/schema.md)
- [UI Components](./ui/components.md)
- [App Routes](./ui/app-routes.md)
- [Authentication Feature](./features/003-authentication.md)
