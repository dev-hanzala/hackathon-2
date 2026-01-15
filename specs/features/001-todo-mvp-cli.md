# Feature: Todo MVP CLI (Phase I - Completed)

**Phase**: I - In-Memory Console App
**Status**: Completed
**Location**: `phase1-console/`

## Overview

Phase I implements a command-line todo application with in-memory storage, demonstrating core CRUD operations using Python and Textual TUI.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Runtime | Python 3.13+ |
| Package Manager | uv |
| UI | Textual TUI |
| Storage | In-memory |
| Testing | pytest |

## User Stories

### US-001: Add Task (P1)

**As a** user
**I want to** add a new task with a title and optional description
**So that** I can track things I need to do

**Acceptance Criteria:**
- Title is required (1-200 characters)
- Description is optional (max 1000 characters)
- Task is assigned a unique ID
- Task defaults to "pending" status
- Success message displayed after creation

### US-002: View Task List (P1)

**As a** user
**I want to** view all my tasks
**So that** I can see what needs to be done

**Acceptance Criteria:**
- Display task ID, title, description, and status
- Show "pending" or "completed" status indicator
- Handle empty list gracefully
- Formatted, readable output

### US-003: Mark Task Complete (P1)

**As a** user
**I want to** mark a task as complete by ID
**So that** I can track my progress

**Acceptance Criteria:**
- Accept task ID as parameter
- Update status to "completed"
- Handle already-completed tasks gracefully
- Display error for non-existent IDs

### US-004: Update Task (P2)

**As a** user
**I want to** update a task's title or description
**So that** I can correct or refine task details

**Acceptance Criteria:**
- Update title, description, or both
- Preserve unchanged fields
- Display error for non-existent IDs

### US-005: Delete Task (P2)

**As a** user
**I want to** delete a task by ID
**So that** I can remove completed or irrelevant tasks

**Acceptance Criteria:**
- Remove task from storage
- Display error for non-existent IDs
- Confirm deletion with success message

## Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-001 | System MUST allow adding tasks with title and optional description |
| FR-002 | System MUST display all tasks with ID, title, description, status |
| FR-003 | System MUST allow marking tasks as complete by ID |
| FR-004 | System MUST allow updating task title/description by ID |
| FR-005 | System MUST allow deleting tasks by ID |
| FR-006 | System MUST use in-memory storage |
| FR-007 | System MUST provide command-line/TUI interface |
| FR-008 | System MUST provide clear feedback messages |
| FR-009 | System MUST handle non-existent task IDs gracefully |
| FR-010 | System MUST assign unique identifiers to tasks |
| FR-011 | System MUST support 'pending' and 'completed' status |

## Data Model

```python
@dataclass
class Task:
    id: int           # Unique identifier (auto-assigned)
    title: str        # Task title (required)
    description: str  # Task description (optional)
    status: str       # 'pending' or 'completed'
```

## Project Structure

```
phase1-console/
├── src/
│   └── todo_console/
│       ├── __init__.py
│       ├── main.py      # TUI entry point
│       ├── models.py    # Task data model
│       └── tui.py       # Textual UI components
├── tests/
│   └── unit/
│       └── test_models.py
├── pyproject.toml
└── CLAUDE.md
```

## Success Criteria

- [x] All 5 CRUD operations functional
- [x] TUI interface operational
- [x] In-memory storage working
- [x] Clear user feedback messages
- [x] Tests passing

## Commands

```bash
cd phase1-console/
uv run python -m src.todo_console.main   # Run TUI
uv run pytest                             # Run tests
```

## Lessons Learned

1. In-memory storage works well for MVP prototyping
2. Textual TUI provides rich console UI capabilities
3. Spec-driven development ensures clear requirements
