# Quickstart Guide: UI Enhancement with shadcn/ui and Dark Mode

**Feature**: 003-ui-enhancement  
**Date**: 2026-01-15  
**Purpose**: Developer setup and implementation guide

---

## Prerequisites

- **Node.js**: 20.x LTS
- **pnpm**: 10.x (recommended) or npm 9.x
- **Python**: 3.13+ (for backend)
- **uv**: Latest version (for backend dependency management)
- **Git**: For version control

---

## 1. Initial Setup

### Clone and Checkout Feature Branch

```bash
git checkout 003-ui-enhancement
```

The branch should already exist. If not:
```bash
git checkout -b 003-ui-enhancement
```

---

## 2. Infrastructure Cleanup (Phase 0)

### Remove Sentry from Backend

**Step 1**: Remove Sentry dependency
```bash
cd backend
# Edit pyproject.toml and remove sentry-sdk from dependencies
# Then run:
uv sync
```

**Step 2**: Delete Sentry module
```bash
rm -rf backend/src/monitoring/error_tracking.py
```

**Step 3**: Remove Sentry initialization from main.py
```bash
# Edit backend/src/main.py
# Remove the following lines:
# - import sentry_sdk
# - sentry_sdk.init(...)
```

**Step 4**: Remove Sentry config from config.py
```bash
# Edit backend/src/config.py
# Remove:
# - sentry_dsn field
# - sentry_traces_sample_rate field
# - sentry_profiles_sample_rate field
```

**Step 5**: Update environment variable docs
```bash
# Edit backend/.env.example
# Remove SENTRY_DSN line
```

**Verification**:
```bash
cd backend
uv run uvicorn src.main:app --reload
# Should start without Sentry errors
```

### Remove GitHub Actions CI/CD

```bash
# From repository root
rm -rf .github/workflows/ci.yml
```

**Verification**:
```bash
ls .github/workflows/
# Should output: No such file or directory
```

### Run Tests After Cleanup

```bash
# Backend tests
cd backend
uv run pytest tests/
# Should pass: 172/172 tests

# Frontend tests
cd frontend
pnpm test
# Should pass: 73/73 tests
```

---

## 3. Install shadcn/ui (Phase 1)

### Initialize shadcn/ui

```bash
cd frontend
npx shadcn@latest init
```

**Configuration prompts** (select these options):
- TypeScript: `Yes`
- Style: `Default`
- Base color: `Slate` (or your preference)
- CSS variables: `Yes`
- Tailwind config location: `tailwind.config.js`
- Import alias for components: `@/components`
- Import alias for utils: `@/lib`
- React Server Components: `Yes`

**Files created**:
- `components.json` - shadcn/ui configuration
- `lib/utils.ts` - `cn()` utility function
- `components/ui/` - Directory for shadcn/ui components

### Add Required Components

```bash
# Core components
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add input
npx shadcn@latest add label
npx shadcn@latest add form

# Optional (for enhanced features)
npx shadcn@latest add checkbox
npx shadcn@latest add dropdown-menu
npx shadcn@latest add toast
```

### Install Icons Library

```bash
pnpm add lucide-react
```

**Usage**:
```tsx
import { Moon, Sun, CheckCircle, Trash2 } from 'lucide-react';
```

### Verify Installation

```bash
# Check components exist
ls src/components/ui/
# Should show: button.tsx, card.tsx, input.tsx, label.tsx, form.tsx

# Check utils exist
cat src/lib/utils.ts
# Should contain: cn() function

# Run type check
pnpm run type-check
# Should pass without errors
```

---

## 4. Install Dark Mode System (Phase 2)

### Install next-themes

```bash
cd frontend
pnpm add next-themes
```

### Create Theme Provider

**File**: `src/app/providers.tsx`
```tsx
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
```

### Update Root Layout

