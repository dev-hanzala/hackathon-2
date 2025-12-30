# Development Tasks: Todo MVP CLI

**Branch**: `001-todo-mvp-cli` | **Date**: 2025-12-30 | **Plan**: /home/hanza/hackathon-2/specs/001-todo-mvp-cli/plan.md

## Overview

This document outlines the step-by-step implementation tasks for the Phase I Todo MVP CLI application, based on the approved specification and implementation plan. Tasks are organized into phases, prioritizing foundational elements and then addressing user stories in their defined priority order.

## Implementation Strategy

The implementation will follow an MVP-first approach, focusing on delivering core functionality incrementally. Each user story is designed to be independently testable to ensure continuous value delivery and ease of integration. Parallelizable tasks are explicitly marked.

## Task Dependency Graph

```mermaid
graph TD
    A[Phase 1: Setup] --> B[Phase 2: Foundational]
    B --> C[Phase 3: User Story 1 (Add Task)]
    B --> D[Phase 4: User Story 2 (View Task List)]
    B --> E[Phase 5: User Story 3 (Mark Task Complete)]
    C --> F[Phase 6: User Story 4 (Update Task)]
    C --> G[Phase 7: User Story 5 (Delete Task)]
    D --> F
    D --> G
    E --> F
    E --> G
    F --> H[Phase 8: Polish & Cross-Cutting]
    G --> H
```

## Parallel Execution Opportunities

**Within User Stories**: Tasks marked with `[P]` can be executed in parallel if they operate on different files or have no direct dependencies on other in-progress tasks within the same story.

**Across User Stories (P2/P3)**: Once all P1 stories are functionally complete and basic integration tests pass, P2 and P3 stories can potentially be implemented in parallel, assuming no direct data model or logical conflicts.

## Tasks

### Phase 1: Setup

- [ ] T001 Create `src/todo_console/__init__.py`
- [ ] T002 Create `src/todo_console/models.py`
- [ ] T003 Create `src/todo_console/main.py`
- [ ] T004 Create `tests/unit/test_models.py`
- [ ] T005 Create `tests/integration/test_cli.py`

### Phase 2: Foundational

- [ ] T006 Implement Task data class in `src/todo_console/models.py` with `id`, `title`, `description`, `status` attributes.
- [ ] T007 Implement in-memory global task storage (e.g., `TODOS: list[Task] = []`) and `next_id` counter in `src/todo_console/models.py`.
- [ ] T008 Add basic CLI command parsing structure in `src/todo_console/main.py`.

### Phase 3: User Story 1 - Add Task (Priority: P1)

**Goal**: User can add a new task with a title and an optional description.
**Independent Test**: Add a task via CLI and verify its presence using the `list` command (once implemented).

- [ ] T009 [P] [US1] Implement `add_task` function in `src/todo_console/models.py` to create a new `Task` and add it to global storage, assigning a unique ID and default status 'pending'.
- [ ] T010 [P] [US1] Implement unit tests for `add_task` in `tests/unit/test_models.py`.
- [ ] T011 [US1] Integrate 'add' command parsing and calling `add_task` in `src/todo_console/main.py`, including user feedback.
- [ ] T012 [US1] Implement integration tests for 'add' command in `tests/integration/test_cli.py`.

### Phase 4: User Story 2 - View Task List (Priority: P1)

**Goal**: User can view all existing tasks, showing their ID, title, description, and status.
**Independent Test**: Add multiple tasks via CLI and then list them to verify correct display.

- [ ] T013 [P] [US2] Implement `get_all_tasks` function in `src/todo_console/models.py` to return the current list of tasks.
- [ ] T014 [P] [US2] Implement unit tests for `get_all_tasks` in `tests/unit/test_models.py`.
- [ ] T015 [US2] Integrate 'list' command parsing and calling `get_all_tasks` in `src/todo_console/main.py`, formatting output for display.
- [ ] T016 [US2] Implement integration tests for 'list' command in `tests/integration/test_cli.py`.

### Phase 5: User Story 3 - Mark Task Complete (Priority: P1)

**Goal**: User can mark an existing task as complete using its ID.
**Independent Test**: Add a task, mark it complete via CLI, and then list it to verify updated status.

- [ ] T017 [P] [US3] Implement `mark_task_complete` function in `src/todo_console/models.py` to find a task by ID and update its status to 'completed'. Handle task not found cases.
- [ ] T018 [P] [US3] Implement unit tests for `mark_task_complete` in `tests/unit/test_models.py`.
- [ ] T019 [US3] Integrate 'complete' command parsing and calling `mark_task_complete` in `src/todo_console/main.py`, including user feedback.
- [ ] T020 [US3] Implement integration tests for 'complete' command in `tests/integration/test_cli.py`.

### Phase 6: User Story 4 - Update Task (Priority: P2)

**Goal**: User can update the title, description, or both for an existing task using its ID.
**Independent Test**: Add a task, update its details via CLI, and then list it to verify changes.

- [ ] T021 [P] [US4] Implement `update_task` function in `src/todo_console/models.py` to find a task by ID and update its title and/or description. Handle task not found cases.
- [ ] T022 [P] [US4] Implement unit tests for `update_task` in `tests/unit/test_models.py`.
- [ ] T023 [US4] Integrate 'update' command parsing and calling `update_task` in `src/todo_console/main.py`, including user feedback.
- [ ] T024 [US4] Implement integration tests for 'update' command in `tests/integration/test_cli.py`.

### Phase 7: User Story 5 - Delete Task (Priority: P2)

**Goal**: User can delete an existing task using its ID.
**Independent Test**: Add a task, delete it via CLI, and then list to confirm its removal.

- [ ] T025 [P] [US5] Implement `delete_task` function in `src/todo_console/models.py` to remove a task by ID from global storage. Handle task not found cases.
- [ ] T026 [P] [US5] Implement unit tests for `delete_task` in `tests/unit/test_models.py`.
- [ ] T027 [US5] Integrate 'delete' command parsing and calling `delete_task` in `src/todo_console/main.py`, including user feedback.
- [ ] T028 [US5] Implement integration tests for 'delete' command in `tests/integration/test_cli.py`.

### Phase 8: Polish & Cross-Cutting Concerns

- [ ] T029 Refine CLI input parsing for robustness and error handling in `src/todo_console/main.py`.
- [ ] T030 Ensure all CLI commands provide clear and consistent success/error messages in `src/todo_console/main.py`.
- [ ] T031 Run `uv run ruff check .` and fix any linting/formatting issues.
- [ ] T032 Run `uv run pytest` to ensure all tests pass.

