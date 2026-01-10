# Todo Evolution - Project Overview

## Purpose

A todo application that evolves from a simple console app to a cloud-native AI chatbot, demonstrating Spec-Driven Development with Claude Code and Spec-Kit.

## Vision

Transform a simple Python console app into a production-grade, Kubernetes-managed, event-driven AI-powered distributed system using spec-driven development principles.

## Current Phase

**Phase II: Full-Stack Web Application**

### Phase II Objectives
- Transform console app into multi-user web application
- Implement RESTful API with FastAPI backend
- Build responsive Next.js 16+ frontend with App Router
- Add persistent storage with Neon PostgreSQL
- Implement user authentication with Better Auth + JWT

## Project Phases

| Phase | Description | Status |
|-------|-------------|--------|
| Phase I | In-Memory Console/TUI App | Completed |
| Phase II | Full-Stack Web Application | Active |
| Phase III | AI-Powered Todo Chatbot | Planned |
| Phase IV | Local Kubernetes Deployment | Planned |
| Phase V | Cloud Deployment (DOKS) | Planned |

## Technology Stack

### Phase I (Completed)
- Python 3.13+, Textual TUI, In-memory storage

### Phase II (Active)
- **Frontend:** Next.js 16+ (App Router), TypeScript
- **Backend:** FastAPI, SQLModel
- **Database:** Neon Serverless PostgreSQL
- **Auth:** Better Auth with JWT

### Phase III+ (Planned)
- OpenAI Agents SDK, MCP Server
- Docker, Kubernetes, Helm
- Kafka, Dapr

## Features

### Basic Level (All Phases)
- [x] Add Task
- [x] Delete Task
- [x] Update Task
- [x] View Task List
- [x] Mark as Complete

### Phase II Additions
- [ ] User Authentication (Better Auth)
- [ ] Persistent Storage (PostgreSQL)
- [ ] RESTful API
- [ ] Web UI

### Intermediate Level (Phase V)
- [ ] Priorities & Tags/Categories
- [ ] Search & Filter
- [ ] Sort Tasks

### Advanced Level (Phase V)
- [ ] Recurring Tasks
- [ ] Due Dates & Reminders

## Repository Structure

```
hackathon-todo/
├── .specify/                 # Spec-Kit configuration
├── specs/                    # Feature specifications
│   ├── overview.md           # This file
│   ├── features/             # Feature specs
│   ├── api/                  # API specs
│   ├── database/             # Database specs
│   └── ui/                   # UI specs
├── phase1-console/           # Phase I: Console app
├── backend/                  # Phase II: FastAPI
├── frontend/                 # Phase II: Next.js
└── history/                  # PHR records
```

## Governance

- **Constitution:** `.specify/memory/constitution.md`
- **Spec-Driven:** All code generated from specs
- **PHR Required:** Document significant interactions