**File**: `src/app/layout.tsx`
```tsx
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

### Add Dark Mode CSS Variables

**File**: `src/styles/globals.css` (add to end of file)
```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 48%;
  }
}
```

### Update Tailwind Config

**File**: `tailwind.config.js`
```js
module.exports = {
  darkMode: 'class', // Enable class-based dark mode
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
    },
  },
  plugins: [],
};
```

### Create Theme Toggle Component

**File**: `src/components/ThemeToggle.tsx`
```tsx
'use client';

import { useTheme } from 'next-themes';
import { Moon, Sun } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
      aria-label="Toggle theme"
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
    </Button>
  );
}
```

### Add Theme Toggle to Layout

Update `src/app/layout.tsx` or create a navigation component:
```tsx
import { ThemeToggle } from '@/components/ThemeToggle';

// Add to your header/nav component:
<nav className="flex items-center justify-between p-4">
  <h1>Todo App</h1>
  <ThemeToggle />
</nav>
```

### Test Dark Mode

```bash
pnpm dev
# Visit http://localhost:3000
# Click theme toggle button
# Verify page switches between light and dark themes
# Refresh page → theme should persist
```

---

## 5. Development Workflow

### Running the Application

**Backend**:
```bash
cd backend
uv run uvicorn src.main:app --reload
# Runs on http://localhost:8000
```

**Frontend**:
```bash
cd frontend
pnpm dev
# Runs on http://localhost:3000
```

### Running Tests

**Backend**:
```bash
cd backend
uv run pytest tests/               # All tests
uv run pytest tests/unit/          # Unit tests only
uv run pytest tests/integration/   # Integration tests only
uv run ruff check .                # Linting
uv run mypy src                    # Type checking
```

**Frontend**:
```bash
cd frontend
pnpm test                    # All tests
pnpm test -- --watch         # Watch mode
pnpm run lint                # ESLint
pnpm run type-check          # TypeScript
```

### Pre-Commit Checklist

Before committing changes, run:

```bash
# Backend
cd backend && uv run ruff check . && uv run mypy src && uv run pytest
# Frontend
cd frontend && pnpm run lint && pnpm run type-check && pnpm test
```

**Shortcut NPM scripts** (add to `frontend/package.json`):
```json
{
  "scripts": {
    "pre-push": "pnpm run lint && pnpm run type-check && pnpm test",
    "check-all": "pnpm run lint && pnpm run type-check && pnpm test && pnpm run build"
  }
}
```

Then run:
```bash
cd frontend && pnpm run pre-push
```

---

## 6. Component Migration Guide

### Migration Process

**For each component to migrate**:

1. **Backup current component**:
   ```bash
   cp src/components/TaskItem.tsx src/components/TaskItem.backup.tsx
   ```

2. **Install required shadcn/ui components**:
   ```bash
   npx shadcn@latest add card button
   ```

3. **Update component**:
   ```tsx
   // Before
   <div className="border rounded p-4">
     <h3>{task.title}</h3>
     <button onClick={handleComplete}>Complete</button>
   </div>
   
   // After
   import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
   import { Button } from '@/components/ui/button';
   
   <Card>
     <CardHeader>
       <CardTitle>{task.title}</CardTitle>
     </CardHeader>
     <CardContent>
       <Button onClick={handleComplete}>Complete</Button>
     </CardContent>
   </Card>
   ```

4. **Run tests**:
   ```bash
   pnpm test -- TaskItem.test.tsx
   ```

5. **Visual verification**:
   - Start dev server: `pnpm dev`
   - Navigate to page with component
   - Verify styling matches or improves on original
   - Test dark mode appearance

6. **Cleanup**:
   ```bash
   rm src/components/TaskItem.backup.tsx
   ```

---

## 7. Adding New shadcn/ui Components

### Browse Available Components

Visit: https://ui.shadcn.com/docs/components

### Add Component

```bash
npx shadcn@latest add <component-name>
```

Examples:
```bash
npx shadcn@latest add alert
npx shadcn@latest add dialog
npx shadcn@latest add select
npx shadcn@latest add tabs
```

### Verify Installation

```bash
# Check component was added
ls src/components/ui/<component-name>.tsx

