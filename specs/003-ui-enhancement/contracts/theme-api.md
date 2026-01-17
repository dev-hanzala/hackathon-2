# API Contracts: Theme System

**Feature**: 003-ui-enhancement  
**Date**: 2026-01-15  
**Purpose**: Define component interfaces for theme system and shadcn/ui integration

---

## 1. Theme Provider Contract

**Component**: `<ThemeProvider>`  
**Location**: `frontend/src/app/providers.tsx`  
**Type**: Client Component

### Props

```typescript
interface ThemeProviderProps {
  children: React.ReactNode;
  defaultTheme?: 'light' | 'dark' | 'system';
  storageKey?: string;
  attribute?: 'class' | 'data-theme';
  enableSystem?: boolean;
}
```

### Prop Descriptions

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | Required | React children to wrap with theme context |
| `defaultTheme` | `'light' \| 'dark' \| 'system'` | `'light'` | Default theme when no preference stored |
| `storageKey` | `string` | `'theme'` | localStorage key for storing preference |
| `attribute` | `'class' \| 'data-theme'` | `'class'` | HTML attribute to set for theme (`<html class="dark">`) |
| `enableSystem` | `boolean` | `false` | Whether to detect system preference (disabled per spec) |

### Context Values

```typescript
interface ThemeContextValue {
  theme: 'light' | 'dark' | 'system';
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
  systemTheme?: 'light' | 'dark';
  resolvedTheme?: 'light' | 'dark';
}
```

### Context Value Descriptions

| Value | Type | Description |
|-------|------|-------------|
| `theme` | `'light' \| 'dark' \| 'system'` | Current theme setting (what user selected) |
| `setTheme` | `(theme) => void` | Function to update theme preference |
| `systemTheme` | `'light' \| 'dark'` | Detected system preference (if `enableSystem: true`) |
| `resolvedTheme` | `'light' \| 'dark'` | Actual theme being applied (never `'system'`) |

### Usage Example

```tsx
// app/providers.tsx
'use client';
import { ThemeProvider as NextThemesProvider } from 'next-themes';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme="light"
      enableSystem={false}
      storageKey="theme"
    >
      {children}
    </NextThemesProvider>
  );
}

// app/layout.tsx
import { Providers } from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

### Behavior Specifications

1. **Initialization**: Reads from localStorage on mount (client-side only)
2. **Storage**: Writes to localStorage immediately when `setTheme()` is called
3. **SSR Safety**: Uses `suppressHydrationWarning` to prevent hydration mismatch
4. **Class Application**: Adds/removes `dark` class on `<html>` element
5. **Storage Events**: Syncs theme across browser tabs automatically

### Error Handling

- If localStorage is blocked → falls back to default theme (no persistence)
- If stored value is invalid → uses default theme
- If `setTheme()` called with invalid value → throws TypeScript error (compile-time)

---

## 2. Theme Toggle Contract

**Component**: `<ThemeToggle>`  
**Location**: `frontend/src/components/ThemeToggle.tsx`  
**Type**: Client Component

### Props

```typescript
interface ThemeToggleProps {
  className?: string;
}
```

### Prop Descriptions

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `className` | `string` | `undefined` | Additional CSS classes for styling |

### Component Structure

```tsx
'use client';
import { useTheme } from 'next-themes';
import { Moon, Sun } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function ThemeToggle({ className }: ThemeToggleProps) {
  const { theme, setTheme } = useTheme();
  
  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
      aria-label="Toggle theme"
      className={className}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
    </Button>
  );
}
```

### Behavior Specifications

1. **Click Handler**: Toggles between 'light' and 'dark' (no 'system' option)
2. **Icon Display**: Shows Sun in light mode, Moon in dark mode
3. **Transition**: Smooth icon rotation/scale animation (~300ms)
4. **Accessibility**: Includes `aria-label` for screen readers
5. **Response Time**: Theme changes apply in <200ms (per SC-002)

### States

| State | Icon | Action | Result |
|-------|------|--------|--------|
| Light Mode | Sun visible | Click → `setTheme('dark')` | Switch to dark mode |
| Dark Mode | Moon visible | Click → `setTheme('light')` | Switch to light mode |

### Accessibility

- **Keyboard**: Focusable and activatable with Enter/Space
- **Screen Reader**: Announces "Toggle theme" button
- **Focus Visible**: Shows focus ring when navigated via keyboard
- **ARIA**: Uses `aria-label` for context

---

## 3. shadcn/ui Component Contracts

**Component Library**: shadcn/ui (based on Radix UI primitives)  
**Documentation**: https://ui.shadcn.com/docs/components

### 3.1 Button Component

**Location**: `frontend/src/components/ui/button.tsx`  
**Source**: Added via `npx shadcn@latest add button`

```typescript
interface ButtonProps {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
  size?: 'default' | 'sm' | 'lg' | 'icon';
  asChild?: boolean;
  disabled?: boolean;
  className?: string;
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  children: React.ReactNode;
}
```

**Variants**:
- `default`: Primary blue button
- `destructive`: Red button for delete/error actions
- `outline`: Bordered button with transparent background
- `secondary`: Subtle gray button
- `ghost`: Transparent button (only visible on hover)
- `link`: Button styled as hyperlink

**Sizes**:
- `default`: Standard height (h-10, px-4 py-2)
- `sm`: Small height (h-9, px-3)
- `lg`: Large height (h-11, px-8)
- `icon`: Square button for icon-only (h-10 w-10)

**Usage Example**:
```tsx
<Button variant="default" size="default">Save</Button>
<Button variant="destructive" size="sm">Delete</Button>
<Button variant="ghost" size="icon">
  <Settings className="h-4 w-4" />
