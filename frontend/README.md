# Todo App Frontend

Modern, responsive todo application frontend built with Next.js 16, TypeScript, and TailwindCSS.

## Features

- **User Authentication**: Registration and signin with JWT
- **Task Management**: Create, view, update, complete, and delete tasks
- **Real-time Updates**: Optimistic UI with automatic refetch
- **Responsive Design**: Mobile-first, works on all devices (320px - 2560px+)
- **Type-Safe**: Full TypeScript coverage
- **Modern Stack**: Next.js 16 App Router with Turbopack

## Tech Stack

- **Framework**: Next.js 16.1.2 (App Router)
- **Language**: TypeScript 5.3.3
- **Styling**: TailwindCSS 3.4.1
- **State Management**: React Query (@tanstack/react-query 5.40.0)
- **Authentication**: better-auth 1.4.10
- **Testing**: Jest 29.7.0, React Testing Library 16.0.0
- **Package Manager**: pnpm

## Prerequisites

- Node.js 18+
- pnpm (install: `npm install -g pnpm`)
- Backend API running (see `../backend/README.md`)

## Quick Start

### 1. Installation

```bash
# Navigate to frontend
cd frontend

# Install dependencies
pnpm install
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.local.example .env.local

# Edit .env.local with your configuration
nano .env.local
```

**Required environment variables:**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1
NEXT_PUBLIC_ENVIRONMENT=development
NEXT_PUBLIC_DEBUG=true
```

### 3. Run Development Server

```bash
# Start dev server with Turbopack
pnpm dev

# Server runs at http://localhost:3000
```

### 4. Verify Setup

```bash
# Open browser
open http://localhost:3000

# Should show signin page
# Register a new user and start creating tasks!
```

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout with providers
│   │   ├── page.tsx            # Landing/home page
│   │   ├── auth/
│   │   │   ├── signin/
│   │   │   │   └── page.tsx    # Sign in page
│   │   │   └── signup/
│   │   │       └── page.tsx    # Registration page
│   │   └── tasks/
│   │       └── page.tsx        # Main task list page (protected)
│   ├── components/
│   │   ├── AuthProvider.tsx    # Auth context provider
│   │   ├── ProtectedRoute.tsx  # Route protection wrapper
│   │   ├── ErrorBoundary.tsx   # Error handling component
│   │   ├── TaskList.tsx        # Task list container
│   │   ├── TaskItem.tsx        # Individual task component
│   │   ├── TaskForm.tsx        # Task creation form
│   │   └── TaskEditForm.tsx    # Task editing form
│   ├── lib/
│   │   ├── types.ts            # TypeScript interfaces
│   │   ├── api-client.ts       # Fetch wrapper for API calls
│   │   └── hooks/
│   │       ├── useAuth.ts      # Authentication hook
│   │       └── useTasks.ts     # Task management hook
│   └── styles/
│       └── globals.css         # Global styles & TailwindCSS
├── tests/
│   ├── setup.ts                # Jest configuration
│   └── __tests__/              # Component tests
├── public/                      # Static assets
├── next.config.js              # Next.js configuration
├── tailwind.config.js          # TailwindCSS configuration
├── tsconfig.json               # TypeScript configuration
├── jest.config.js              # Jest testing configuration
├── .env.local.example          # Development environment template
└── package.json                # Dependencies & scripts
```

## Available Scripts

### Development

```bash
# Start development server (with Turbopack)
pnpm dev

# Start on different port
pnpm dev -- -p 3001
```

### Building

```bash
# Create production build
pnpm build

# Start production server
pnpm start

# Preview production build locally
pnpm build && pnpm start
```

### Testing

```bash
# Run all tests
pnpm test

# Run tests in watch mode
pnpm test:watch

# Run tests with coverage
pnpm test:coverage

# Run specific test file
pnpm test TaskList.test.tsx
```

### Code Quality

```bash
# Type checking
pnpm type-check

# Or use TypeScript compiler directly
npx tsc --noEmit

# Lint code (if ESLint configured)
pnpm lint

# Format code (if Prettier configured)
pnpm format
```

## Development Workflow

### Creating New Features

1. **Create page** in `src/app/your-feature/page.tsx`
2. **Create components** in `src/components/`
3. **Add types** in `src/lib/types.ts`
4. **Create hooks** in `src/lib/hooks/` if needed
5. **Add tests** in `tests/__tests__/`
6. **Update routes** and navigation

### Component Pattern

```tsx
// src/components/MyComponent.tsx
'use client'; // If using hooks/state

import { useState } from 'react';

interface MyComponentProps {
  title: string;
  onAction?: () => void;
}

export function MyComponent({ title, onAction }: MyComponentProps) {
  const [state, setState] = useState(false);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold">{title}</h2>
      <button onClick={onAction} className="btn-primary">
        Action
      </button>
    </div>
  );
}
```

### API Integration Pattern

```tsx
// src/lib/hooks/useMyData.ts
'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';

export function useMyData() {
  const queryClient = useQueryClient();

  const { data, isLoading, error } = useQuery({
    queryKey: ['myData'],
    queryFn: () => apiClient.get('/api/v1/mydata'),
  });

  const createMutation = useMutation({
    mutationFn: (newData) => apiClient.post('/api/v1/mydata', newData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['myData'] });
    },
  });

  return { data, isLoading, error, create: createMutation.mutate };
}
```

## Authentication Flow

