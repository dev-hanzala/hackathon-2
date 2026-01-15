# UI Components Specification

## Overview

React components for the Next.js 16+ frontend using App Router patterns. Components are organized by Server Components (default) and Client Components (for interactivity).

## Component Architecture

### Server vs Client Components

| Type | Use Case | Directive |
|------|----------|-----------|
| Server Component | Data fetching, static content | None (default) |
| Client Component | Interactivity, state, effects | `'use client'` |

### Component Directory Structure

```
frontend/
├── app/                    # App Router pages
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page
│   ├── tasks/
│   │   ├── page.tsx        # Tasks list page
│   │   └── actions.ts      # Server Actions
│   └── auth/
│       ├── signin/page.tsx
│       └── signup/page.tsx
├── components/
│   ├── ui/                 # Base UI components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   └── checkbox.tsx
│   ├── tasks/              # Task-specific components
│   │   ├── task-list.tsx
│   │   ├── task-item.tsx
│   │   ├── task-form.tsx
│   │   └── task-filters.tsx
│   ├── auth/               # Auth components
│   │   ├── signin-form.tsx
│   │   ├── signup-form.tsx
│   │   └── user-menu.tsx
│   └── layout/             # Layout components
│       ├── header.tsx
│       ├── footer.tsx
│       └── nav.tsx
└── lib/
    ├── api.ts              # API client
    └── auth.ts             # Better Auth config
```

## Core Components

### Layout Components

#### Header

```tsx
// components/layout/header.tsx
import { UserMenu } from '@/components/auth/user-menu';
import { Nav } from './nav';

export function Header() {
  return (
    <header className="border-b">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center gap-6">
          <Link href="/" className="font-bold text-xl">
            Todo App
          </Link>
          <Nav />
        </div>
        <UserMenu />
      </div>
    </header>
  );
}
```

**Props:** None
**Type:** Server Component
**Dependencies:** UserMenu, Nav

#### Nav

```tsx
// components/layout/nav.tsx
import Link from 'next/link';

export function Nav() {
  return (
    <nav>
      <Link href="/tasks" className="hover:underline">
        Tasks
      </Link>
    </nav>
  );
}
```

**Props:** None
**Type:** Server Component

---

### Task Components

#### TaskList

```tsx
// components/tasks/task-list.tsx
import { TaskItem } from './task-item';
import type { Task } from '@/lib/types';

interface TaskListProps {
  tasks: Task[];
}

export function TaskList({ tasks }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        No tasks yet. Create one to get started!
      </div>
    );
  }

  return (
    <ul className="space-y-3">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} />
      ))}
    </ul>
  );
}
```

**Props:**
| Prop | Type | Required | Description |
|------|------|----------|-------------|
| tasks | Task[] | Yes | Array of task objects |

**Type:** Server Component
**Children:** TaskItem

#### TaskItem

```tsx
// components/tasks/task-item.tsx
'use client';

import { useState } from 'react';
import { toggleComplete, deleteTask } from '@/app/tasks/actions';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';

interface TaskItemProps {
  task: Task;
}

export function TaskItem({ task }: TaskItemProps) {
  const [isPending, setIsPending] = useState(false);

  async function handleToggle() {
    setIsPending(true);
    await toggleComplete(task.id);
    setIsPending(false);
  }

  async function handleDelete() {
    if (confirm('Delete this task?')) {
      await deleteTask(task.id);
    }
  }

  return (
    <li className={`
      flex items-center gap-3 p-4 border rounded-lg
      ${task.completed ? 'bg-gray-50' : 'bg-white'}
    `}>
      <Checkbox
        checked={task.completed}
        onCheckedChange={handleToggle}
        disabled={isPending}
      />
      <div className="flex-1">
        <h3 className={task.completed ? 'line-through text-gray-500' : ''}>
          {task.title}
        </h3>
        {task.description && (
          <p className="text-sm text-gray-500">{task.description}</p>
        )}
      </div>
      <Button
        variant="ghost"
        size="sm"
        onClick={handleDelete}
      >
        Delete
      </Button>
    </li>
  );
}
```

**Props:**
| Prop | Type | Required | Description |
|------|------|----------|-------------|
| task | Task | Yes | Task object to display |

**Type:** Client Component (interactivity)
**State:** isPending (optimistic UI)

#### TaskForm

```tsx
// components/tasks/task-form.tsx
'use client';

import { useRef } from 'react';
import { createTask } from '@/app/tasks/actions';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export function TaskForm() {
  const formRef = useRef<HTMLFormElement>(null);

  async function handleSubmit(formData: FormData) {
    await createTask(formData);
    formRef.current?.reset();
  }

  return (
    <form ref={formRef} action={handleSubmit} className="flex gap-3">
      <Input
        name="title"
        placeholder="What needs to be done?"
        required
        maxLength={200}
        className="flex-1"
      />
      <Button type="submit">Add Task</Button>
    </form>
  );
}
```

