# Research: UI Enhancement with shadcn/ui and Infrastructure Cleanup

**Feature**: 003-ui-enhancement  
**Date**: 2026-01-15  
**Purpose**: Resolve technical unknowns and establish best practices for implementation

## Research Questions & Findings

### 1. shadcn/ui Installation with Next.js 16

**Question**: What is the recommended setup process for shadcn/ui with Next.js 16?

**Findings**:

**Installation Steps**:
```bash
# Install shadcn/ui CLI
npx shadcn@latest init

# Configuration prompts (recommended answers):
# - TypeScript: Yes
# - Style: Default
# - Base color: Slate
# - CSS variables: Yes
# - Tailwind config: Yes (tailwind.config.js)
# - Import alias: @/components
# - React Server Components: Yes
```

**Required Dependencies** (auto-installed by CLI):
- `tailwindcss-animate`: For component animations
- `class-variance-authority`: For component variants
- `clsx`: For conditional classes
- `tailwind-merge`: For merging Tailwind classes

**Configuration Files Created**:
- `components.json`: shadcn/ui configuration
- `lib/utils.ts`: `cn()` utility function for class merging
- `components/ui/`: Directory for shadcn/ui components

**Adding Components**:
```bash
# Add specific components as needed
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add input
npx shadcn@latest add form
npx shadcn@latest add label
npx shadcn@latest add checkbox
```

**Decision**: Use official CLI for setup. Components are copied into project (not installed as npm package), allowing full customization.

---

### 2. Dark Mode Implementation with Tailwind CSS and Next.js App Router

**Question**: What are best practices for implementing dark mode with Tailwind CSS and Next.js 13+ app router?

**Findings**:

**Recommended Library**: `next-themes` by pacocoursey
- Avoids theme flicker on page load
- SSR-safe (syncs theme before hydration)
- Works with Next.js app router
- Stores preference in localStorage automatically
- Provides `<ThemeProvider>` and `useTheme()` hook

**Installation**:
```bash
npm install next-themes
```

**Implementation Pattern**:

```tsx
// app/providers.tsx (client component)
'use client';
import { ThemeProvider } from 'next-themes';

export function Providers({ children }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false}>
      {children}
    </ThemeProvider>
  );
}

// app/layout.tsx (server component)
import { Providers } from './providers';

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

// components/ThemeToggle.tsx (client component)
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
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
    </Button>
  );
}
```

**Tailwind Configuration**:
```js
// tailwind.config.js
module.exports = {
  darkMode: 'class', // Use class-based dark mode
  // ... rest of config
};
```

**CSS Variables Approach**:
```css
/* globals.css */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    /* ... more variables */
  }
  
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    /* ... more variables */
  }
}
```

**Decision**: Use `next-themes` library with class-based dark mode and CSS variables. This approach is SSR-safe and integrates perfectly with shadcn/ui (which uses the same pattern).

---

### 3. Component Migration Strategy

**Question**: What is the systematic approach to migrating existing custom components to shadcn/ui?

**Findings**:

**Migration Order** (by priority and dependencies):
1. **Base UI components** (Button, Input, Label) - used by all others
2. **Form components** (Form wrapper, validation display)
3. **Layout components** (Card, Container)
4. **Page-specific components** (TaskItem, TaskForm, TaskList)
5. **Auth components** (SignIn, SignUp forms)

**Migration Process per Component**:
1. **Identify**: List all props and behaviors of current component
2. **Install**: Add corresponding shadcn/ui component(s)
3. **Map**: Document prop equivalence (current → shadcn/ui)
4. **Replace**: Update component JSX to use shadcn/ui
5. **Test**: Run existing tests and visual comparison
6. **Iterate**: Fix any broken tests or styling issues

**Example Mapping**:

| Current Component | shadcn/ui Component | Notes |
|-------------------|---------------------|-------|
| Custom Button | `<Button>` | Use variant prop: default, destructive, outline, ghost |
| Custom Input | `<Input>` | Wrap with `<Label>` for accessibility |
| Custom Card | `<Card>`, `<CardHeader>`, `<CardContent>` | More structured than current div-based approach |
| Custom Form | `<Form>` + react-hook-form | More robust validation |

