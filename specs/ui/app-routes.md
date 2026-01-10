# App Router Routes Specification

## Overview

Next.js 16+ App Router file-system based routing for the Todo application. Routes are organized with authentication protection and proper layouts.

## Route Structure

```
app/
├── layout.tsx              # Root layout (providers, global styles)
├── page.tsx                # Home page (/)
├── loading.tsx             # Global loading UI
├── error.tsx               # Global error boundary
├── not-found.tsx           # 404 page
│
├── tasks/
│   ├── layout.tsx          # Tasks layout (auth guard)
│   ├── page.tsx            # Task list (/tasks)
│   ├── loading.tsx         # Tasks loading skeleton
│   └── actions.ts          # Server Actions for mutations
│
├── auth/
│   ├── layout.tsx          # Auth pages layout
│   ├── signin/
│   │   └── page.tsx        # Sign in (/auth/signin)
│   ├── signup/
│   │   └── page.tsx        # Sign up (/auth/signup)
│   └── signout/
│       └── route.ts        # Sign out handler
│
└── api/
    └── auth/
        └── [...all]/
            └── route.ts    # Better Auth catch-all handler
```

## Route Details

### Public Routes

#### / (Home)

**File:** `app/page.tsx`
**Type:** Server Component
**Auth:** Public

```tsx
// app/page.tsx
import Link from 'next/link';
import { auth } from '@/lib/auth';
import { redirect } from 'next/navigation';

export default async function HomePage() {
  const session = await auth.api.getSession();

  // Redirect authenticated users to tasks
  if (session) {
    redirect('/tasks');
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-4xl font-bold mb-4">Todo App</h1>
      <p className="text-gray-600 mb-8">
        Manage your tasks with ease
      </p>
      <div className="flex gap-4">
        <Link href="/auth/signin" className="btn-primary">
          Sign In
        </Link>
        <Link href="/auth/signup" className="btn-outline">
          Sign Up
        </Link>
      </div>
    </div>
  );
}
```

---

### Authentication Routes

#### /auth/signin

**File:** `app/auth/signin/page.tsx`
**Type:** Server Component with Client Form
**Auth:** Public (redirect if authenticated)

```tsx
// app/auth/signin/page.tsx
import { auth } from '@/lib/auth';
import { redirect } from 'next/navigation';
import { SignInForm } from '@/components/auth/signin-form';

export default async function SignInPage() {
  const session = await auth.api.getSession();

  if (session) {
    redirect('/tasks');
  }

  return (
    <div className="max-w-md mx-auto mt-20">
      <h1 className="text-2xl font-bold mb-6">Sign In</h1>
      <SignInForm />
      <p className="mt-4 text-center text-gray-600">
        Don't have an account?{' '}
        <Link href="/auth/signup" className="text-blue-600">
          Sign up
        </Link>
      </p>
    </div>
  );
}
```

#### /auth/signup

**File:** `app/auth/signup/page.tsx`
**Type:** Server Component with Client Form
**Auth:** Public (redirect if authenticated)

```tsx
// app/auth/signup/page.tsx
import { auth } from '@/lib/auth';
import { redirect } from 'next/navigation';
import { SignUpForm } from '@/components/auth/signup-form';

export default async function SignUpPage() {
  const session = await auth.api.getSession();

  if (session) {
    redirect('/tasks');
  }

  return (
    <div className="max-w-md mx-auto mt-20">
      <h1 className="text-2xl font-bold mb-6">Create Account</h1>
      <SignUpForm />
      <p className="mt-4 text-center text-gray-600">
        Already have an account?{' '}
        <Link href="/auth/signin" className="text-blue-600">
          Sign in
        </Link>
      </p>
    </div>
  );
}
```

#### /api/auth/[...all]

**File:** `app/api/auth/[...all]/route.ts`
**Type:** Route Handler (API)
**Purpose:** Better Auth API endpoints

```tsx
// app/api/auth/[...all]/route.ts
import { auth } from '@/lib/auth';

export const { GET, POST } = auth.handler;
```

---

### Protected Routes

#### /tasks

**File:** `app/tasks/page.tsx`
**Type:** Server Component
**Auth:** Required