</Button>
```

---

### 3.2 Card Component

**Location**: `frontend/src/components/ui/card.tsx`  
**Source**: Added via `npx shadcn@latest add card`

```typescript
// Main Card wrapper
interface CardProps {
  className?: string;
  children: React.ReactNode;
}

// Card sections
interface CardHeaderProps { className?: string; children: React.ReactNode; }
interface CardTitleProps { className?: string; children: React.ReactNode; }
interface CardDescriptionProps { className?: string; children: React.ReactNode; }
interface CardContentProps { className?: string; children: React.ReactNode; }
interface CardFooterProps { className?: string; children: React.ReactNode; }
```

**Structure**:
```tsx
<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Optional description</CardDescription>
  </CardHeader>
  <CardContent>
    Main content goes here
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

**Styling**: Automatically themed via CSS variables (background, border, foreground)

---

### 3.3 Input Component

**Location**: `frontend/src/components/ui/input.tsx`  
**Source**: Added via `npx shadcn@latest add input`

```typescript
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  className?: string;
  type?: string;
  placeholder?: string;
  disabled?: boolean;
  // ... all standard HTML input attributes
}
```

**Usage Example**:
```tsx
<div className="space-y-2">
  <Label htmlFor="email">Email</Label>
  <Input
    id="email"
    type="email"
    placeholder="you@example.com"
    required
  />
</div>
```

**States**:
- Normal: Border color via `--input`
- Focus: Ring color via `--ring`, border-primary
- Error: Border-destructive (apply via className)
- Disabled: Opacity-50, cursor-not-allowed

---

### 3.4 Form Component

**Location**: `frontend/src/components/ui/form.tsx`  
**Source**: Added via `npx shadcn@latest add form`

**Integration**: Uses `react-hook-form` for validation

```typescript
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

const formSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

function SignInForm() {
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: { email: '', password: '' },
  });
  
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="you@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Sign In</Button>
      </form>
    </Form>
  );
}
```

**Components**:
- `<Form>`: Wrapper providing form context
- `<FormField>`: Individual field wrapper
- `<FormItem>`: Spacing and layout for field
- `<FormLabel>`: Accessible label for input
- `<FormControl>`: Wrapper for input component
- `<FormMessage>`: Displays validation errors

---

## 4. Component Migration Contract

### Migration Checklist per Component

For each component being migrated to shadcn/ui:

