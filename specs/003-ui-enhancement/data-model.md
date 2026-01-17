# Data Model: UI Enhancement with shadcn/ui and Infrastructure Cleanup

**Feature**: 003-ui-enhancement  
**Date**: 2026-01-15  
**Status**: Draft

## Overview

This feature primarily involves UI changes and infrastructure cleanup. There are minimal data model changes—the only new entity is the **Theme Preference**, which is stored client-side in browser localStorage.

---

## Entities

### 1. Theme Preference (Client-Side Storage)

**Description**: Stores the user's selected color theme (light or dark mode) in browser localStorage.

**Storage Location**: Browser localStorage  
**Storage Key**: `theme` (managed by next-themes library)  
**Scope**: Per-browser/device (not synced across user's devices)

**Schema**:

```typescript
type Theme = 'light' | 'dark';

interface ThemePreference {
  theme: Theme;
}
```

**Default Value**: `'light'` (when no preference is stored)

**Lifecycle**:
1. **Read**: On application initialization (page load)
2. **Write**: When user clicks theme toggle button
3. **Update**: Immediately when user changes preference
4. **Delete**: Not applicable (persists indefinitely until browser storage cleared)

**Validation Rules**:
- Must be one of: `'light'` or `'dark'`
- If stored value is invalid/corrupted, default to `'light'`
- If localStorage is blocked/disabled, use in-memory state (defaults to `'light'` on each visit)

**Access Patterns**:
- Read once on app load (by ThemeProvider)
- Write once per theme toggle (by ThemeToggle component)
- No network calls (entirely client-side)

---

### 2. Landing Page Content (Static Data)

**Description**: Static content displayed on the landing page. Not stored in a database—lives in component code.

**Storage Location**: React component JSX (hardcoded)

**Structure**:

```typescript
interface LandingPageContent {
  appName: string;          // "Todo Evolution"
  tagline: string;          // Brief description (1 sentence)
  valueProposition: string; // What problem does it solve (2-3 sentences)
  features: Feature[];      // List of key features
  ctaButtons: CTAButton[];  // Call-to-action buttons
}

interface Feature {
  title: string;        // Feature name
  description: string;  // Brief description (1-2 sentences)
  icon?: string;        // Icon name (from lucide-react)
}

interface CTAButton {
  label: string;       // Button text
  href: string;        // Navigation target
  variant: 'primary' | 'secondary'; // Button style
}
```

**Example Data**:

```typescript
const landingContent: LandingPageContent = {
  appName: "Todo Evolution",
  tagline: "Your personal productivity companion",
  valueProposition: "Manage tasks effortlessly with a clean, modern interface. Stay organized and accomplish more every day.",
  features: [
    {
      title: "Quick Task Creation",
      description: "Add tasks in seconds with a simple, intuitive interface",
      icon: "Plus"
    },
    {
      title: "Task Organization",
      description: "Keep your work organized with lists and categories",
      icon: "List"
    },
    {
      title: "Progress Tracking",
      description: "Check off completed tasks and track your achievements",
      icon: "CheckCircle"
    }
  ],
  ctaButtons: [
    { label: "Get Started", href: "/auth/signup", variant: "primary" },
    { label: "Sign In", href: "/auth/signin", variant: "secondary" }
  ]
};
```

**Lifecycle**: Immutable (changes require code updates)

---

### 3. UI Theme Configuration (CSS Variables)

**Description**: Color values and styling rules that define the appearance of the interface in light and dark modes.

**Storage Location**: `frontend/src/styles/globals.css`

**Structure** (CSS Custom Properties):

```css
:root {
  /* Light mode colors */
  --background: 0 0% 100%;           /* White background */
  --foreground: 222.2 84% 4.9%;      /* Dark text */
  --card: 0 0% 100%;                 /* Card background */
  --card-foreground: 222.2 84% 4.9%; /* Card text */
  --primary: 221.2 83.2% 53.3%;      /* Primary brand color */
  --primary-foreground: 210 40% 98%; /* Text on primary */
  --secondary: 210 40% 96.1%;        /* Secondary color */
  --secondary-foreground: 222.2 47.4% 11.2%;
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;
  --accent: 210 40% 96.1%;
  --accent-foreground: 222.2 47.4% 11.2%;
  --destructive: 0 84.2% 60.2%;      /* Error/delete color */
  --destructive-foreground: 210 40% 98%;
  --border: 214.3 31.8% 91.4%;
  --input: 214.3 31.8% 91.4%;
  --ring: 221.2 83.2% 53.3%;         /* Focus ring color */
  --radius: 0.5rem;                  /* Border radius */
}

.dark {
  /* Dark mode colors (inverted) */
  --background: 222.2 84% 4.9%;       /* Dark background */
  --foreground: 210 40% 98%;          /* Light text */
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
```

**Usage**: Colors are referenced in Tailwind CSS classes using HSL format:
```tsx
<div className="bg-background text-foreground">
  <Button className="bg-primary text-primary-foreground">
    Click me
  </Button>
</div>
```

**Modification**: To change colors, edit CSS variables in `globals.css`. All components update automatically.

---

## Relationships

```
ThemePreference (localStorage)
    ↓
ThemeProvider (React Context)
    ↓
All Components (consume theme via context)
    ↓
CSS Variables (apply colors based on theme class)
```

**Flow**:
1. User clicks ThemeToggle → updates ThemePreference in localStorage
2. ThemeProvider reads updated value → updates React context
3. Context change triggers re-render → components use new theme
4. `<html>` element receives `class="dark"` → CSS variables switch
5. All components inherit new colors via CSS custom properties

---

## No Backend Changes

**Important**: This feature does not modify any backend data models.

**Existing Backend Models (unchanged)**:
- `User`: Email, password hash, created_at, updated_at
- `Task`: Title, completed, user_id, created_at, updated_at
- `Session`: Token, user_id, expires_at

**Verification**: All backend tests should pass without modification after infrastructure cleanup.

---

## Migration Impact

### Sentry Removal Impact

**Backend Models**: No changes  
**Backend Configuration**: Remove Sentry config fields from `config.py`:
- `sentry_dsn`
- `sentry_traces_sample_rate`
- `sentry_profiles_sample_rate`

**Environment Variables to Remove**:
- `SENTRY_DSN`

### GitHub Actions Removal Impact

**Data Models**: No impact (CI/CD is external to application data)  
**Files to Delete**: `.github/workflows/ci.yml`

---

## State Management

### Client-Side State (React)

**Theme State**:
```typescript
// Managed by next-themes library
const { theme, setTheme } = useTheme();

// Internal state (not exposed):
// - theme: 'light' | 'dark' | 'system'
// - resolvedTheme: 'light' | 'dark' (actual applied theme)
```

**No New Server State**: This feature is entirely client-side. No new API endpoints or database tables are required.

---

## Validation Rules

### Theme Preference Validation

1. **Type Check**: Must be string `'light'` or `'dark'`
2. **Fallback**: If invalid, default to `'light'`
3. **Sanitization**: next-themes library handles this automatically

```typescript
// Validation logic (handled by next-themes)
function validateTheme(stored: string | null): Theme {
  if (stored === 'dark') return 'dark';
  return 'light'; // Default fallback
}
```

### Landing Page Content Validation

**No runtime validation needed** (static content in code).

**Build-time validation** (TypeScript):
- Feature titles must be non-empty strings
- Feature icons must match valid lucide-react icon names
- CTA button hrefs must be valid Next.js routes

---

## Testing Considerations

### Theme Preference Testing

**Unit Tests**:
- Theme toggle updates localStorage
- Invalid theme values default to 'light'
- Theme persists across page refreshes

**Integration Tests**:
- Theme applied to all pages (landing, auth, tasks)
- Theme toggle accessible from all pages
- No flicker on page load (SSR handled correctly)

**Edge Case Tests**:
- localStorage disabled → defaults to 'light' each visit
- localStorage corrupted → gracefully falls back to 'light'
- Multiple tabs → theme syncs across tabs (handled by next-themes)

### Landing Page Content Testing

**Visual Tests**:
- All features display correctly
- CTA buttons navigate to correct pages
- Content is readable and well-formatted

**Accessibility Tests**:
- Lighthouse accessibility score 90+
- Keyboard navigation works
- Screen reader compatibility

---

## Performance Considerations

### Theme Switching Performance

**Target**: <200ms toggle response (per success criteria SC-002)

**Optimization**:
- CSS variables allow instant theme switching (no component re-renders needed)
- localStorage write is synchronous and fast (~1ms)
- No network calls required

**Measurement**:
```typescript
// In ThemeToggle component
const handleToggle = () => {
  const start = performance.now();
  setTheme(theme === 'light' ? 'dark' : 'light');
  const end = performance.now();
  console.log(`Theme toggle took ${end - start}ms`);
};
```

### Landing Page Performance

**Target**: Lighthouse performance score 85+

**Optimization**:
- Static content (no API calls)
- Minimal JavaScript (only auth check)
- Optimized images (if any icons are images, use next/image)

---

## Summary

This feature introduces one new client-side entity (Theme Preference) and two configuration structures (Landing Page Content, UI Theme Variables). No backend database changes are required. The data model is intentionally simple to maintain the principle of simplicity (Constitution Principle VI).

**Key Points**:
- ✅ Theme stored in localStorage (per-device)
- ✅ No backend API changes
- ✅ No database migrations
- ✅ All data changes are client-side
- ✅ Existing backend models unchanged
