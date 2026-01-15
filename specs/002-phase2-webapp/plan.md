# Implementation Plan: Phase II - Full-Stack Web Application

**Branch**: `002-phase2-webapp` | **Date**: 2026-01-10 | **Spec**: [Phase II Specification](./spec.md)
**Input**: Feature specification from `/specs/002-phase2-webapp/spec.md`

## Summary

Implement a full-stack web application supporting 5 basic todo features (Create, Read, Update, Delete, Mark Complete) with user authentication via Better Auth, RESTful API endpoints, responsive frontend, and Neon Serverless PostgreSQL database persistence. MVP focuses on single-user per account, title-only tasks, and straightforward UI/UX.

**Key Technical Decisions:**
- Backend: FastAPI (Python) with SQLModel ORM
- Frontend: Next.js 16+ (App Router, TypeScript)
- Database: Neon Serverless PostgreSQL
- Auth: Better Auth (email/password)
- API: URL-versioned REST (`/api/v1/...`)
- Concurrency: Last-Write-Wins (optimistic)
- Deletion: Dual strategy (hard-delete explicit, soft-delete/archive completed)

## Technical Context

**Language/Version**: 
- Backend: Python 3.13+
- Frontend: TypeScript 5.3+
- Node.js: 20+

**Primary Dependencies**: 
- Backend: FastAPI, SQLModel, Alembic (migrations), Better Auth, Pydantic
- Frontend: Next.js, TypeScript, TailwindCSS, React Query (for data fetching)

**Storage**: Neon Serverless PostgreSQL (serverless, auto-scaling)

**Testing**: 
- Backend: pytest, pytest-asyncio, httpx (for API testing)
- Frontend: Jest, React Testing Library
- Integration: pytest for API contract tests

**Target Platform**: Web (responsive design: 320px - 4K), Server (Linux)

**Project Type**: Web (frontend + backend separation)

**Performance Goals**:
- Task list display: <500ms (p95) - SC-002
- API response: <200ms (p95) - SC-004
- Authentication: <1 second - SC-006
- Task creation to list appearance: <2 seconds - SC-001
- Large task list (100+): <2 seconds - User Story 2, scenario 4

**Constraints**:
- 99.5% uptime SLA - SC-005
- User data isolation mandatory (no cross-user data leakage) - SC-009
- Mobile responsiveness required - SC-003, SC-010
- No rate limiting in Phase II (defer to Phase III) - Clarification Q5

**Scale/Scope**: 
- Initial: 1000 concurrent users - Assumption #7
- MVP: Single device, single browser session per user
- Tasks per user: No hard limit initially (test with 100+ for load)

## Constitution Check

**Principles Verified:**

- ✅ **I. Spec-Driven Development**: Implementation plan follows specification; spec is source of truth; no deviations without amendment
- ✅ **II. Prompt History Records**: PHR created for spec, clarification, and this plan stage; audit trail complete
- ✅ **III. Architectural Decision Records**: No ADR-significant decisions yet (standard tech stack); will evaluate after architecture review
- ✅ **IV. Test-First Development**: Tests required for API contracts, integration, and unit tests; TDD cycle mandatory during implementation
- ✅ **V. Library-First Design**: Backend components modularized as independent services (auth, task management); API provides CLI-like interface
- ✅ **VI. Simplicity & YAGNI**: Minimal feature set (title-only tasks); no custom fields, categories, or advanced filtering; deferring complexity to Phase III

**Gates - All Passing:**
- Specification complete with all clarifications resolved ✅
- No unresolved ambiguities ✅
- Constitution principles aligned ✅
- Technical stack justified (see rationale below) ✅
- Performance goals measurable and testable ✅

## Project Structure

### Documentation (this feature)

```text
specs/002-phase2-webapp/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 research (technology choices, best practices)
├── data-model.md        # Phase 1 design (entities, schema)
├── quickstart.md        # Phase 1 developer guide
├── contracts/           # Phase 1 API contracts (OpenAPI)
│   └── tasks-api.openapi.yaml
└── checklists/
    └── requirements.md  # Quality checklist
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py                 # FastAPI app entry point
│   ├── models/
│   │   ├── user.py            # User entity
│   │   └── task.py            # Task entity
│   ├── services/
│   │   ├── auth_service.py    # Authentication logic (Better Auth wrapper)
│   │   ├── task_service.py    # Task CRUD logic
│   │   └── db_service.py      # Database access patterns
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py        # Auth endpoints (register, login, logout)
│   │   │   ├── tasks.py       # Task endpoints (CRUD)
│   │   │   └── health.py      # Health check
│   │   └── schemas.py          # Pydantic request/response schemas
│   ├── db/
│   │   ├── database.py        # SQLModel session, connection pool
│   │   ├── migrations/        # Alembic migration scripts
│   │   └── models.py          # SQLModel ORM definitions
│   └── config.py              # Environment config, secrets
├── tests/
│   ├── unit/
│   │   ├── test_models.py
│   │   └── test_services.py
│   ├── integration/
│   │   ├── test_auth_flow.py
│   │   └── test_task_api.py
│   ├── contract/
│   │   └── test_api_contracts.py
│   └── conftest.py            # Pytest fixtures, test database
├── pyproject.toml             # Dependencies, metadata
├── .env.example               # Environment template
└── README.md                  # Backend setup guide

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Landing page
│   │   ├── auth/
│   │   │   ├── signup/page.tsx
│   │   │   └── signin/page.tsx
│   │   ├── tasks/
│   │   │   └── page.tsx       # Main task list page
│   │   └── api/               # API routes (Next.js server functions)
│   │       └── [...].ts       # Proxy to backend
│   ├── components/
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskForm.tsx
│   │   └── AuthForm.tsx
│   ├── lib/
│   │   ├── api-client.ts      # Fetch wrapper, error handling
│   │   ├── hooks/
│   │   │   ├── useTasks.ts    # React Query hook for tasks
│   │   │   └── useAuth.ts     # Auth context/state
│   │   └── types.ts           # Shared TypeScript types
│   ├── styles/
│   │   └── globals.css        # TailwindCSS
│   └── app.tsx                # App configuration
├── tests/
│   ├── unit/
│   │   └── components/
│   ├── integration/
│   │   └── task-flow.test.tsx
│   └── setup.ts               # Jest configuration
├── package.json               # Dependencies
├── tsconfig.json              # TypeScript config
├── tailwind.config.js         # TailwindCSS config
└── README.md                  # Frontend setup guide

.env.local                      # Local environment (git-ignored)
docker-compose.yml             # Local dev: Neon emulator or PostgreSQL
```

