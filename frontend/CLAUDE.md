# Frontend Service: Next.js Todo App

## Service Overview

This is the frontend service for the Todo Evolution application. It provides a web-based UI built with Next.js 16+ using the App Router.

**Parent Constitution:** `../.specify/memory/constitution.md`

---

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | Next.js | 16+ |
| Router | App Router | - |
| Language | TypeScript | 5+ |
| Package Manager | pnpm | Latest |
| Styling | Tailwind CSS | 4+ |
| State | React Server Components + Client State | - |
| Testing | Vitest + Playwright | Latest |

---

## Commands

```bash
# Navigate to frontend directory
cd frontend/

# Install dependencies
pnpm install

# Run development server
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start

# Run unit tests
pnpm test

# Run E2E tests
pnpm test:e2e

# Lint code
pnpm lint

# Type check
pnpm typecheck

# Generate API client from OpenAPI
pnpm generate:api
```

---

## Directory Structure

```
frontend/
├── CLAUDE.md               # This file
├── package.json
├── tsconfig.json
├── next.config.ts
├── tailwind.config.ts
├── src/
│   ├── app/                # Next.js App Router
│   │   ├── layout.tsx      # Root layout
│   │   ├── page.tsx        # Home page
│   │   ├── (auth)/         # Auth route group
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── register/
│   │   │       └── page.tsx
│   │   └── (dashboard)/    # Protected route group
│   │       ├── layout.tsx  # Dashboard layout with auth
│   │       └── todos/
│   │           └── page.tsx
│   ├── components/         # React components
│   │   ├── ui/             # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   └── Card.tsx
│   │   ├── todos/          # Todo-specific components
│   │   │   ├── TodoList.tsx
│   │   │   ├── TodoItem.tsx
│   │   │   └── TodoForm.tsx
│   │   └── auth/           # Auth components
│   │       ├── LoginForm.tsx
│   │       └── RegisterForm.tsx
│   ├── lib/                # Utilities and helpers
│   │   ├── api.ts          # API client (generated from OpenAPI)
│   │   ├── auth.ts         # Auth utilities
│   │   └── utils.ts        # General utilities
│   ├── hooks/              # Custom React hooks
│   │   ├── useTodos.ts
│   │   └── useAuth.ts
│   └── types/              # TypeScript types
│       ├── api.ts          # API types (generated)
│       └── index.ts
├── public/                 # Static assets
└── tests/
    ├── unit/               # Vitest unit tests
    └── e2e/                # Playwright E2E tests
```

---

## Pages & Routes

### Public Routes
| Route | Description |
|-------|-------------|
| `/` | Landing page |
| `/login` | Login form |
| `/register` | Registration form |

### Protected Routes (require authentication)
| Route | Description |
|-------|-------------|
| `/todos` | Todo list dashboard |

---

## Environment Variables

```bash
# .env.local (DO NOT COMMIT)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Coding Standards

### Components
- **Functional components only** with TypeScript
- **React Server Components** by default, add `'use client'` only when needed
- **Props interfaces** defined inline or in types/
- **No `any` types** without explicit justification

### File Naming
- Components: `PascalCase.tsx` (e.g., `TodoItem.tsx`)
- Utilities: `camelCase.ts` (e.g., `formatDate.ts`)
- Hooks: `useCamelCase.ts` (e.g., `useTodos.ts`)

### State Management
- Server state: React Server Components + Server Actions
- Client state: React useState/useReducer for local UI state
- API cache: SWR or React Query for client-side data fetching

### Styling
- Tailwind CSS for all styling
- Use `cn()` utility for conditional classes
- Component variants via CVA (Class Variance Authority) if needed

### API Integration
- Generate typed client from backend OpenAPI spec
- Handle loading, error, and success states
- Use React Suspense for async boundaries

---

## Authentication Flow

1. User submits login/register form
2. Frontend calls backend `/auth/login` or `/auth/register`
3. JWT token stored in httpOnly cookie (set by backend)
4. Middleware checks auth on protected routes
5. API requests include cookie automatically
6. Token refresh handled transparently

---

## Component Patterns

### Server Component (default)
```tsx
// src/app/todos/page.tsx
import { getTodos } from '@/lib/api'

export default async function TodosPage() {
  const todos = await getTodos()
  return <TodoList todos={todos} />
}
```

### Client Component (interactive)
```tsx
// src/components/todos/TodoItem.tsx
'use client'

interface TodoItemProps {
  todo: Todo
  onComplete: (id: number) => void
}

export function TodoItem({ todo, onComplete }: TodoItemProps) {
  return (
    <div onClick={() => onComplete(todo.id)}>
      {todo.title}
    </div>
  )
}
```

---

## Testing

### Unit Tests (Vitest)
- Test component rendering
- Test hooks in isolation
- Test utility functions
- Mock API calls

### E2E Tests (Playwright)
- Test full user flows
- Test authentication flow
- Test CRUD operations
- Test error states
