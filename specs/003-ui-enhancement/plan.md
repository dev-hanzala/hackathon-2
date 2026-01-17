# Implementation Plan: UI Enhancement with shadcn/ui and Infrastructure Cleanup

**Branch**: `003-ui-enhancement` | **Date**: 2026-01-15 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/003-ui-enhancement/spec.md`

## Summary

This feature enhances the user interface by integrating shadcn/ui as the component library, implementing a comprehensive dark mode with theme persistence, enhancing the existing landing page, and removing unnecessary infrastructure dependencies (Sentry error tracking and GitHub Actions CI/CD). The work combines cleanup tasks with new functionality to create a more polished, modern application that is simpler to maintain and deploy.

**Primary Goals**:
1. Remove Sentry SDK and GitHub Actions CI/CD infrastructure
2. Install and configure shadcn/ui component library
3. Implement dark mode with localStorage persistence
4. Enhance landing page with better content and structure
5. Migrate existing components to shadcn/ui for consistency

## Technical Context

**Language/Version**: TypeScript 5.3.3 with Next.js 16.1.2 (frontend), Python 3.13+ (backend)  
**Primary Dependencies**: 
- Frontend: React 19, Next.js 16, shadcn/ui (to be added), Tailwind CSS 3.4, @tanstack/react-query 5.40
- Backend: FastAPI, SQLModel, PostgreSQL (no changes required for this feature)

**Storage**: 
- Theme preference: Browser localStorage
- No database changes required

**Testing**: 
- Frontend: Jest 29.7 with @testing-library/react 16.0
- Backend tests unaffected (pytest suite remains)

**Target Platform**: Modern web browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)  

**Project Type**: Web application (separate frontend and backend)  

**Performance Goals**: 
- Theme toggle response: <200ms
- Landing page Lighthouse score: Accessibility 90+, Performance 85+
- No performance degradation from current baseline

**Constraints**: 
- Must maintain existing authentication and task management functionality
- Theme preference stored client-side only (no backend API changes)
- Landing page must remain publicly accessible (no authentication required)
- Zero downtime during infrastructure removal

**Scale/Scope**: 
- ~15 existing React components to migrate to shadcn/ui
- ~8 pages to theme (landing, auth pages, tasks, error pages)
- ~50 LOC to remove (Sentry integration)
- ~1 GitHub Actions workflow file to delete

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Spec-Driven Development (SDD)
- **Status**: PASS
- **Evidence**: Formal specification exists at `specs/003-ui-enhancement/spec.md` with all user stories, requirements, and success criteria defined before implementation

### ✅ Prompt History Records (PHR Mandate)
- **Status**: PASS
- **Evidence**: PHR created for spec generation (`history/prompts/003-ui-enhancement/0001-ui-enhancement-spec-created.spec.prompt.md`). Plan generation will create additional PHR.

### ✅ Architectural Decision Records (ADR)
- **Status**: PENDING EVALUATION
- **Decisions to evaluate**:
  1. Choice of shadcn/ui over other component libraries (Chakra UI, Material UI, Ant Design)
  2. Client-side theme storage (localStorage) vs server-side preference storage
  3. Removal of Sentry without replacement error tracking solution
- **Action**: Will suggest ADR creation after Phase 1 design if decisions meet significance criteria

### ✅ Test-First Development
- **Status**: PASS
- **Evidence**: Tasks will follow red-green-refactor cycle. Tests required for:
  - Theme toggle component and persistence logic
  - Landing page content and routing behavior
  - Component migration (verify shadcn/ui components work as replacements)
  - Infrastructure removal (verify no broken imports or runtime errors)

### ✅ Library-First Design
- **Status**: N/A
- **Rationale**: This is a UI enhancement and infrastructure cleanup, not a new library. Work is tightly coupled to Next.js application.

### ✅ Simplicity & YAGNI
- **Status**: PASS with JUSTIFICATION
- **Adherence**: 
  - Removing unused infrastructure (Sentry, GitHub Actions) reduces complexity ✅
  - Adding shadcn/ui components only for existing UI elements (no speculative components) ✅
  - Theme system limited to light/dark (no custom themes, animations, or system preference detection) ✅
- **Justified complexity**:
  - Adding shadcn/ui: Required for modern UI patterns and long-term maintainability
  - Theme persistence: Required per FR-008 (user expectation for preferences to persist)

### 🔄 Re-evaluation After Phase 1
Will re-check Constitution compliance after data model and contracts are finalized.

## Project Structure

### Documentation (this feature)

```text
specs/003-ui-enhancement/
├── spec.md              # Feature specification (DONE)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output - technology choices and patterns
├── data-model.md        # Phase 1 output - theme preference entity model
├── quickstart.md        # Phase 1 output - developer setup guide
├── contracts/           # Phase 1 output - component API contracts
│   └── theme-api.md     # Theme provider and toggle component contracts
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

