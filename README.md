# Todo Evolution - Hackathon II

A todo application demonstrating **Spec-Driven Development** - evolving from a simple console app to a cloud-native AI chatbot.

## Current Phase: Phase II (Full-Stack Web App)

| Phase | Description | Status |
|-------|-------------|--------|
| I | In-Memory Console App | Completed |
| II | Full-Stack Web Application | **Active** |
| III | AI-Powered Chatbot | Planned |
| IV | Local Kubernetes | Planned |
| V | Cloud Deployment | Planned |

## Quick Start

### Phase I - Console App
```bash
cd phase1-console/
uv sync
uv run python -m src.todo_console.main
```

### Phase II - Web App (Coming Soon)
```bash
# Backend
cd backend/
uv sync
uv run uvicorn src.todo_api.main:app --reload

# Frontend
cd frontend/
pnpm install
pnpm dev
```

## Project Structure

```
hackathon-todo/
├── phase1-console/       # Phase I: TUI app (completed)
├── backend/              # Phase II: FastAPI
├── frontend/             # Phase II: Next.js
├── specs/                # Feature specifications
├── .specify/             # Spec-Kit configuration
└── history/              # Prompt history records
```

## Technology Stack

### Phase II
- **Frontend:** Next.js 16+ (App Router), TypeScript
- **Backend:** FastAPI, SQLModel, Python 3.13+
- **Database:** Neon Serverless PostgreSQL
- **Auth:** Better Auth with JWT

## Features

### Basic (All Phases)
- Add Task
- View Task List
- Update Task
- Delete Task
- Mark Complete

### Phase II Additions
- User Authentication
- Persistent Storage
- RESTful API
- Web UI

## Development

This project uses **Spec-Driven Development**:

1. Write specifications in `specs/`
2. Generate implementation plans
3. Build from specs using Claude Code
4. Document with Prompt History Records

See `CLAUDE.md` for detailed development guidelines.

## Documentation

| Document | Location |
|----------|----------|
| Constitution | `.specify/memory/constitution.md` |
| Project Overview | `specs/overview.md` |
| Phase I Docs | `phase1-console/README.md` |
| Backend Docs | `backend/CLAUDE.md` |
| Frontend Docs | `frontend/CLAUDE.md` |

## License

MIT