**Props:** None
**Type:** Client Component (form interactivity)
**Server Action:** createTask

#### TaskFilters

```tsx
// components/tasks/task-filters.tsx
'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { Button } from '@/components/ui/button';

const filters = [
  { value: 'all', label: 'All' },
  { value: 'pending', label: 'Pending' },
  { value: 'completed', label: 'Completed' },
];

export function TaskFilters() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const current = searchParams.get('status') || 'all';

  function setFilter(status: string) {
    const params = new URLSearchParams(searchParams);
    if (status === 'all') {
      params.delete('status');
    } else {
      params.set('status', status);
    }
    router.push(`/tasks?${params.toString()}`);
  }

  return (
    <div className="flex gap-2">
      {filters.map((filter) => (
        <Button
          key={filter.value}
          variant={current === filter.value ? 'default' : 'outline'}
          size="sm"
          onClick={() => setFilter(filter.value)}
        >
          {filter.label}
        </Button>
      ))}
    </div>
  );
}
```

**Props:** None
**Type:** Client Component (URL manipulation)

---

### Auth Components

#### SignInForm

```tsx
// components/auth/signin-form.tsx
'use client';

import { useState } from 'react';
import { signIn } from '@/lib/auth-client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export function SignInForm() {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const formData = new FormData(e.currentTarget);

    const result = await signIn.email({
      email: formData.get('email') as string,
      password: formData.get('password') as string,
    });

    if (result.error) {
      setError(result.error.message);
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="p-3 bg-red-50 text-red-700 rounded">
          {error}
        </div>
      )}
      <div>
        <Input
          name="email"
          type="email"
          placeholder="Email"
          required
        />
      </div>
      <div>
        <Input
          name="password"
          type="password"
          placeholder="Password"
          required
          minLength={8}
        />
      </div>
      <Button type="submit" className="w-full" disabled={loading}>
        {loading ? 'Signing in...' : 'Sign In'}
      </Button>
    </form>
  );
}
```

**Props:** None
**Type:** Client Component
**State:** error, loading

#### UserMenu

```tsx
// components/auth/user-menu.tsx
import { auth } from '@/lib/auth';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

export async function UserMenu() {
  const session = await auth.api.getSession();

  if (!session) {
    return (
      <div className="flex gap-2">
        <Link href="/auth/signin">
          <Button variant="outline" size="sm">Sign In</Button>
        </Link>
        <Link href="/auth/signup">
          <Button size="sm">Sign Up</Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-3">
      <span className="text-sm">{session.user.name || session.user.email}</span>
      <form action={signOut}>
        <Button variant="outline" size="sm" type="submit">
          Sign Out
        </Button>
      </form>
    </div>
  );
}
```

**Props:** None
**Type:** Server Component (session check)

---

### Base UI Components

#### Button

```tsx
// components/ui/button.tsx
import { cn } from '@/lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
}

export function Button({
  variant = 'default',
  size = 'md',
  className,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        'rounded font-medium transition-colors',
        {
          'bg-blue-600 text-white hover:bg-blue-700': variant === 'default',
          'border border-gray-300 hover:bg-gray-50': variant === 'outline',
          'hover:bg-gray-100': variant === 'ghost',
          'px-2 py-1 text-sm': size === 'sm',
          'px-4 py-2': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
        },
        className
      )}
      {...props}
    />
  );
}
```

#### Input

```tsx
// components/ui/input.tsx
import { cn } from '@/lib/utils';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export function Input({ className, ...props }: InputProps) {
  return (
    <input
      className={cn(
        'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500',
        className
      )}
      {...props}
    />
  );
}
```

#### Checkbox

```tsx
// components/ui/checkbox.tsx
'use client';

interface CheckboxProps {
  checked: boolean;
  onCheckedChange: () => void;
  disabled?: boolean;
}

export function Checkbox({ checked, onCheckedChange, disabled }: CheckboxProps) {
  return (
    <input
      type="checkbox"
      checked={checked}
      onChange={onCheckedChange}
      disabled={disabled}
      className="w-5 h-5 rounded border-gray-300 cursor-pointer"
    />
  );
}
```

## Styling

- **Framework:** Tailwind CSS
- **Approach:** Utility-first CSS classes
- **Theme:** Light mode (dark mode optional)
- **Responsive:** Mobile-first breakpoints

## Accessibility

| Requirement | Implementation |
|-------------|----------------|
| Keyboard nav | All interactive elements focusable |
| Screen readers | Proper labels and ARIA attributes |
| Color contrast | WCAG AA compliance |
| Focus indicators | Visible focus rings |

## Related Specifications

- [App Routes](./app-routes.md)
- [Task CRUD Feature](../features/002-task-crud-api.md)
- [Authentication](../features/003-authentication.md)