**Before Migration**:
1. Document current props and behaviors
2. Identify which shadcn/ui components to use
3. Map current props to shadcn/ui equivalents
4. Review existing tests

**During Migration**:
1. Install required shadcn/ui components
2. Update component implementation
3. Maintain existing prop interface (if possible)
4. Update tests to match new structure

**After Migration**:
1. Run existing tests (must pass)
2. Visual comparison (screenshot before/after)
3. Accessibility check (keyboard navigation, ARIA)
4. Performance check (no regression)

### Example Migration: TaskItem Component

**Before** (custom components):
```tsx
// Old implementation
export function TaskItem({ task, onComplete, onDelete }) {
  return (
    <div className="border rounded p-4">
      <h3 className="font-bold">{task.title}</h3>
      <div className="flex gap-2 mt-2">
        <button onClick={() => onComplete(task.id)}>Complete</button>
        <button onClick={() => onDelete(task.id)}>Delete</button>
      </div>
    </div>
  );
}
```

**After** (shadcn/ui components):
```tsx
// New implementation
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CheckCircle, Trash2 } from 'lucide-react';

export function TaskItem({ task, onComplete, onDelete }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{task.title}</CardTitle>
      </CardHeader>
      <CardFooter className="flex gap-2">
        <Button
          variant="default"
          size="sm"
          onClick={() => onComplete(task.id)}
        >
          <CheckCircle className="h-4 w-4 mr-2" />
          Complete
        </Button>
        <Button
          variant="destructive"
          size="sm"
          onClick={() => onDelete(task.id)}
        >
          <Trash2 className="h-4 w-4 mr-2" />
          Delete
        </Button>
      </CardFooter>
    </Card>
  );
}
```

**Contract Maintained**:
- ✅ Props unchanged (`task`, `onComplete`, `onDelete`)
- ✅ Behavior unchanged (same click handlers)
- ✅ Tests require minimal updates (selector changes only)
- ✅ Visual improvement (better spacing, hover states, icons)

---

## 5. Testing Contracts

### Theme System Tests

**Unit Tests** (`tests/__tests__/ThemeProvider.test.tsx`):
```typescript
describe('ThemeProvider', () => {
  it('defaults to light theme when no preference stored', () => {
    render(<ThemeProvider><TestComponent /></ThemeProvider>);
    expect(getTheme()).toBe('light');
  });
  
  it('reads theme from localStorage on mount', () => {
    localStorage.setItem('theme', 'dark');
    render(<ThemeProvider><TestComponent /></ThemeProvider>);
    expect(getTheme()).toBe('dark');
  });
  
  it('persists theme to localStorage on change', () => {
    const { getByRole } = render(<ThemeProvider><ThemeToggle /></ThemeProvider>);
    fireEvent.click(getByRole('button'));
    expect(localStorage.getItem('theme')).toBe('dark');
  });
});
```

**Integration Tests** (`tests/__tests__/ThemeToggle.test.tsx`):
```typescript
describe('ThemeToggle', () => {
  it('toggles theme on click', () => {
    const { getByRole } = render(<ThemeToggle />);
    const button = getByRole('button');
    
    fireEvent.click(button);
    expect(document.documentElement.classList.contains('dark')).toBe(true);
    
    fireEvent.click(button);
    expect(document.documentElement.classList.contains('dark')).toBe(false);
  });
  
  it('applies theme change in under 200ms', async () => {
    const { getByRole } = render(<ThemeToggle />);
    const start = performance.now();
    
    fireEvent.click(getByRole('button'));
    await waitFor(() => {
      expect(document.documentElement.classList.contains('dark')).toBe(true);
    });
    
    const duration = performance.now() - start;
    expect(duration).toBeLessThan(200);
  });
});
```

---

## Summary

This contract defines:
1. **ThemeProvider**: Context provider for theme state
2. **ThemeToggle**: UI control for switching themes
3. **shadcn/ui Components**: Button, Card, Input, Form interfaces
4. **Migration Contract**: Process for updating existing components
5. **Testing Contract**: Required tests for theme functionality

All contracts follow TypeScript best practices and ensure type safety. Components are designed to be composable, accessible, and performant.