**Testing Strategy**:
- Keep old component alongside new one temporarily
- Use feature flags or separate pages for testing
- Run full test suite after each migration
- Take before/after screenshots for visual regression
- Test keyboard navigation and screen readers

**Rollback Plan**:
- Keep old components in `components/legacy/` directory
- If issues found, revert imports to legacy components
- Delete legacy components only after all tests pass

**Decision**: Migrate incrementally, starting with base components. Test thoroughly before moving to next component. Use shadcn/ui components as-is (minimal customization) to maintain consistency.

---

### 4. localStorage Best Practices with SSR

**Question**: How should theme preferences be stored, retrieved, and synced with SSR in Next.js?

**Findings**:

**Challenge**: localStorage is not available during SSR (server-side rendering). Reading from it directly causes hydration mismatches.

**Solution**: `next-themes` library handles this automatically by:
1. Rendering neutral state on server (no theme applied)
2. Reading from localStorage on client mount
3. Applying theme before first paint (no flicker)
4. Using `suppressHydrationWarning` on `<html>` element

**Alternative Manual Implementation** (if not using next-themes):
```tsx
// Not recommended - use next-themes instead
import { useEffect, useState } from 'react';

export function useLocalStorage(key, defaultValue) {
  const [value, setValue] = useState(defaultValue);
  const [isClient, setIsClient] = useState(false);
  
  useEffect(() => {
    setIsClient(true);
    const stored = localStorage.getItem(key);
    if (stored) setValue(JSON.parse(stored));
  }, [key]);
  
  useEffect(() => {
    if (isClient) {
      localStorage.setItem(key, JSON.stringify(value));
    }
  }, [key, value, isClient]);
  
  return [value, setValue];
}
```

**Edge Cases Handled by next-themes**:
- localStorage disabled/blocked: Falls back to default theme
- Invalid stored value: Uses default theme
- System preference changes: Can optionally sync (disabled in our case)
- Multiple tabs: Syncs via storage events

**Decision**: Use `next-themes` library to handle all localStorage complexity. It's battle-tested and handles SSR correctly out of the box.

---

### 5. Error Logging Strategy Post-Sentry Removal

**Question**: What logging/error handling should replace Sentry for basic error visibility?

**Findings**:

**Current Error Handling in FastAPI**:
- Built-in exception handlers for HTTP errors
- Automatic logging to stdout/stderr
- Development mode shows detailed tracebacks

**Recommended Approach for Hackathon/Prototype**:
1. **Backend**: Use Python's built-in `logging` module
   ```python
   import logging
   
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )
   logger = logging.getLogger(__name__)
   
   # In route handlers
   try:
       result = await some_operation()
   except Exception as e:
       logger.error(f"Operation failed: {e}", exc_info=True)
       raise
   ```

2. **Frontend**: Use console.error and window.onerror
   ```tsx
   // app/error.tsx (Next.js error boundary)
   'use client';
   
   export default function Error({ error, reset }) {
     console.error('Application error:', error);
     
     return (
       <div>
         <h2>Something went wrong!</h2>
         <button onClick={reset}>Try again</button>
       </div>
     );
   }
   ```

**Production Considerations** (future enhancements):
- Structured logging to file for later analysis
- Simple log aggregation with `lnav` or `grep`
- Docker logs accessible via `docker-compose logs`
- Consider open-source alternatives later: Sentry self-hosted, Glitchtip

**Decision**: Remove Sentry entirely. Use Python logging module for backend and console.error for frontend. This is sufficient for prototype/development phase. Document this decision in ADR.

---

### 6. Developer Workflow Without CI/CD

**Question**: What should developers do for testing and quality checks without CI/CD?

**Findings**:

**Recommended Pre-Commit Workflow**:

1. **Manual checklist** (document in README):
   ```markdown
   Before committing:
   - [ ] Run backend tests: `cd backend && uv run pytest`
   - [ ] Run frontend tests: `cd frontend && pnpm test`
   - [ ] Run backend linting: `cd backend && uv run ruff check .`
   - [ ] Run backend type check: `cd backend && uv run mypy src`
   - [ ] Run frontend linting: `cd frontend && pnpm run lint`
   - [ ] Run frontend type check: `cd frontend && pnpm run type-check`
   ```

2. **NPM scripts** to simplify:
   ```json
   // frontend/package.json
   {
     "scripts": {
       "pre-push": "pnpm run lint && pnpm run type-check && pnpm test",
       "check-all": "pnpm run lint && pnpm run type-check && pnpm test && pnpm run build"
     }
   }
   ```
   
   ```bash
   # backend: add to pyproject.toml or create Makefile
   check-all:
       uv run ruff check .
       uv run mypy src
       uv run pytest
   ```

3. **Git hooks** (optional, but recommended):
   ```bash
   # .git/hooks/pre-commit (make executable: chmod +x)
   #!/bin/bash
   echo "Running pre-commit checks..."
   
   cd frontend
   pnpm run lint || exit 1
   pnpm run type-check || exit 1
   pnpm test || exit 1
   
   cd ../backend
   uv run ruff check . || exit 1
   uv run mypy src || exit 1
   uv run pytest || exit 1
   
   echo "✅ All checks passed!"
   ```

**Trade-offs**:
- Pro: Simple, no external dependencies
- Con: Requires developer discipline
- Mitigation: Git hooks automate checks

**Decision**: Document manual testing workflow in README. Recommend Git pre-commit hooks (optional). Create `npm run pre-push` and backend `make check-all` shortcuts.

---

## Summary of Decisions

| Decision | Choice | Rationale | ADR Required? |
|----------|--------|-----------|---------------|
| Component Library | shadcn/ui | Full customization, Tailwind integration, copy-paste architecture | YES |
| Dark Mode Library | next-themes | SSR-safe, handles localStorage, battle-tested | NO |
| Theme Storage | localStorage (client-side only) | Simple, fast, no backend changes | NO |
| Sentry Replacement | Python logging + console.error | Sufficient for prototype, reduces complexity | YES |
| CI/CD Alternative | Manual pre-commit checklist + optional Git hooks | Simple, no external services | NO |
| Component Migration | Incremental, base components first | Lower risk, testable in isolation | NO |

---

## Implementation Priorities

Based on research findings, the recommended implementation order is:

1. **Phase 0**: Infrastructure cleanup (remove Sentry, GitHub Actions)
2. **Phase 1**: shadcn/ui setup (install CLI, add base components)
3. **Phase 2**: Theme system (install next-themes, create ThemeProvider and ThemeToggle)
4. **Phase 3**: Landing page enhancement (improve content, apply shadcn/ui components)
5. **Phase 4**: Component migration (replace existing components with shadcn/ui equivalents)
6. **Phase 5**: Testing and polish (verify all functionality, run Lighthouse audits)

---

## Open Questions for Implementation

1. **Icon library**: Use `lucide-react` (recommended by shadcn/ui) or current icon setup?
   - **Recommendation**: Install lucide-react for consistency with shadcn/ui examples

2. **Form validation**: Keep current validation or migrate to react-hook-form?
   - **Recommendation**: Migrate to react-hook-form for better integration with shadcn/ui Form components

3. **Animation preferences**: Use default shadcn/ui animations or customize?
   - **Recommendation**: Use defaults (tailwindcss-animate) to maintain consistency

4. **Accessibility testing**: Manual testing or automated tools?
   - **Recommendation**: Use Lighthouse for automated checks + manual keyboard navigation testing

---

## References

- shadcn/ui Documentation: https://ui.shadcn.com/docs
- next-themes GitHub: https://github.com/pacocoursey/next-themes
- Next.js Dark Mode Guide: https://nextjs.org/docs/app/building-your-application/styling/css-variables
- Tailwind CSS Dark Mode: https://tailwindcss.com/docs/dark-mode
- FastAPI Logging: https://fastapi.tiangolo.com/tutorial/handling-errors/