1. **Unauthenticated**: User sees signin page at `/auth/signin`
2. **Register**: User creates account at `/auth/signup`
3. **Auto-login**: After registration, JWT token stored in localStorage
4. **Protected Routes**: Token validated on protected pages (e.g., `/tasks`)
5. **Session Persistence**: Token persists across page reloads
6. **Logout**: Token removed from localStorage, user redirected to signin

### Token Storage

```typescript
// Tokens stored in localStorage
localStorage.setItem('auth_token', token);
localStorage.getItem('auth_token');
localStorage.removeItem('auth_token');

// Auto-attached to API requests via api-client.ts
```

## Styling Guide

### TailwindCSS Utilities

```tsx
// Common patterns used in this project

// Buttons
<button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
  Primary Action
</button>

// Cards
<div className="bg-white rounded-lg shadow p-4">
  Card Content
</div>

// Forms
<input 
  className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2"
  type="text"
/>

// Responsive Design
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  ...
</div>

// Loading States
<div className="animate-pulse bg-gray-200 h-4 rounded" />
```

### Responsive Breakpoints

- **Mobile**: 320px - 767px (default)
- **Tablet**: 768px - 1023px (`md:`)
- **Desktop**: 1024px - 1279px (`lg:`)
- **Large**: 1280px+ (`xl:`, `2xl:`)

## API Integration

### API Client Configuration

All API requests go through `src/lib/api-client.ts`:

```typescript
const BASE_URL = process.env.NEXT_PUBLIC_API_URL;
const API_VERSION = process.env.NEXT_PUBLIC_API_VERSION;

// Automatically adds:
// - Base URL
// - API version prefix
// - Auth token from localStorage
// - Content-Type headers
// - Error handling
```

### Available Hooks

#### `useAuth()`
```typescript
const { signin, signup, logout, user, isLoading } = useAuth();

// Usage
await signup({ email, password });
await signin({ email, password });
await logout();
```

#### `useTasks()`
```typescript
const { 
  tasks, 
  isLoading, 
  createTask, 
  updateTask, 
  completeTask, 
  deleteTask 
} = useTasks();

// Usage
createTask.mutate({ title: 'New task' });
updateTask.mutate({ id, title: 'Updated' });
completeTask.mutate(taskId);
deleteTask.mutate(taskId);
```

## Deployment

### Environment Variables (Production)

```bash
# .env.production
NEXT_PUBLIC_API_URL=https://api.your-domain.com
NEXT_PUBLIC_API_VERSION=v1
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_DEBUG=false
```

### Vercel Deployment (Recommended)

```bash
# Install Vercel CLI
pnpm install -g vercel

# Deploy to Vercel
vercel

# Set environment variables in Vercel dashboard
# Settings → Environment Variables → Add:
# - NEXT_PUBLIC_API_URL
# - NEXT_PUBLIC_API_VERSION
# - NEXT_PUBLIC_ENVIRONMENT=production
```

### Docker Deployment

```bash
# Build Docker image
docker build -t todo-frontend .

# Run container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=https://api.example.com \
  -e NEXT_PUBLIC_API_VERSION=v1 \
  todo-frontend
```

### Static Export (Optional)

```bash
# Build static site
pnpm build

# Output in 'out/' directory
# Upload to any static host (Netlify, Cloudflare Pages, etc.)
```

## Performance Optimization

### Current Optimizations

- ✅ React Query for efficient data fetching and caching
- ✅ Optimistic UI updates for instant feedback
- ✅ Turbopack for faster dev builds
- ✅ Automatic code splitting by route
- ✅ Image optimization with Next.js Image component (when used)

### Recommendations for Scale

- Add page-level loading states with Suspense
- Implement virtualized lists for 100+ tasks
- Add service worker for offline support
- Use React.memo() for heavy components
- Add bundle analyzer to monitor size

## Troubleshooting

### Common Issues

**Issue: `API_URL` not defined**
```bash
# Solution: Create .env.local
cp .env.local.example .env.local
# Restart dev server
```

**Issue: CORS errors**
```bash
# Backend must allow frontend origin
# Check backend/.env ALLOWED_ORIGINS includes:
# ["http://localhost:3000"]
```

**Issue: Authentication not persisting**
```bash
# Check localStorage in DevTools
# Application → Local Storage → Should see 'auth_token'
# If missing, token not being saved after signin
```

**Issue: Build fails**
```bash
# Clear cache and rebuild
rm -rf .next
pnpm install
pnpm build
```

**Issue: TypeScript errors**
```bash
# Check types
npx tsc --noEmit

# Update types
pnpm install @types/node @types/react @types/react-dom --save-dev
```

## Browser Support

- **Chrome/Edge**: Latest 2 versions
- **Firefox**: Latest 2 versions
- **Safari**: Latest 2 versions
- **Mobile**: iOS Safari 14+, Chrome Android Latest

## Accessibility

- Keyboard navigation supported
- ARIA labels on interactive elements
- Focus management for modals/dialogs
- Screen reader compatible
- High contrast mode support

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Write components with TypeScript types
3. Add tests for new components
4. Ensure all tests pass: `pnpm test`
5. Check types: `pnpm type-check`
6. Create pull request

## License

MIT License - See LICENSE file for details

## Support

- **Backend API**: `../backend/README.md`
- **Issues**: GitHub Issues
- **Documentation**: Project Wiki (Coming soon)

## Related

- **Backend**: `../backend/README.md`
- **Deployment Guide**: `./docs/deployment.md` (Coming in Phase III)