**Structure Decision**: 
Web application with separate frontend (Next.js) and backend (FastAPI) allows independent scaling, testing, and deployment. Shared types via TypeScript types file. API-first design ensures both web and future mobile clients can use same endpoints.

## Architecture Overview

### Data Flow

```
User → Frontend (Next.js) → API (FastAPI/v1) → Services → Database (Neon PostgreSQL)
                ↑ React Query (caching)
                ↑ Session via Better Auth cookies
```

### Key Components

**Backend**:
1. **FastAPI App**: HTTP server, OpenAPI docs at `/api/docs`
2. **Better Auth Integration**: Session/JWT management, middleware for auth checks
3. **SQLModel ORM**: Type-safe database models (Pydantic + SQLAlchemy)
4. **Alembic**: Database schema versioning and migrations
5. **Services Layer**: Business logic (task CRUD, auth validation)

**Frontend**:
1. **Next.js App Router**: File-based routing
2. **React Query**: Server state management, caching, refetching
3. **TypeScript Components**: Type-safe UI
4. **TailwindCSS**: Responsive styling (mobile-first)
5. **Auth Context**: Session state (user ID, logged-in status)

**Database**:
1. **Neon PostgreSQL**: Serverless, auto-scaling, connection pooling
2. **Schema**: Users table, Tasks table (with user_id FK), Sessions (via Better Auth)
3. **Migrations**: Alembic-managed schema changes

### Concurrency & Data Integrity

**Concurrency Model**: Last-Write-Wins (optimistic approach)
- No version fields needed in MVP
- Each update overwrites previous (appropriate for rare simultaneous edits)
- Trade-off: simplicity for MVP vs. potential lost updates in edge case

**Data Isolation**: 
- All task queries filtered by `user_id` (authenticated session user)
- API middleware validates user ownership before allowing mutations
- Database constraints enforce FK relationship (user owns task)

### Deletion Strategy (Clarification Q2)

**Completed Tasks** → Soft-delete (archive):
- Add `is_archived` boolean field to tasks table
- Mark complete → set `is_archived = true` (not deleted, just hidden from active list)
- Benefits: audit trail, potential "undo complete", data recovery

**Explicitly Deleted Tasks** → Hard-delete:
- User clicks "Delete" button → remove from database entirely
- Permanent removal (no recovery, no archive)
- Simpler UX: trash is gone

**UI Implications**:
- Active task list: `WHERE user_id = ? AND completed = false AND is_archived = false`
- Completed/archived: separate view (optional in Phase II, could be hidden)
- Delete button: hard-delete from DB

### API Versioning (Clarification Q3)

URL path versioning: `/api/v1/tasks`
- Allows future `/api/v2/tasks` without breaking v1 clients
- Explicit version in URL aids debugging, logging, analytics
- OpenAPI docs available at `/api/v1/docs`

## Complexity Tracking

No Constitution violations; all principles aligned. Simple, focused MVP scope.

## Deployment & Operations (Phase II+)

**Not in Phase II scope but documented for planning:**

- Staging environment: Neon preview branches or separate DB
- CI/CD: GitHub Actions for linting, testing, type checking
- Deployment: Backend to serverless (Vercel, Railway, Fly.io); Frontend to Vercel
- Monitoring: Sentry (errors), structured logging, health checks
- Rate limiting: Reverse proxy (Cloudflare, nginx) added in Phase III

---

## Next Steps (Phase 1 Design)

1. ✅ **Research.md**: Document technology choices, best practices (FastAPI auth, SQLModel patterns, Next.js data fetching)
2. ✅ **Data-model.md**: Entity definitions, schema, relationships (User, Task with is_archived, Session)
3. ✅ **API Contracts**: OpenAPI schema for `/api/v1/auth/*` and `/api/v1/tasks/*`
4. ✅ **Quickstart.md**: Developer setup guide (clone, `.env` setup, `docker-compose up`, `npm install`, first run)
5. ⏭ **Update agent context**: Run `update-agent-context.sh claude` to inject tech stack into agent memory

Then proceed to Phase 2:
- Run `/sp.tasks` to generate testable, dependency-ordered task list
- Execute `/sp.implement` for red-green-refactor cycles