This is a **web application** with separate frontend and backend.

```text
backend/
├── src/
│   ├── main.py                          # [MODIFY] Remove Sentry initialization
│   ├── config.py                        # [MODIFY] Remove Sentry config vars
│   └── monitoring/
│       └── error_tracking.py            # [DELETE] Entire Sentry module
└── tests/                               # [VERIFY] All tests still pass after cleanup

frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx                     # [ENHANCE] Landing page content
│   │   ├── layout.tsx                   # [MODIFY] Add theme provider
│   │   ├── auth/                        # [MIGRATE] Auth forms to shadcn/ui
│   │   └── tasks/                       # [MIGRATE] Task components to shadcn/ui
│   ├── components/
│   │   ├── ThemeProvider.tsx            # [NEW] Theme context and persistence
│   │   ├── ThemeToggle.tsx              # [NEW] Dark mode toggle button
│   │   ├── ui/                          # [NEW] shadcn/ui components directory
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   ├── form.tsx
│   │   │   └── ...                      # Other shadcn/ui components as needed
│   │   ├── TaskItem.tsx                 # [MIGRATE] Use shadcn/ui Card, Button
│   │   ├── TaskForm.tsx                 # [MIGRATE] Use shadcn/ui Form, Input, Button
│   │   └── TaskList.tsx                 # [MIGRATE] Use shadcn/ui Card
│   ├── lib/
│   │   └── utils.ts                     # [NEW] shadcn/ui utility (cn function)
│   └── styles/
│       └── globals.css                  # [MODIFY] Add dark mode CSS variables
├── components.json                      # [NEW] shadcn/ui configuration
├── tailwind.config.js                   # [MODIFY] Add shadcn/ui theme config
└── tests/
    └── __tests__/
        ├── ThemeProvider.test.tsx       # [NEW] Theme persistence tests
        ├── ThemeToggle.test.tsx         # [NEW] Toggle interaction tests
        └── ...                          # [UPDATE] Existing component tests

.github/
└── workflows/
    └── ci.yml                           # [DELETE] Remove GitHub Actions CI/CD

.env.example                             # [MODIFY] Remove SENTRY_DSN
backend/.env.example                     # [MODIFY] Remove Sentry vars
backend/pyproject.toml                   # [MODIFY] Remove sentry-sdk dependency
frontend/package.json                    # [MODIFY] Add shadcn/ui dependencies
```

**Structure Decision**: Existing web application structure is preserved. Frontend receives new theme-related components and migrates existing components to shadcn/ui. Backend only requires cleanup (no new functionality). Infrastructure files (GitHub Actions workflows) are deleted entirely.

## Complexity Tracking

> **No Constitution violations requiring justification.**

All complexity additions are justified by functional requirements in the spec:
- shadcn/ui integration: Required by FR-012
- Theme provider and persistence: Required by FR-006 through FR-011
- Enhanced landing page: Required by FR-001 through FR-005

Infrastructure removal (Sentry, GitHub Actions) reduces overall project complexity.

## Phase 0: Research & Technology Decisions

### Research Questions

1. **shadcn/ui Installation**: What is the recommended setup process for shadcn/ui with Next.js 16?
2. **Theme Implementation**: What are best practices for implementing dark mode with Tailwind CSS and Next.js 13+ app router?
3. **Component Migration**: What is the systematic approach to migrating existing custom components to shadcn/ui?
4. **localStorage Best Practices**: How should theme preferences be stored, retrieved, and synced with SSR in Next.js?
5. **Sentry Removal Impact**: What logging/error handling should replace Sentry for basic error visibility?
6. **GitHub Actions Alternatives**: What should developers do for testing and quality checks without CI/CD?

### Expected Outputs

A `research.md` file documenting:
- shadcn/ui setup steps and configuration options
- Dark mode implementation patterns with Tailwind CSS
- Component migration strategy (prioritization, testing approach)
- Theme persistence implementation with SSR considerations
- Error logging strategy post-Sentry removal
- Developer workflow recommendations post-CI/CD removal

## Phase 1: Design & Contracts

### Data Model

Create `data-model.md` with:

**Theme Preference Entity**:
- **Storage**: Browser localStorage
- **Key**: `todo-app-theme`
- **Values**: `"light"` | `"dark"`
- **Default**: `"light"`
- **Lifecycle**: Set on toggle, read on app initialization
- **Validation**: Must be one of allowed values; invalid/missing defaults to "light"

