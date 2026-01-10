# Feature: Task CRUD API (Phase II)

**Phase**: II - Full-Stack Web Application
**Status**: Active
**Priority**: P1

## Overview

Transform the Phase I in-memory task management into a persistent, multi-user web application with RESTful API endpoints and a responsive Next.js frontend.

## User Stories

### US-001: Create Task via Web UI (P1)

**As a** logged-in user
**I want to** create a task through the web interface
**So that** I can add items to my todo list from any device

**Acceptance Criteria:**
- Form with title (required) and description (optional) fields
- Title: 1-200 characters
- Description: max 1000 characters
- Task associated with authenticated user
- Success notification on creation
- Task appears in list immediately
- Form clears after successful submission

**App Router Implementation:**
- Server Action for form submission
- Optimistic UI update
- `revalidatePath('/tasks')` after mutation

### US-002: View Tasks via Web UI (P1)

**As a** logged-in user
**I want to** see all my tasks in a list view
**So that** I can manage my todo items

**Acceptance Criteria:**
- Display task title, status indicator, created date
- Only show tasks belonging to current user
- Support filtering by status (all/pending/completed)
- Empty state message when no tasks
- Responsive layout (mobile/desktop)

**App Router Implementation:**
- Server Component for initial render
- Streaming with Suspense for loading states
- URL-based filter state (`?status=pending`)

### US-003: Update Task via Web UI (P2)

**As a** logged-in user
**I want to** edit my task details
**So that** I can correct or update information

**Acceptance Criteria:**
- Inline edit or modal form
- Update title and/or description
- Preserve unchanged fields
- Optimistic update with rollback on error
- Success notification

### US-004: Delete Task via Web UI (P2)

**As a** logged-in user
**I want to** delete tasks I no longer need
**So that** I can keep my list clean

**Acceptance Criteria:**
- Confirmation dialog before deletion
- Optimistic removal from list
- Success notification
- Undo option (optional enhancement)

### US-005: Toggle Task Completion (P1)

**As a** logged-in user
**I want to** mark tasks as complete/incomplete
**So that** I can track my progress

**Acceptance Criteria:**
- One-click toggle via checkbox or button
- Visual distinction for completed tasks
- Optimistic UI update
- Persists to database

## Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-001 | System MUST persist tasks to PostgreSQL database |
| FR-002 | System MUST associate tasks with user accounts |
| FR-003 | System MUST enforce task ownership (users only see their tasks) |
| FR-004 | System MUST provide responsive web interface |
| FR-005 | System MUST support CRUD operations via REST API |
| FR-006 | System MUST validate input on both client and server |
| FR-007 | System MUST handle concurrent updates gracefully |
| FR-008 | System MUST provide real-time feedback on operations |

## Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-001 | API response time < 200ms for CRUD operations |
| NFR-002 | UI must be accessible (WCAG 2.1 AA) |
| NFR-003 | Support latest 2 versions of major browsers |
| NFR-004 | Mobile-responsive design |

## API Integration

The web UI integrates with the backend API:

| UI Action | API Endpoint | Method |
|-----------|--------------|--------|
| Create Task | `/api/{user_id}/tasks` | POST |
| List Tasks | `/api/{user_id}/tasks` | GET |
| Update Task | `/api/{user_id}/tasks/{id}` | PUT |
| Delete Task | `/api/{user_id}/tasks/{id}` | DELETE |
| Toggle Complete | `/api/{user_id}/tasks/{id}/complete` | PATCH |

See [REST Endpoints Spec](../api/rest-endpoints.md) for full API documentation.

## Data Flow (App Router)

### Create Task Flow

```
1. User fills form -> Client Component
2. Submit triggers Server Action
3. Server Action:
   - Validates input
   - Gets JWT from session
   - Calls FastAPI POST /api/{user_id}/tasks
   - revalidatePath('/tasks')
4. UI updates via React Server Component re-render
```

### List Tasks Flow

```
1. User navigates to /tasks
2. Server Component renders:
   - Fetches tasks from FastAPI (server-side)
   - Returns pre-rendered HTML
3. Suspense boundary shows loading skeleton
4. Filter changes update URL searchParams
5. Server Component re-renders with new data
```

## Component Hierarchy

```
app/tasks/page.tsx (Server Component)
├── TaskFilters (Client Component - interactivity)
├── Suspense boundary
│   └── TaskList (Server Component - data fetching)
│       └── TaskItem (Client Component - toggle, delete)
└── CreateTaskForm (Client Component - Server Action)
```

## Success Criteria

- [ ] Users can perform all CRUD operations via web UI
- [ ] Tasks persist across sessions
- [ ] Multi-user support with data isolation
- [ ] Responsive design works on mobile/tablet/desktop
- [ ] API latency < 200ms
- [ ] Zero data leakage between users

## Related Specifications

- [REST API Endpoints](../api/rest-endpoints.md)
- [Database Schema](../database/schema.md)
- [UI Components](../ui/components.md)
- [Authentication](./003-authentication.md)