```tsx
// app/tasks/page.tsx
import { auth } from '@/lib/auth';
import { redirect } from 'next/navigation';
import { Suspense } from 'react';
import { TaskList } from '@/components/tasks/task-list';
import { TaskForm } from '@/components/tasks/task-form';
import { TaskFilters } from '@/components/tasks/task-filters';
import { TaskListSkeleton } from '@/components/tasks/task-list-skeleton';

interface TasksPageProps {
  searchParams: { status?: string };
}

export default async function TasksPage({ searchParams }: TasksPageProps) {
  const session = await auth.api.getSession();

  if (!session) {
    redirect('/auth/signin');
  }

  const status = searchParams.status || 'all';

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">My Tasks</h1>
        <TaskFilters />
      </div>

      <div className="mb-6">
        <TaskForm />
      </div>

      <Suspense fallback={<TaskListSkeleton />}>
        <TaskListWrapper userId={session.user.id} status={status} />
      </Suspense>
    </div>
  );
}

async function TaskListWrapper({
  userId,
  status
}: {
  userId: string;
  status: string;
}) {
  const tasks = await fetchTasks(userId, status);
  return <TaskList tasks={tasks} />;
}
```

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| status | string | "all" | Filter: "all", "pending", "completed" |

---

### Tasks Layout (Auth Guard)

```tsx
// app/tasks/layout.tsx
import { auth } from '@/lib/auth';
import { redirect } from 'next/navigation';

export default async function TasksLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth.api.getSession();

  if (!session) {
    redirect('/auth/signin');
  }

  return <>{children}</>;
}
```

---

### Server Actions

```tsx
// app/tasks/actions.ts
'use server';

import { auth } from '@/lib/auth';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export async function createTask(formData: FormData) {
  const session = await auth.api.getSession();

  if (!session) {
    redirect('/auth/signin');
  }

  const title = formData.get('title') as string;
  const description = formData.get('description') as string | null;

  await fetch(`${API_URL}/api/${session.user.id}/tasks`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${session.token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title, description }),
  });

  revalidatePath('/tasks');
}

export async function toggleComplete(taskId: number) {
  const session = await auth.api.getSession();

  if (!session) {
    redirect('/auth/signin');
  }

  await fetch(`${API_URL}/api/${session.user.id}/tasks/${taskId}/complete`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${session.token}`,
    },
  });

  revalidatePath('/tasks');
}

export async function deleteTask(taskId: number) {
  const session = await auth.api.getSession();

  if (!session) {
    redirect('/auth/signin');
  }

  await fetch(`${API_URL}/api/${session.user.id}/tasks/${taskId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${session.token}`,
    },
  });

  revalidatePath('/tasks');
}

export async function updateTask(taskId: number, formData: FormData) {
  const session = await auth.api.getSession();

  if (!session) {
    redirect('/auth/signin');
  }

  const title = formData.get('title') as string | null;
  const description = formData.get('description') as string | null;

  await fetch(`${API_URL}/api/${session.user.id}/tasks/${taskId}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${session.token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title, description }),
  });

  revalidatePath('/tasks');
}
```

---

### Root Layout

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google';
import { Header } from '@/components/layout/header';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Todo App',
  description: 'Manage your tasks with ease',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Header />
        <main>{children}</main>
      </body>
    </html>
  );
}
```

---

### Loading States

```tsx
// app/tasks/loading.tsx
import { TaskListSkeleton } from '@/components/tasks/task-list-skeleton';

export default function TasksLoading() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="h-8 w-32 bg-gray-200 rounded mb-6 animate-pulse" />
      <TaskListSkeleton />
    </div>
  );
}
```

---

### Error Handling

```tsx
// app/tasks/error.tsx
'use client';

export default function TasksError({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="container mx-auto px-4 py-8 text-center">
      <h2 className="text-xl font-bold mb-4">Something went wrong!</h2>
      <p className="text-gray-600 mb-4">{error.message}</p>
      <button
        onClick={reset}
        className="px-4 py-2 bg-blue-600 text-white rounded"
      >
        Try again
      </button>
    </div>
  );
}
```

---

## Route Summary

| Path | Auth | Component Type | Description |
|------|------|----------------|-------------|
| `/` | Public | Server | Home/landing page |
| `/tasks` | Required | Server | Task list |
| `/auth/signin` | Public | Server + Client | Sign in form |
| `/auth/signup` | Public | Server + Client | Sign up form |
| `/api/auth/*` | - | Route Handler | Better Auth API |

## Middleware (Optional)

```tsx
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Add custom headers, logging, etc.
  return NextResponse.next();
}

export const config = {
  matcher: ['/tasks/:path*'],
};
```

## Related Specifications

- [UI Components](./components.md)
- [Authentication](../features/003-authentication.md)
- [Task CRUD Feature](../features/002-task-crud-api.md)