**Theme Configuration**:
- **Color variables**: Defined in `globals.css` using CSS custom properties
- **Scope**: Global (applies to all pages and components)
- **Sync**: Theme applied immediately on toggle, no page refresh required

### API Contracts

Create `contracts/` directory with:

**contracts/theme-api.md** - Define:
1. **ThemeProvider Component**:
   - Props: `children`, `defaultTheme?`, `storageKey?`
   - Context values: `theme`, `setTheme()`
   - Behavior: Reads from localStorage, provides theme to children

2. **ThemeToggle Component**:
   - Props: `className?`
   - Behavior: Renders toggle button, calls `setTheme()` on click
   - States: Shows sun icon (light mode) or moon icon (dark mode)

3. **shadcn/ui Component APIs**:
   - Button: variants (default, destructive, outline, ghost), sizes, disabled, loading
   - Card: header, content, footer structure
   - Input: label, error state, helper text
   - Form: integration with react-hook-form, validation display

### Quickstart Guide

Create `quickstart.md` with:
- Prerequisites (Node.js version, pnpm)
- shadcn/ui installation commands
- How to add new shadcn/ui components
- How to test theme toggle locally
- How to verify Sentry removal (no errors on startup)
- How to run tests after infrastructure cleanup

### Agent Context Update

Run `.specify/scripts/bash/update-agent-context.sh opencode` to update `.opencode/context.md` with:
- shadcn/ui as the UI component library
- Theme implementation approach (Tailwind CSS + localStorage)
- Note about removed infrastructure (Sentry, GitHub Actions)

## Phase 2: Implementation Tasks

**Note**: Tasks are generated by `/sp.tasks` command (not part of `/sp.plan`). This section outlines the expected task structure.

### Expected Task Phases

**Phase 0: Infrastructure Cleanup (Priority: P1)**
- Remove Sentry SDK from backend dependencies and imports
- Delete GitHub Actions workflow files
- Update environment variable documentation
- Verify application starts without errors
- Run full test suite to ensure no breaks

**Phase 1: shadcn/ui Setup (Priority: P1)**
- Install shadcn/ui CLI and initialize configuration
- Add base shadcn/ui components (button, card, input, form)
- Configure Tailwind CSS for shadcn/ui theme
- Add utility functions (cn helper)
- Write component documentation

**Phase 2: Theme System (Priority: P2)**
- Create ThemeProvider with localStorage integration
- Implement ThemeToggle component
- Add dark mode CSS variables to globals.css
- Update root layout to include ThemeProvider
- Test theme persistence across page refreshes
- Write unit tests for theme functionality

**Phase 3: Landing Page Enhancement (Priority: P1)**
- Enhance landing page content (better copy, feature highlights)
- Apply shadcn/ui components to landing page
- Verify authenticated user redirect
- Test navigation to auth pages
- Accessibility audit (Lighthouse)

**Phase 4: Component Migration (Priority: P3)**
- Migrate TaskForm to shadcn/ui components
- Migrate TaskItem to shadcn/ui components
- Migrate TaskList to shadcn/ui components
- Migrate auth forms (SignIn, SignUp) to shadcn/ui
- Update all component tests
- Visual regression testing

**Phase 5: Integration & Polish**
- End-to-end theme testing across all pages
- Verify responsive behavior on mobile/tablet/desktop
- Performance testing (Lighthouse scores)
- Final cleanup (remove unused Tailwind classes, old component code)
- Update documentation (README, deployment guides)

## Design Decisions

### Decision 1: shadcn/ui as Component Library

**Chosen**: shadcn/ui  
**Rationale**:
- Copy-paste architecture (components live in project, not node_modules)
- Full control over component customization
- Excellent Tailwind CSS integration
- Strong TypeScript support
- Active community and documentation
- Radix UI primitives for accessibility

**Alternatives Considered**:
- **Chakra UI**: More opinionated, theme overrides more complex
- **Material UI**: Heavier bundle size, different design language
- **Ant Design**: Less Tailwind-friendly, more prescriptive

**Tradeoffs**:
- Pro: Complete customization control, smaller bundle (tree-shakeable)
- Con: Manual component updates (no npm package updates)

**ADR Candidate**: YES (meets all three criteria - long-term impact, alternatives considered, cross-cutting design decision)

### Decision 2: Client-Side Theme Storage

**Chosen**: localStorage with no server sync  
**Rationale**:
- Simple implementation (no backend changes)
- Fast toggle response (<200ms requirement)
- No authentication required (works on landing page)
- Per-device preference is acceptable UX

**Alternatives Considered**:
- **Server-side storage**: Requires backend API, authentication dependency, slower initial load
- **System preference detection**: Out of scope per spec assumptions
- **Cookies**: No SSR benefit, same limitations as localStorage

