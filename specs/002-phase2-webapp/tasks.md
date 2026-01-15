# Tasks: Phase II - Full-Stack Web Application

**Input**: Design documents from `/specs/002-phase2-webapp/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/tasks-api.openapi.yaml ✅
**Status**: Ready for implementation
**Branch**: `002-phase2-webapp`

---

## Format Reference

- **[ID]**: Task identifier (T001, T002, etc.) in execution order
- **[P]**: Task can run in parallel (different files, no blocking dependencies)
- **[US#]**: User story identifier (US1, US2, US3, US4, US5, US6)
- **Description**: Action with exact file path

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and foundational structure setup

- [X] T001 Create backend directory structure with src/, tests/unit/, tests/integration/, tests/contract/ in backend/
- [X] T002 Create frontend directory structure with src/app/, src/components/, src/lib/, src/styles/, tests/ in frontend/
- [X] T003 [P] Initialize backend Python project: backend/pyproject.toml with FastAPI, SQLModel, Alembic, Better Auth, pytest, pytest-asyncio, httpx
- [X] T004 [P] Initialize frontend Node project: frontend/package.json with Next.js, TypeScript, TailwindCSS, React Query, Jest, React Testing Library
- [X] T005 [P] Configure backend linting and formatting: ruff, mypy configuration in pyproject.toml
- [X] T006 [P] Configure frontend linting and formatting: ESLint, Prettier, TypeScript in frontend/
- [X] T007 Create .env.example files for backend and frontend with required environment variables
- [X] T008 Create docker-compose.yml for local PostgreSQL development database
- [X] T009 Create GitHub Actions CI/CD workflow for linting, type-checking, and tests (.github/workflows/)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST complete before ANY user story work begins

**⚠️ CRITICAL**: No user story implementation can start until ALL foundational tasks complete

### Database & Migrations

- [X] T010 Initialize Alembic in backend/alembic/ with env.py configuration
- [X] T011 Create initial migration script: backend/alembic/versions/001_initial_schema.py (users, tasks tables with schema from data-model.md)

### Backend API & Middleware Infrastructure

- [X] T012 [P] Create backend/src/main.py with FastAPI app initialization, CORS, middleware setup
- [X] T013 [P] Create backend/src/config.py with environment configuration (DATABASE_URL, BETTER_AUTH_SECRET, DEBUG)
- [X] T014 [P] Create backend/src/db/database.py with SQLModel engine, session factory, connection pooling
- [X] T015 Create backend/src/db/models.py with SQLModel base classes and ORM model definitions (User, Task, Session)
- [X] T016 [P] Create backend/src/api/schemas.py with Pydantic request/response schemas (UserCreate, TaskCreate, TaskResponse, etc.)
- [X] T017 [P] Create backend/src/api/v1/__init__.py and router setup for /api/v1/ endpoints
- [X] T018 Create backend/src/middleware/auth.py with Better Auth integration and session validation middleware
- [X] T019 [P] Create backend/src/services/db_service.py with database access patterns (get_user_by_email, get_task_by_id, etc.)
- [X] T020 Create backend/src/api/health.py with /health endpoint for status checks

### Frontend Setup & Configuration

- [X] T021 [P] Create frontend/src/app/layout.tsx with root layout, metadata, providers setup
- [X] T022 [P] Create frontend/src/lib/types.ts with shared TypeScript interfaces (User, Task, AuthContext)
- [X] T023 [P] Create frontend/src/lib/api-client.ts with fetch wrapper, error handling, base configuration for API calls
- [X] T024 Create frontend/src/lib/hooks/useAuth.ts with auth state management (login, signup, logout, session persistence)
- [X] T025 Create frontend/src/lib/hooks/useTasks.ts with React Query hooks for task operations (list, create, update, delete, complete)
- [X] T026 [P] Create frontend/src/components/ErrorBoundary.tsx for error handling and display
- [X] T027 [P] Create frontend/src/styles/globals.css with TailwindCSS setup and base styles

### Testing Infrastructure

- [X] T028 Create backend/tests/conftest.py with pytest fixtures (test database, test client, auth fixtures)
- [X] T029 Create frontend/jest.config.js and frontend/tests/setup.ts with Jest configuration
- [X] T030 [P] Create backend/tests/contract/conftest.py for OpenAPI contract test fixtures
- [X] T031 Create backend/tests/integration/conftest.py for integration test database setup

**✅ Checkpoint**: Foundation infrastructure complete - all user stories can now proceed independently

---

## Phase 3: User Story 1 - User Registration & Authentication (Priority: P1) 🎯 MVP Core

**Goal**: Enable new users to register with email/password and existing users to sign in, establishing authenticated sessions for subsequent features.

**Independent Test**: User can register → login with credentials → session persists across page reloads → logout clears session

### Contract Tests for US1

- [X] T032 [P] [US1] Create backend/tests/contract/test_auth_contracts.py validating /api/v1/auth/register endpoint against OpenAPI schema
- [X] T033 [P] [US1] Create backend/tests/contract/test_auth_contracts.py validating /api/v1/auth/signin endpoint against OpenAPI schema
- [X] T034 [P] [US1] Create backend/tests/contract/test_auth_contracts.py validating /api/v1/auth/logout endpoint against OpenAPI schema

### Integration Tests for US1

- [X] T035 [P] [US1] Create backend/tests/integration/test_auth_flow.py with registration flow test (email validation, password requirements, duplicate email detection)
- [X] T036 [P] [US1] Create backend/tests/integration/test_auth_flow.py with signin flow test (valid credentials → session token, invalid credentials → 401 error)
- [X] T037 [P] [US1] Create backend/tests/integration/test_auth_flow.py with session persistence test (token validity, refresh, expiration handling)

### Implementation for US1

- [X] T038 [P] [US1] Implement User model in backend/src/db/models.py with email (unique), password_hash, created_at, updated_at fields
- [X] T039 [US1] Create backend/src/services/auth_service.py with registration, signin, logout, session validation functions
- [X] T040 [US1] Implement /api/v1/auth/register endpoint in backend/src/api/v1/auth.py (POST: email, password → User object + session token)
- [X] T041 [US1] Implement /api/v1/auth/signin endpoint in backend/src/api/v1/auth.py (POST: email, password → session token, redirect)
- [X] T042 [US1] Implement /api/v1/auth/logout endpoint in backend/src/api/v1/auth.py (POST: session cleanup + redirect to signin)
- [X] T043 [US1] Add input validation in backend/src/api/schemas.py (email format, password strength, required fields)
- [X] T044 [US1] Add error handling for auth failures (invalid credentials, account exists, network errors) in backend/src/api/v1/auth.py
- [X] T045 [P] [US1] Create frontend/src/app/auth/signup/page.tsx with registration form (email, password, submit button)
- [X] T046 [P] [US1] Create frontend/src/app/auth/signin/page.tsx with login form (email, password, submit button, forgot password link)
- [X] T047 [US1] Implement frontend/src/lib/hooks/useAuth.ts with signup, signin, logout mutations using React Query
- [X] T048 [US1] Implement session persistence in frontend: save token to localStorage, validate on app load in frontend/src/app/layout.tsx
- [X] T049 [US1] Add auth context provider in frontend/src/components/AuthProvider.tsx for session state across app
- [X] T050 [US1] Create frontend/src/components/ProtectedRoute.tsx wrapper to redirect unauthenticated users to signin

**✅ Checkpoint**: User Story 1 complete - users can register, login, logout. Session persists. Ready for task management features.

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Display authenticated user's task list with title, completion status, and responsive layout on all devices.

**Independent Test**: Authenticated user can view empty task list → add sample task to DB → reload page → see task in list with correct details and status

### Contract Tests for US2

- [X] T051 [P] [US2] Create backend/tests/contract/test_tasks_contracts.py validating /api/v1/tasks GET endpoint against OpenAPI schema
- [X] T052 [P] [US2] Verify GET /api/v1/tasks returns Task array with id, title, completed, is_archived, created_at, updated_at fields

### Integration Tests for US2

- [X] T053 [P] [US2] Create backend/tests/integration/test_task_list.py testing list_tasks endpoint (authenticates user, creates 5 tasks, fetches list, verifies count and details)
- [X] T054 [P] [US2] Create backend/tests/integration/test_task_list.py testing empty task list (authenticated user with no tasks returns empty array, 200 status)
- [X] T055 [P] [US2] Create backend/tests/integration/test_task_list.py testing unauthenticated request (GET /tasks without session → 401 Unauthorized)
- [X] T056 [P] [US2] Create backend/tests/integration/test_task_list.py testing user data isolation (user A's tasks not visible to user B)
- [X] T057 [P] [US2] Create backend/tests/integration/test_task_list.py testing large task list performance (100+ tasks load in <2 seconds)

### Implementation for US2

- [X] T058 [P] [US2] Create Task model in backend/src/db/models.py with user_id (FK), title, completed, is_archived, created_at, updated_at fields
- [X] T059 [US2] Create backend/src/services/task_service.py with list_tasks_for_user(user_id) function (returns active tasks: completed=false, is_archived=false)
- [X] T060 [US2] Implement /api/v1/tasks GET endpoint in backend/src/api/v1/tasks.py (authenticated user → their task list filtered by user_id)
- [X] T061 [US2] Add authentication requirement to GET /tasks endpoint (middleware validates session, extracts user_id)
- [X] T062 [US2] Add query optimization in backend: index on (user_id, completed, is_archived) for fast filtering
- [X] T063 [P] [US2] Create frontend/src/components/TaskList.tsx component displaying task array, empty state when no tasks
- [X] T064 [P] [US2] Create frontend/src/components/TaskItem.tsx component for individual task display (title, completion checkbox, actions)
- [X] T065 [US2] Implement useTasks hook in frontend/src/lib/hooks/useTasks.ts with useQuery for fetching task list
- [X] T066 [US2] Create frontend/src/app/tasks/page.tsx main task list page (protected route, loads useTasks, renders TaskList component)
- [X] T067 [US2] Add responsive styling in frontend/src/components/TaskList.tsx (mobile: single column, tablet/desktop: full width, TailwindCSS)
- [X] T068 [US2] Implement loading state in TaskList.tsx (skeleton loaders while useTasks is fetching)
- [X] T069 [US2] Implement error state in TaskList.tsx (display error message, retry button if fetch fails)
- [X] T070 [US2] Add pagination or infinite scroll if needed for 100+ tasks (optional MVP - can defer if performance acceptable)

**✅ Checkpoint**: User Story 2 complete - authenticated users can view their task list with correct filtering, data isolation, responsive design. Ready for task creation.

---

## Phase 5: User Story 3 - Add Task (Priority: P1)

**Goal**: Allow authenticated users to create new tasks with title input, immediately visible in list and persisted to database.

**Independent Test**: User enters task title → clicks Add Task → task appears in list with unique ID → refreshes page → task still present

### Contract Tests for US3

- [X] T071 [P] [US3] Create backend/tests/contract/test_tasks_contracts.py validating /api/v1/tasks POST endpoint against OpenAPI schema
- [X] T072 [P] [US3] Verify POST /api/v1/tasks request requires { title: string } and returns Task object with generated id

### Integration Tests for US3

- [X] T073 [P] [US3] Create backend/tests/integration/test_create_task.py testing create_task endpoint (authenticated user, valid title → 201 Created with task object)
- [X] T074 [P] [US3] Create backend/tests/integration/test_create_task.py testing empty title validation (empty string → 400 Bad Request with error message)
- [X] T075 [P] [US3] Create backend/tests/integration/test_create_task.py testing multiple rapid task creation (5 tasks created concurrently → all persisted with unique IDs, no duplicates)
- [X] T076 [P] [US3] Create backend/tests/integration/test_create_task.py testing unauthenticated request (POST /tasks without session → 401 Unauthorized)
- [X] T077 [P] [US3] Create backend/tests/integration/test_create_task.py testing title with special characters and long strings (properly escaped, truncated if needed)

### Implementation for US3

- [X] T078 [US3] Create backend/src/services/task_service.py function create_task(user_id, title) → Task object with generated UUID, defaults (completed=false, is_archived=false)
- [X] T079 [US3] Implement /api/v1/tasks POST endpoint in backend/src/api/v1/tasks.py (authenticated user + title → create task, return 201 with task object)
- [X] T080 [US3] Add input validation in backend/src/api/schemas.py TaskCreate schema (title required, non-empty, max 500 chars)
- [X] T081 [US3] Add error handling in POST /tasks endpoint (title validation, database errors, permission denied)
- [X] T082 [US3] Ensure database mutation immediately persists (no caching delays) for Task creation
- [X] T083 [P] [US3] Create frontend/src/components/TaskForm.tsx component with title input, add button, form submission
- [X] T084 [US3] Implement useMutation for task creation in frontend/src/lib/hooks/useTasks.ts (POST /tasks, then refetch task list)
- [X] T085 [US3] Integrate TaskForm into frontend/src/app/tasks/page.tsx (form at top of page, onSubmit → createTaskMutation)
- [X] T086 [US3] Add optimistic UI in TaskForm: task appears in list immediately, rollback if creation fails
- [X] T087 [US3] Add form validation in TaskForm.tsx (empty title → show error, disable submit button)
- [X] T088 [US3] Add loading state in TaskForm.tsx (disable button while submitting, show spinner)
- [X] T089 [US3] Add success feedback in TaskForm.tsx (brief success message or toast, clear input field after submit)
- [X] T090 [US3] Add responsive design to TaskForm.tsx (mobile: single column input, desktop: inline input + button, TailwindCSS)

**✅ Checkpoint**: User Story 3 complete - users can create tasks, see them immediately, persist to DB, form has validation and feedback. MVP now has auth + view + create.

---

## Phase 6: User Story 4 - Mark Task Complete (Priority: P2)

**Goal**: Allow users to toggle task completion status, marking done tasks as complete (archived) and incomplete tasks as active. Status persists across page reloads.

**Independent Test**: User has task → clicks checkbox/complete button → task marked complete, visually distinct, archived → refreshes page → task still archived

### Contract Tests for US4

- [X] T091 [P] [US4] Create backend/tests/contract/test_tasks_contracts.py validating /api/v1/tasks/{taskId}/complete PATCH endpoint against OpenAPI schema
- [X] T092 [P] [US4] Create backend/tests/contract/test_tasks_contracts.py validating /api/v1/tasks/{taskId}/incomplete PATCH endpoint against OpenAPI schema

### Integration Tests for US4

- [X] T093 [P] [US4] Create backend/tests/integration/test_task_complete.py testing mark_complete endpoint (incomplete task → PATCH /tasks/{id}/complete → 200, task now completed=true, is_archived=true)
- [X] T094 [P] [US4] Create backend/tests/integration/test_task_complete.py testing mark_incomplete endpoint (completed task → PATCH /tasks/{id}/incomplete → 200, task now completed=false, is_archived=false)
- [X] T095 [P] [US4] Create backend/tests/integration/test_task_complete.py testing completion persistence (mark complete → GET /tasks → task not in active list, refresh → still absent)
- [X] T096 [P] [US4] Create backend/tests/integration/test_task_complete.py testing user ownership (user A marks user B's task complete → 403 Forbidden)
- [X] T097 [P] [US4] Create backend/tests/integration/test_task_complete.py testing concurrent completion (two requests mark task complete simultaneously → no data corruption, Last-Write-Wins applied)

### Implementation for US4

- [X] T098 [US4] Create backend/src/services/task_service.py function mark_task_complete(task_id, user_id) → sets completed=true, is_archived=true, updated_at=now
- [X] T099 [US4] Create backend/src/services/task_service.py function mark_task_incomplete(task_id, user_id) → sets completed=false, is_archived=false, updated_at=now
- [X] T100 [US4] Implement /api/v1/tasks/{taskId}/complete PATCH endpoint in backend/src/api/v1/tasks.py (authenticated user, task ownership validation → mark complete)
- [X] T101 [US4] Implement /api/v1/tasks/{taskId}/incomplete PATCH endpoint in backend/src/api/v1/tasks.py (authenticated user, task ownership validation → mark incomplete)
- [X] T102 [US4] Add ownership validation middleware for {taskId} endpoints (verify task belongs to authenticated user, return 403 if not)
- [X] T103 [US4] Implement Last-Write-Wins concurrency handling (no version field check, latest timestamp wins)
- [X] T104 [P] [US4] Update frontend/src/components/TaskItem.tsx with checkbox/toggle button for completion
- [X] T105 [US4] Implement createTaskMutation for task completion in frontend/src/lib/hooks/useTasks.ts (PATCH /tasks/{id}/complete)
- [X] T106 [US4] Add onclick handler to TaskItem checkbox (call complete mutation, optimistic update to UI)
- [X] T107 [US4] Add visual distinction for completed tasks in TaskItem.tsx (strikethrough, dimmed text, different background color, TailwindCSS)
- [X] T108 [US4] Implement optimistic UI: completed tasks disappear from active list immediately, show in archive view if implemented
- [X] T109 [US4] Add rollback handling if completion request fails (task reverts to incomplete in UI, error message shown)
- [X] T110 [US4] Update task list query to exclude completed (is_archived=true) tasks from /api/v1/tasks GET endpoint

**✅ Checkpoint**: User Story 4 complete - users can mark tasks complete/incomplete, visual feedback, persistence. Task completion integrated with list view.

---

## Phase 7: User Story 5 - Update Task Title (Priority: P2)

**Goal**: Allow users to edit existing task titles, persisting changes to database and updating UI.

**Independent Test**: User has task "Buy groceries" → clicks edit → changes to "Buy groceries and milk" → saves → list shows updated title → refreshes page → title persists

### Contract Tests for US5

- [X] T111 [P] [US5] Create backend/tests/contract/test_tasks_contracts.py validating /api/v1/tasks/{taskId} PUT endpoint against OpenAPI schema
- [X] T112 [P] [US5] Verify PUT /api/v1/tasks/{taskId} request requires { title: string } and returns updated Task object

### Integration Tests for US5

- [X] T113 [P] [US5] Create backend/tests/integration/test_update_task.py testing update_task endpoint (existing task, valid new title → 200 with updated task object)
- [X] T114 [P] [US5] Create backend/tests/integration/test_update_task.py testing empty title validation (empty string → 400 Bad Request)
- [X] T115 [P] [US5] Create backend/tests/integration/test_update_task.py testing update persists (update title → GET task → returns new title, refresh → still updated)
- [X] T116 [P] [US5] Create backend/tests/integration/test_update_task.py testing user ownership (user A updates user B's task → 403 Forbidden)
- [X] T117 [P] [US5] Create backend/tests/integration/test_update_task.py testing completion status unchanged (update title on completed task → completion status remains unchanged)

### Implementation for US5

- [X] T118 [US5] Create backend/src/services/task_service.py function update_task_title(task_id, user_id, new_title) → updates title, updated_at=now
- [X] T119 [US5] Implement /api/v1/tasks/{taskId} PUT endpoint in backend/src/api/v1/tasks.py (authenticated user, task ownership validation, new title → update task)
- [X] T120 [US5] Add input validation to TaskUpdate schema (title required, non-empty, max 500 chars)
- [X] T121 [US5] Ensure update endpoint doesn't modify completed/is_archived status (only title field updated)
- [X] T122 [P] [US5] Create frontend/src/components/TaskEditForm.tsx component with title input, save/cancel buttons, edit mode toggle
- [X] T123 [US5] Implement useMutation for task update in frontend/src/lib/hooks/useTasks.ts (PUT /tasks/{id}, then refetch or optimistic update)
- [X] T124 [US5] Add edit button/link in TaskItem.tsx to trigger edit mode
- [X] T125 [US5] Implement TaskItem edit mode: hide display, show TaskEditForm inline
- [X] T126 [US5] Add optimistic UI: title updates in list immediately, reverts if update fails
- [X] T127 [US5] Add form validation in TaskEditForm.tsx (empty title → show error, disable save)
- [X] T128 [US5] Add loading state in TaskEditForm.tsx (disable buttons while saving, show spinner)
- [X] T129 [US5] Add cancel button to exit edit mode without saving
- [X] T130 [US5] Add success feedback in TaskEditForm.tsx (brief message, exit edit mode on success)

**✅ Checkpoint**: User Story 5 complete - users can edit task titles, changes persist. All P2 stories done.

---

## Phase 8: User Story 6 - Delete Task (Priority: P3)

**Goal**: Allow users to delete tasks (hard-delete explicit deletions; completed tasks auto-archive when marked complete). Deleted tasks removed from list and database.

**Independent Test**: User has task → clicks delete → task disappears from list → refreshes page → task absent (hard deleted)

### Contract Tests for US6

- [X] T131 [P] [US6] Create backend/tests/contract/test_tasks_contracts.py validating /api/v1/tasks/{taskId} DELETE endpoint against OpenAPI schema
- [X] T132 [P] [US6] Verify DELETE /api/v1/tasks/{taskId} returns 204 No Content on success

### Integration Tests for US6

- [X] T133 [P] [US6] Create backend/tests/integration/test_delete_task.py testing delete_task endpoint (existing task → DELETE /tasks/{id} → 204, task removed from DB)
- [X] T134 [P] [US6] Create backend/tests/integration/test_delete_task.py testing deletion persists (delete task → GET /tasks → task absent, refresh → still absent)
- [X] T135 [P] [US6] Create backend/tests/integration/test_delete_task.py testing user ownership (user A deletes user B's task → 403 Forbidden)
- [X] T136 [P] [US6] Create backend/tests/integration/test_delete_task.py testing delete confirmation workflow (if UI implements confirmation dialog)
- [X] T137 [P] [US6] Create backend/tests/integration/test_delete_task.py testing delete on completed task (completed tasks should NOT be deletable via PATCH /complete, only explicit DELETE)

### Implementation for US6

- [X] T138 [US6] Create backend/src/services/task_service.py function delete_task(task_id, user_id) → removes task from database (hard delete)
- [X] T139 [US6] Implement /api/v1/tasks/{taskId} DELETE endpoint in backend/src/api/v1/tasks.py (authenticated user, task ownership validation → delete task)
- [X] T140 [US6] Add ownership validation to DELETE /tasks/{taskId} endpoint (403 if task doesn't belong to user)
- [X] T141 [US6] Ensure CASCADE delete is properly configured in database (deleting task doesn't cascade to other records)
- [X] T142 [P] [US6] Add delete button to TaskItem.tsx component
- [X] T143 [US6] Implement useMutation for task deletion in frontend/src/lib/hooks/useTasks.ts (DELETE /tasks/{id}, then refetch list)
- [X] T144 [US6] Add delete confirmation dialog in TaskItem.tsx (confirm before deleting, cancel option)
- [X] T145 [US6] Implement optimistic UI: task disappears from list immediately, reappears if deletion fails
- [X] T146 [US6] Add error handling if deletion fails (show error message, restore task to list)
- [X] T147 [US6] Add success feedback for deletion (brief message or toast confirmation)
- [X] T148 [US6] Ensure delete button is only shown on incomplete tasks. Completed/archived tasks are hidden from active list (not deletable in Phase II; archive view deferred to Phase III)

**✅ Checkpoint**: User Story 6 complete - users can delete tasks (hard-deleted from DB). All user stories implemented.

---

## Phase 9: Integration & Polish

**Purpose**: Cross-story integration, edge case handling, performance optimization, documentation

- [ ] T149 [P] Implement database migrations runner in startup (backend/src/main.py runs alembic upgrade head on app start)
- [ ] T150 [P] Add comprehensive logging to backend services (auth, task operations, errors) for debugging and monitoring
- [ ] T151 [P] Implement request/response logging middleware in backend for API debugging
- [ ] T152 Add error tracking/reporting (Sentry or similar) for production error visibility
- [ ] T153 [P] Add CORS configuration in backend/src/main.py for frontend domain (allow credentials, specific methods)
- [ ] T154 [P] Test session expiration flow (expired session → automatic redirect to signin page, graceful logout)
- [ ] T155 [P] Test network failure scenarios (create/update/delete with network error → UI shows error, user can retry)
- [ ] T156 Test concurrent operations (two users modifying tasks simultaneously → Last-Write-Wins, no data corruption)
- [ ] T157 [P] Test rapid task creation (5+ tasks created in quick succession → all unique IDs, no duplicates)
- [ ] T158 Load test with 100+ tasks per user (verify <2 second load time per SC-002)
- [ ] T159 Performance optimization: ensure DB queries use proper indexes (user_id, completed, is_archived)
- [ ] T160 [P] Test mobile responsiveness: verify all pages render correctly on 320px, 768px, 1024px, 2560px widths
- [ ] T161 [P] Test accessibility: keyboard navigation, screen reader compatibility (basic WCAG)
- [ ] T162 Add unit tests for backend services (auth_service, task_service functions without DB)
- [ ] T163 Add unit tests for frontend components (TaskItem, TaskList, TaskForm component rendering tests)
- [ ] T164 Create API documentation: update backend/src/main.py OpenAPI config for auto-docs at /api/v1/docs
- [ ] T165 Update README.md files: backend/README.md and frontend/README.md with setup, running, testing instructions
- [ ] T166 Validate quickstart.md guide: follow all steps, verify project runs without errors
- [ ] T167 [P] Add production config: environment variables for production deployment (database URL, auth secret, CORS domain)
- [ ] T168 Add database backup script and documentation
- [ ] T169 Create deployment guide for Phase III (serverless backend, Next.js frontend on Vercel)

**✅ Checkpoint**: All user stories integrated, tested, documented. MVP complete and production-ready.

---

## Dependencies & Execution Order

### Phase Completion Order

1. **Phase 1 (Setup)**: Start immediately - initialize projects
2. **Phase 2 (Foundational)**: Start after Phase 1 - BLOCKS all user stories
3. **Phases 3-8 (User Stories)**: Can start in parallel once Phase 2 completes
   - Recommended sequential order: US1 → US2 → US3 → US4 → US5 → US6
   - Or parallel if team capacity: US1+US2+US3 in parallel (all P1), then US4+US5 in parallel (P2), then US6 (P3)
4. **Phase 9 (Integration & Polish)**: After desired user stories complete, before production deployment

### User Story Dependencies

- **US1 (Auth)**: No dependencies - can start immediately after Phase 2
- **US2 (View Tasks)**: Depends on US1 (requires authenticated user) - can start after US1 complete
- **US3 (Add Task)**: Depends on US1 and US2 (requires auth + task list exists) - can start after US1+US2
- **US4 (Mark Complete)**: Depends on US1+US3 (requires auth + tasks exist) - can start after US3
- **US5 (Update Title)**: Depends on US1+US3 (requires auth + tasks exist) - can start after US3
- **US6 (Delete Task)**: Depends on US1+US3 (requires auth + tasks exist) - can start after US3

### Parallel Opportunities

**Phase 1 - All [P] tasks run in parallel**:
- T003, T004, T005, T006 can all execute simultaneously

**Phase 2 - Multiple developers**:
- Developer A: T010-T011 (database setup)
- Developer B: T012-T020 (backend API infrastructure)
- Developer C: T021-T031 (frontend setup + testing infrastructure)
- All complete before user story work starts

**User Stories - With team capacity**:
- Developer A: Phase 3 (US1 - Auth) - prerequisite for all others
- After US1 completes:
  - Developer A: Phase 4 (US2 - View Tasks)
  - Developer B: Phase 5 (US3 - Add Task) in parallel
  - Developer C: Phase 6+ (US4+, US5+) in parallel

**Within each Phase**:
- All contract tests [P] for a story can run in parallel
- All models [P] for a story can run in parallel
- Frontend components for different features can be built in parallel

### MVP Scope Recommendation

**Minimum Viable Product - Stop after Phase 5 (User Story 3)**:
- Phase 1: Setup ✅
- Phase 2: Foundational ✅
- Phase 3: US1 Authentication ✅
- Phase 4: US2 View Tasks ✅
- Phase 5: US3 Add Tasks ✅

**Why**: Users can register, view empty list, create tasks. Full todo app functionality with core value. Ship, gather feedback.

**Extend MVP - Add Phase 6 (User Story 4)**:
- Phase 6: US4 Mark Complete ✅

**Why**: Now users can track done vs todo. More complete task management workflow.

**Full Implementation - Complete all Phases**:
- Phases 7-9: US5, US6, Integration & Polish
- Complete feature set with edit, delete, archive, all edge cases handled

---

## Summary Statistics

- **Total Tasks**: 169
- **Setup Tasks**: 9
- **Foundational Tasks**: 22 (BLOCKING - must complete first)
- **User Story 1 (Auth)**: 19 tasks
- **User Story 2 (View)**: 20 tasks
- **User Story 3 (Add)**: 20 tasks
- **User Story 4 (Complete)**: 20 tasks
- **User Story 5 (Update)**: 20 tasks
- **User Story 6 (Delete)**: 17 tasks
- **Integration & Polish**: 21 tasks

**Parallelizable Tasks**: ~80 marked [P]  
**Sequential Tasks**: ~89 with dependencies

**Estimated Timeline** (single developer):
- Phase 1: 1 day
- Phase 2: 3 days
- US1-US3 (MVP): 10 days
- US4-US6 + Integration: 12 days
- **Total**: ~26 days for full implementation

**With 3-person team** (parallel execution):
- Phase 1 + 2: 5 days (same, foundational)
- US1-US6 + Integration: 8 days (parallel stories)
- **Total**: ~13 days for full implementation

---

## Task Format Validation Checklist

Every task follows strict format:
- ✅ Checkbox: `- [ ]` at start
- ✅ Task ID: Sequential T001-T169
- ✅ Parallelizable marker: [P] when applicable
- ✅ Story label: [US#] for user story tasks only
- ✅ Description: Clear action with exact file path
- ✅ No vague instructions (each task is immediately actionable)
- ✅ Dependencies tracked and documented
- ✅ File paths match project structure from plan.md

---

## Implementation Notes

1. **Test-First Approach**: Run each test task FIRST to establish acceptance criteria, verify tests FAIL before implementing
2. **Commit Strategy**: Commit after each user story phase completes (not per individual task)
3. **Review Gates**: At each checkpoint, verify story is independently testable before moving to next
4. **Constitution Compliance**: All implementation must follow IV. Test-First Development (tests before code)
5. **PHR Creation**: Create PHR after each user story phase completes documenting work completed, tests passing, integration status
6. **Deployment**: After Phase 5 (MVP), can deploy to production; Phases 6+ are incremental enhancements

---

**Status**: ✅ Ready to implement
**Next Command**: Start Phase 1 setup tasks with `/sp.implement` or begin manually with T001-T009