# Check imports work
pnpm run type-check
```

---

## 8. Troubleshooting

### Issue: Theme flickers on page load

**Cause**: SSR mismatch  
**Solution**: Ensure `suppressHydrationWarning` is on `<html>` element in `layout.tsx`

```tsx
<html lang="en" suppressHydrationWarning>
```

### Issue: localStorage errors in console

**Cause**: Accessing localStorage during SSR  
**Solution**: Ensure `next-themes` is used, not manual localStorage access

### Issue: Dark mode colors not applying

**Cause**: CSS variables not defined  
**Solution**: 
1. Verify `globals.css` has `:root` and `.dark` CSS variables
2. Verify `tailwind.config.js` has `darkMode: 'class'`
3. Check browser DevTools → `<html>` element has `class="dark"`

### Issue: shadcn/ui components not found

**Cause**: Import alias not configured  
**Solution**: Check `tsconfig.json` has:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### Issue: Tests failing after component migration

**Cause**: Test selectors changed (e.g., `getByText` vs `getByRole`)  
**Solution**: Update test queries to match new component structure:
```tsx
// Before
getByText('Complete')

// After
getByRole('button', { name: 'Complete' })
```

---

## 9. Performance Checks

### Measure Theme Toggle Performance

```tsx
// Add to ThemeToggle.tsx for testing
const handleToggle = () => {
  const start = performance.now();
  setTheme(theme === 'light' ? 'dark' : 'light');
  const end = performance.now();
  console.log(`Theme toggle took ${end - start}ms`);
  // Target: <200ms (per SC-002)
};
```

### Run Lighthouse Audit

```bash
# Start production build
cd frontend
pnpm build
pnpm start
# Open http://localhost:3000 in Chrome
# DevTools → Lighthouse → Run audit
# Target: Accessibility 90+, Performance 85+
```

---

## 10. Documentation Updates

### Update README.md

Add to "Features" section:
- Dark mode with theme persistence
- Modern UI with shadcn/ui components
- Enhanced landing page

Remove from "Infrastructure" section:
- Sentry error tracking
- GitHub Actions CI/CD

### Update Deployment Guide

Remove Sentry-related environment variables:
- `SENTRY_DSN`

Add note about manual testing workflow:
- Developers must run tests locally before pushing
- Optional: Set up Git pre-commit hooks

---

## Quick Reference

### Key Files

| File | Purpose |
|------|---------|
| `frontend/components.json` | shadcn/ui configuration |
| `frontend/src/lib/utils.ts` | `cn()` utility function |
| `frontend/src/app/providers.tsx` | Theme provider setup |
| `frontend/src/components/ThemeToggle.tsx` | Dark mode toggle button |
| `frontend/src/styles/globals.css` | Dark mode CSS variables |
| `frontend/tailwind.config.js` | Tailwind + theme config |

### Useful Commands

```bash
# Add shadcn/ui component
npx shadcn@latest add <component>

# Check what components are available
npx shadcn@latest list

# Run all checks (frontend)
pnpm run pre-push

# Run all checks (backend)
cd backend && uv run ruff check . && uv run mypy src && uv run pytest

# Start dev servers
cd backend && uv run uvicorn src.main:app --reload &
cd frontend && pnpm dev
```

---

## Next Steps

After completing this setup:

1. ✅ **Verify infrastructure cleanup**: No Sentry errors, no GitHub Actions
2. ✅ **Verify shadcn/ui installation**: Components render correctly
3. ✅ **Verify dark mode**: Theme toggles and persists
4. 🔄 **Begin component migration**: Follow Phase 4 tasks
5. 🔄 **Enhance landing page**: Follow Phase 3 tasks
6. 🔄 **Run full test suite**: Ensure all tests pass
7. 🔄 **Lighthouse audit**: Meet accessibility and performance targets

See `tasks.md` (generated by `/sp.tasks` command) for detailed task breakdown.
