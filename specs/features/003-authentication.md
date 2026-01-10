# Feature: User Authentication (Phase II)

**Phase**: II - Full-Stack Web Application
**Status**: Active
**Priority**: P1

## Overview

Implement user authentication using Better Auth on the Next.js frontend with JWT token verification on the FastAPI backend. This enables multi-user support with secure task isolation.

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Auth Library | Better Auth | Session management, JWT issuance |
| Token Format | JWT | Stateless authentication |
| Frontend | Next.js 16+ | Auth UI, token storage |
| Backend | FastAPI | JWT verification, user extraction |
| Database | Neon PostgreSQL | User storage (Better Auth tables) |

## User Stories

### US-001: User Registration (P1)

**As a** new user
**I want to** create an account with email and password
**So that** I can save and access my tasks

**Acceptance Criteria:**
- Email must be valid and unique
- Password minimum 8 characters
- Password confirmation required
- Email verification (optional for MVP)
- Redirect to tasks page after registration
- Show validation errors inline

### US-002: User Login (P1)

**As a** registered user
**I want to** sign in with my credentials
**So that** I can access my tasks

**Acceptance Criteria:**
- Email and password fields
- "Remember me" option
- Show error for invalid credentials
- Redirect to intended page after login
- JWT token stored securely (httpOnly cookie)

### US-003: User Logout (P1)

**As a** logged-in user
**I want to** sign out
**So that** I can secure my account on shared devices

**Acceptance Criteria:**
- Clear session and JWT
- Redirect to home/login page
- Invalidate server-side session

### US-004: Protected Routes (P1)

**As the** system
**I want to** protect task routes
**So that** only authenticated users can access tasks

**Acceptance Criteria:**
- Unauthenticated users redirected to login
- JWT validated on every API request
- Expired tokens trigger re-authentication
- User ID extracted from token for API calls

### US-005: Session Persistence (P2)

**As a** logged-in user
**I want to** remain logged in across browser sessions
**So that** I don't have to sign in repeatedly

**Acceptance Criteria:**
- Session persists for configured duration (e.g., 7 days)
- Token refresh mechanism
- Secure token storage

## Authentication Architecture

### Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           AUTHENTICATION FLOW                            │
└─────────────────────────────────────────────────────────────────────────┘

  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
  │   Browser    │         │   Next.js    │         │   FastAPI    │
  │              │         │   + Better   │         │   Backend    │
  │              │         │     Auth     │         │              │
  └──────┬───────┘         └──────┬───────┘         └──────┬───────┘
         │                        │                        │
         │  1. Login Request      │                        │
         │──────────────────────>│                        │
         │                        │                        │
         │                        │  2. Validate credentials
         │                        │  (Better Auth + DB)    │
         │                        │                        │
         │  3. JWT Token          │                        │
         │<──────────────────────│                        │
         │  (httpOnly cookie)     │                        │
         │                        │                        │
         │  4. API Request        │                        │
         │  + Authorization header│                        │
         │──────────────────────────────────────────────>│
         │                        │                        │
         │                        │  5. Verify JWT         │
         │                        │  Extract user_id       │
         │                        │                        │
         │  6. User-specific data │                        │
         │<──────────────────────────────────────────────│
         │                        │                        │
```

### JWT Token Structure

```json
{
  "sub": "user_id_here",
  "email": "user@example.com",
  "name": "User Name",
  "iat": 1704067200,
  "exp": 1704672000
}
```

## Implementation Details

### Frontend (Better Auth)

```typescript
// lib/auth.ts
import { betterAuth } from 'better-auth';
import { nextCookies } from 'better-auth/next-cookies';

export const auth = betterAuth({
  database: {
    type: 'postgres',
    url: process.env.DATABASE_URL,
  },
  jwt: {
    enabled: true,
    secret: process.env.BETTER_AUTH_SECRET,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
  },
  plugins: [nextCookies()],
});
```

### Backend (FastAPI JWT Middleware)

```python
# middleware/auth.py
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
import jwt

security = HTTPBearer()

async def verify_jwt(credentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        return payload["sub"]  # user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
```

### Protected Route Example

```typescript
// app/tasks/page.tsx
import { auth } from '@/lib/auth';
import { redirect } from 'next/navigation';

export default async function TasksPage() {
  const session = await auth.api.getSession();

  if (!session) {
    redirect('/auth/signin');
  }

  // Fetch user's tasks
  const tasks = await fetchTasks(session.user.id, session.token);

  return <TaskList tasks={tasks} />;
}
```

## API Client Integration

```typescript
// lib/api.ts
import { auth } from './auth';

export async function apiClient(endpoint: string, options: RequestInit = {}) {
  const session = await auth.api.getSession();

  if (!session) {
    throw new Error('Not authenticated');
  }

  return fetch(`${API_URL}/api/${session.user.id}${endpoint}`, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${session.token}`,
      'Content-Type': 'application/json',
    },
  });
}
```

## Security Requirements

| Requirement | Implementation |
|-------------|----------------|
| Password Hashing | Better Auth (bcrypt) |
| Token Storage | httpOnly cookies |
| Token Expiry | 7 days (configurable) |
| HTTPS | Required in production |
| CORS | Whitelist frontend domain |
| Rate Limiting | Login attempts limited |

## Database Tables (Better Auth)

Better Auth creates these tables automatically:

| Table | Purpose |
|-------|---------|
| `user` | User accounts |
| `session` | Active sessions |
| `account` | OAuth providers (future) |
| `verification` | Email verification tokens |

See [Database Schema](../database/schema.md) for full schema.

## Environment Variables

### Frontend (.env.local)

```
BETTER_AUTH_SECRET=your-256-bit-secret
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://...
```

### Backend (.env)

```
BETTER_AUTH_SECRET=your-256-bit-secret  # Must match frontend
```

## Success Criteria

- [ ] Users can register with email/password
- [ ] Users can log in and receive JWT
- [ ] JWT validated on all API requests
- [ ] Users only see their own tasks
- [ ] Sessions persist across browser restarts
- [ ] Invalid/expired tokens handled gracefully
- [ ] No security vulnerabilities (XSS, CSRF, etc.)

## Related Specifications

- [REST API Endpoints](../api/rest-endpoints.md)
- [Database Schema](../database/schema.md)
- [App Routes](../ui/app-routes.md)