**Tradeoffs**:
- Pro: Simplicity, no backend work, fast performance
- Con: Not synced across user's devices

**ADR Candidate**: NO (clear requirement in spec, limited alternatives, not architecturally significant)

### Decision 3: Sentry Removal Without Replacement

**Chosen**: Remove Sentry, use console logging and FastAPI default error handling  
**Rationale**:
- Application is hackathon/prototype scope
- Local testing is sufficient for current needs
- Reduces external dependencies and costs
- FastAPI has built-in error handling and logging

**Alternatives Considered**:
- **Replace with open-source alternative**: Sentry self-hosted, Glitchtip (adds complexity)
- **Keep Sentry**: User explicitly requested removal

**Tradeoffs**:
- Pro: Simpler deployment, no external service dependencies
- Con: Less visibility into production errors (acceptable for prototype)

**ADR Candidate**: YES (long-term impact on error visibility, alternative monitoring solutions exist, affects operational practices)

### Decision 4: No CI/CD Replacement

**Chosen**: Manual local testing before commits  
**Rationale**:
- User explicitly requested GitHub Actions removal
- Small team/solo development context
- Tests can be run locally before pushing

**Alternatives Considered**:
- **Different CI/CD provider**: CircleCI, GitLab CI (adds new external dependency)
- **Keep GitHub Actions**: User explicitly requested removal
- **Git hooks**: Pre-commit hooks could run tests, but adds local setup complexity

**Tradeoffs**:
- Pro: No external services, simpler deployment pipeline
- Con: Requires developer discipline (must remember to run tests)

**ADR Candidate**: NO (user directive, temporary decision for prototype phase)

## Risk Mitigation

### Risk 1: Incomplete Sentry Removal Causes Runtime Errors
**Mitigation**:
- Comprehensive grep for all Sentry references before testing
- Test application startup in clean environment
- Add checklist item to search for: `sentry`, `SENTRY_`, `sentry_sdk`, `error_tracking`

### Risk 2: Component Migration Breaks Existing Functionality
**Mitigation**:
- Migrate one component at a time
- Run existing test suite after each migration
- Visual comparison testing (before/after screenshots)
- Keep existing components until shadcn/ui replacements are verified

### Risk 3: Theme Flicker on Page Load (SSR Mismatch)
**Mitigation**:
- Use Next.js `next-themes` library pattern for SSR-safe theme handling
- Apply theme class to `<html>` element before first paint
- Test with JavaScript disabled to verify fallback

### Risk 4: Developers Forget to Run Tests Without CI/CD
**Mitigation**:
- Document testing workflow clearly in README
- Add npm script shortcuts for pre-push checks (`npm run pre-push`)
- Consider adding Git pre-commit hooks (optional)

### Risk 5: Accessibility Regression from Component Changes
**Mitigation**:
- shadcn/ui uses Radix UI primitives (built-in accessibility)
- Run Lighthouse accessibility audit before and after
- Test keyboard navigation on all migrated components
- Use ARIA labels where needed

## Success Metrics

From spec success criteria (SC-001 through SC-008):

1. **Landing page comprehension**: Verified through user testing or readability metrics
2. **Theme toggle performance**: Measured with performance.now(), target <200ms
3. **Theme persistence**: 100% success rate in test suite (refresh, close/reopen tests)
4. **Sentry removal**: Zero grep matches for sentry-related strings
5. **Infrastructure cleanup**: Zero files in `.github/workflows/`, no Sentry in dependencies
6. **Component consistency**: Visual regression testing shows consistent styling
7. **Lighthouse scores**: Accessibility 90+, Performance 85+
8. **Navigation success**: Functional tests verify 2-click path to sign up/sign in

## Next Steps

1. ✅ **Completed**: Specification created (`spec.md`)
2. ✅ **Completed**: Implementation plan created (this file)
3. 🔄 **Next**: Run `/sp.tasks specs/003-ui-enhancement/plan.md` to generate detailed task breakdown
4. ⏭️ **Then**: Begin implementation with Phase 0 (Infrastructure Cleanup)

## ADR Recommendations

**Suggested ADRs** (require user approval via `/sp.adr <title>`):

1. **ADR: Selection of shadcn/ui as Component Library**
   - Decision meets all three significance criteria
   - Affects long-term maintainability and developer experience
   - Multiple viable alternatives existed

2. **ADR: Removal of Sentry Error Tracking Without Replacement**
   - Significant operational decision
   - Affects production error visibility and debugging capability
   - Alternative monitoring solutions were considered

**Command to create**: User should run `/sp.adr "shadcn-ui-component-library"` and `/sp.adr "remove-sentry-error-tracking"` if they wish to document these decisions formally.
