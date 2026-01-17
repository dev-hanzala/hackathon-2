# Tasks: UI Enhancement with shadcn/ui and Infrastructure Cleanup

**Input**: Design documents from `/specs/003-ui-enhancement/`  
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓, quickstart.md ✓

**Tests**: Tests are NOT explicitly requested in the specification. Focus on implementation and manual verification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. User stories are ordered by priority (P1 stories first, then P2, then P3).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

This is a **web application** with separate frontend and backend:
- Frontend: `frontend/src/`
- Backend: `backend/src/`
- Tests: `frontend/tests/`, `backend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and tooling setup

- [ ] T001 Verify current branch is 003-ui-enhancement and all existing tests pass
- [ ] T002 Document current application state (take screenshots of all pages for visual comparison)
- [ ] T003 [P] Create backup of current components in frontend/src/components/legacy/ directory

---

## Phase 2: User Story 4 - Infrastructure Cleanup (Priority: P1) 🎯

**Goal**: Remove Sentry and GitHub Actions infrastructure to simplify the project

**Independent Test**: Application starts and runs without Sentry errors; no CI/CD workflows trigger on push

**Why First**: This is a P1 story and should be completed early to avoid confusion. It's also a prerequisite for clean implementation of other stories (no Sentry references to work around).

### Implementation for User Story 4

- [ ] T004 [P] [US4] Remove Sentry SDK from backend/pyproject.toml dependencies section
- [ ] T005 [US4] Delete backend/src/monitoring/error_tracking.py file entirely
- [ ] T006 [US4] Remove Sentry initialization from backend/src/main.py (lines with sentry_sdk.init)
- [ ] T007 [US4] Remove Sentry config fields from backend/src/config.py (sentry_dsn, sentry_traces_sample_rate, sentry_profiles_sample_rate)
- [ ] T008 [US4] Remove SENTRY_DSN from backend/.env.example
- [ ] T009 [US4] Delete .github/workflows/ci.yml file
- [ ] T010 [US4] Run backend dependency sync: cd backend && uv sync
- [ ] T011 [US4] Start backend server and verify no Sentry-related errors: cd backend && uv run uvicorn src.main:app --reload
- [ ] T012 [US4] Run all backend tests to verify no breaks: cd backend && uv run pytest tests/
- [ ] T013 [US4] Run all frontend tests to verify no breaks: cd frontend && pnpm test
- [ ] T014 [US4] Search codebase for remaining "sentry" references: grep -r "sentry" backend/ frontend/ --exclude-dir=node_modules --exclude-dir=.git
- [ ] T015 [US4] Update README.md to remove Sentry and GitHub Actions from infrastructure section
- [ ] T016 [US4] Update docs/deployment-guide.md to remove Sentry environment variable instructions

**Checkpoint**: Infrastructure cleanup complete. Application runs cleanly without external dependencies.

---

## Phase 3: Foundational (shadcn/ui Setup) - Blocking for US1, US2, US3

**Purpose**: Install and configure shadcn/ui component library that all other stories depend on

**⚠️ CRITICAL**: User stories 1, 2, and 3 cannot proceed until shadcn/ui is installed

- [ ] T017 Install shadcn/ui CLI in frontend: cd frontend && npx shadcn@latest init (select: TypeScript=Yes, Style=Default, Base color=Slate, CSS variables=Yes, Tailwind config=tailwind.config.js, Import alias=@/components, RSC=Yes)
- [ ] T018 [P] Add Button component: cd frontend && npx shadcn@latest add button
- [ ] T019 [P] Add Card component: cd frontend && npx shadcn@latest add card
- [ ] T020 [P] Add Input component: cd frontend && npx shadcn@latest add input
- [ ] T021 [P] Add Label component: cd frontend && npx shadcn@latest add label
- [ ] T022 [P] Add Form component: cd frontend && npx shadcn@latest add form
- [ ] T023 [P] Add Checkbox component: cd frontend && npx shadcn@latest add checkbox
- [ ] T024 [P] Install lucide-react icons: cd frontend && pnpm add lucide-react
- [ ] T025 Verify shadcn/ui components exist in frontend/src/components/ui/ directory
- [ ] T026 Verify lib/utils.ts contains cn() utility function
- [ ] T027 Run type check to verify no errors: cd frontend && pnpm run type-check
- [ ] T028 Create simple test page to verify shadcn/ui components render: frontend/src/app/test-components/page.tsx

**Checkpoint**: shadcn/ui foundation ready - UI component work can now begin in parallel

---

## Phase 4: User Story 2 - Dark Mode Toggle (Priority: P2)

**Goal**: Implement theme switching with localStorage persistence

**Independent Test**: Toggle theme button switches between light/dark modes instantly, preference persists across page refreshes and browser sessions

**Why Before US1**: Landing page (US1) should have dark mode support from the start, so we implement theme system first

### Implementation for User Story 2

- [ ] T029 [P] [US2] Install next-themes library: cd frontend && pnpm add next-themes
- [ ] T030 [US2] Create theme provider in frontend/src/app/providers.tsx (wrap children with ThemeProvider from next-themes, set attribute="class", defaultTheme="light", enableSystem=false, storageKey="theme")
- [ ] T031 [US2] Update root layout frontend/src/app/layout.tsx to wrap children with Providers component and add suppressHydrationWarning to html element
- [ ] T032 [P] [US2] Add dark mode CSS variables to frontend/src/styles/globals.css (add :root and .dark selectors with color variables per research.md)
- [ ] T033 [P] [US2] Update frontend/tailwind.config.js to enable class-based dark mode (set darkMode: 'class') and add color tokens mapping to CSS variables
- [ ] T034 [US2] Create ThemeToggle component in frontend/src/components/ThemeToggle.tsx (use useTheme hook, Button component, Sun and Moon icons from lucide-react)
- [ ] T035 [US2] Add ThemeToggle to navigation/header (update frontend/src/app/layout.tsx or create Header component)
- [ ] T036 [US2] Test theme toggle on all existing pages (/, /auth/signin, /auth/signup, /tasks) and verify colors change correctly
- [ ] T037 [US2] Verify theme preference persists: toggle to dark, refresh page, should still be dark
- [ ] T038 [US2] Test edge case: clear localStorage, verify defaults to light mode
- [ ] T039 [US2] Measure theme toggle performance with performance.now() - verify <200ms (per SC-002)

**Checkpoint**: Dark mode system fully functional across all pages

---

## Phase 5: User Story 1 - Landing Page Experience (Priority: P1) 🎯 MVP

**Goal**: Create an attractive landing page that explains the app and invites sign up/sign in

**Independent Test**: Visit root URL without auth, see landing content with feature highlights and CTA buttons that navigate correctly; authenticated users get redirected to /tasks

**Why After US2**: Landing page should support dark mode from the start, so theme system (US2) is a prerequisite

### Implementation for User Story 1

- [ ] T040 [P] [US1] Create landing page content structure in frontend/src/app/page.tsx (replace existing basic landing with comprehensive content)
- [ ] T041 [P] [US1] Add hero section with app name "Todo Evolution", tagline "Your personal productivity companion", and value proposition using shadcn/ui Card and typography
- [ ] T042 [P] [US1] Add features section highlighting 3 key features (Quick Task Creation, Task Organization, Progress Tracking) with icons from lucide-react
- [ ] T043 [P] [US1] Add CTA buttons section with "Get Started" (primary, links to /auth/signup) and "Sign In" (secondary, links to /auth/signin) using shadcn/ui Button
- [ ] T044 [US1] Implement authenticated user redirect logic: if isAuthenticated, router.push('/tasks')
- [ ] T045 [US1] Style landing page layout with Tailwind CSS for responsive design (mobile, tablet, desktop breakpoints)
- [ ] T046 [US1] Verify landing page works in both light and dark modes
- [ ] T047 [US1] Test navigation: click "Get Started" → goes to /auth/signup
- [ ] T048 [US1] Test navigation: click "Sign In" → goes to /auth/signin
- [ ] T049 [US1] Test redirect: sign in as user, navigate to /, should redirect to /tasks
- [ ] T050 [US1] Test unauthenticated access: sign out, navigate to /, should show landing page
- [ ] T051 [US1] Run Lighthouse audit on landing page and verify Accessibility score 90+ and Performance score 85+ (per SC-007)

**Checkpoint**: Landing page complete and fully functional with dark mode support

---

## Phase 6: User Story 3 - Enhanced Component Library (Priority: P3)

**Goal**: Migrate existing components to shadcn/ui for consistent, polished UI

**Independent Test**: All forms and interactive elements use shadcn/ui components with consistent styling, proper hover/focus states, and responsive behavior

**Why Last**: This is a P3 story and builds on the foundation from US2 (theme) and US1 (landing page). It's polish work that can be done after core functionality exists.

### Implementation for User Story 3 - Task Components

- [ ] T052 [P] [US3] Migrate TaskItem component in frontend/src/components/TaskItem.tsx to use shadcn/ui Card, CardHeader, CardTitle, CardContent, CardFooter, and Button components
- [ ] T053 [P] [US3] Update TaskItem to use lucide-react icons (CheckCircle for complete, Trash2 for delete)
- [ ] T054 [P] [US3] Migrate TaskForm component in frontend/src/components/TaskForm.tsx to use shadcn/ui Form, Input, Label, and Button components
- [ ] T055 [P] [US3] Update TaskForm to use react-hook-form for validation (integrate with shadcn/ui Form)
- [ ] T056 [P] [US3] Migrate TaskList component in frontend/src/components/TaskList.tsx to use shadcn/ui Card for container
- [ ] T057 [US3] Test task components: create task, complete task, delete task - verify all actions work with new shadcn/ui components
- [ ] T058 [US3] Verify task components work in both light and dark modes
- [ ] T059 [US3] Test responsive behavior: resize browser window, verify task components adapt correctly

### Implementation for User Story 3 - Auth Forms

- [ ] T060 [P] [US3] Migrate SignIn form in frontend/src/app/auth/signin/page.tsx to use shadcn/ui Form, Input, Label, and Button components
- [ ] T061 [P] [US3] Migrate SignUp form in frontend/src/app/auth/signup/page.tsx to use shadcn/ui Form, Input, Label, and Button components
- [ ] T062 [P] [US3] Add validation feedback to auth forms using shadcn/ui FormMessage component
- [ ] T063 [US3] Test sign in flow: enter credentials, submit, verify form validation and submission work
- [ ] T064 [US3] Test sign up flow: create new account, verify form validation and submission work
- [ ] T065 [US3] Verify auth forms work in both light and dark modes

### Implementation for User Story 3 - UI Polish

- [ ] T066 [P] [US3] Add consistent hover states to all buttons across the application
- [ ] T067 [P] [US3] Add consistent focus states to all form inputs across the application
- [ ] T068 [P] [US3] Verify all interactive elements have proper loading states (buttons show loading spinner when actions are in progress)
- [ ] T069 [P] [US3] Verify all buttons have proper disabled states when actions cannot be performed
- [ ] T070 [US3] Test keyboard navigation: tab through all forms and buttons, verify focus order makes sense
- [ ] T071 [US3] Test on mobile device (or browser mobile emulation) and verify responsive layout works correctly
- [ ] T072 [US3] Test on tablet size and verify layout adapts appropriately

**Checkpoint**: All components migrated to shadcn/ui with consistent styling

---

## Phase 7: Integration & Polish

**Purpose**: Final verification, performance checks, and documentation updates

- [ ] T073 [P] Run full backend test suite: cd backend && uv run pytest tests/ (should pass 172/172 tests)
- [ ] T074 [P] Run full frontend test suite: cd frontend && pnpm test (should pass 73/73 tests - may need to update test selectors after component migration)
- [ ] T075 [P] Run backend linting: cd backend && uv run ruff check .
- [ ] T076 [P] Run backend type checking: cd backend && uv run mypy src
- [ ] T077 [P] Run frontend linting: cd frontend && pnpm run lint
- [ ] T078 [P] Run frontend type checking: cd frontend && pnpm run type-check
- [ ] T079 Build frontend for production and verify no errors: cd frontend && pnpm run build
- [ ] T080 Test end-to-end user journey (light mode): Visit landing → Sign Up → Create tasks → Complete tasks → Sign Out
- [ ] T081 Test end-to-end user journey (dark mode): Toggle to dark → Sign In → View tasks → Edit tasks → Sign Out
- [ ] T082 Test theme persistence: Set dark mode, close browser completely, reopen, should still be dark
- [ ] T083 Run Lighthouse audits on all pages (landing, auth, tasks) and verify scores meet targets
- [ ] T084 Compare before/after screenshots from T002 to verify visual improvements
- [ ] T085 Update frontend/README.md with shadcn/ui setup and dark mode information
- [ ] T086 Create frontend/src/components/README.md documenting component migration approach and shadcn/ui usage
- [ ] T087 Add npm script "pre-push" to frontend/package.json: "pnpm run lint && pnpm run type-check && pnpm test"
- [ ] T088 Document manual testing checklist in frontend/TESTING.md (since GitHub Actions is removed)
- [ ] T089 Final verification: Grep codebase for any remaining Sentry references that should be removed
- [ ] T090 Final verification: Confirm .github/workflows/ directory is completely empty or deleted

**Checkpoint**: All work complete, all tests passing, documentation updated

---

## Dependencies Between User Stories

```
Phase 1: Setup
    ↓
Phase 2: US4 (Infrastructure Cleanup) - P1
    ↓
Phase 3: Foundational (shadcn/ui Setup) - BLOCKING
    ↓
Phase 4: US2 (Dark Mode) - P2 ───────┐
    ↓                                 │
Phase 5: US1 (Landing Page) - P1     │
    ↓                                 │
Phase 6: US3 (Component Migration) ←─┘
    ↓
Phase 7: Integration & Polish
```

**Key Dependencies**:
1. **US4 must complete first**: Infrastructure cleanup (P1) should be done early
2. **Foundational blocks all UI work**: shadcn/ui must be installed before any component work
3. **US2 enables US1**: Landing page needs dark mode support, so theme system comes first
4. **US1 and US2 enable US3**: Component migration requires both landing page and theme system to be working

**Parallelization Opportunities**:
- Within US4: Tasks T004-T009 can run in parallel (different files)
- Within Foundational: Tasks T018-T024 can run in parallel (independent component installs)
- Within US2: Tasks T032-T033 can run in parallel (CSS and Tailwind config)
- Within US1: Tasks T040-T043 can run in parallel (different sections of landing page)
- Within US3 (Task Components): Tasks T052-T056 can run in parallel (different component files)
- Within US3 (Auth Forms): Tasks T060-T062 can run in parallel (different form files)
- Within US3 (Polish): Tasks T066-T069 can run in parallel (different aspects of UI)
- Final checks: Tasks T073-T078 can run in parallel (independent test/lint runs)

---

## Parallel Execution Examples

### Example 1: US4 Infrastructure Cleanup
```bash
# Can run these in parallel (different files):
Task T004: Edit backend/pyproject.toml
Task T005: Delete backend/src/monitoring/error_tracking.py
Task T006: Edit backend/src/main.py
Task T007: Edit backend/src/config.py
Task T008: Edit backend/.env.example
Task T009: Delete .github/workflows/ci.yml

# Then run these sequentially (depend on file changes):
Task T010: uv sync
Task T011: Start server test
Task T012: Run backend tests
Task T013: Run frontend tests
```

### Example 2: Foundational shadcn/ui Setup
```bash
# Can run these in parallel (independent component installations):
Task T018: npx shadcn@latest add button
Task T019: npx shadcn@latest add card
Task T020: npx shadcn@latest add input
Task T021: npx shadcn@latest add label
Task T022: npx shadcn@latest add form
Task T023: npx shadcn@latest add checkbox
Task T024: pnpm add lucide-react
```

### Example 3: US3 Component Migration
```bash
# Can run these in parallel (different component files):
Task T052: Migrate TaskItem.tsx
Task T053: Update TaskItem icons
Task T054: Migrate TaskForm.tsx
Task T055: Update TaskForm validation
Task T056: Migrate TaskList.tsx
```

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**Recommended MVP**: Complete through Phase 5 (US1 + US2 + US4)

**MVP Deliverables**:
- ✅ Infrastructure cleaned up (no Sentry, no GitHub Actions)
- ✅ Dark mode working with theme persistence
- ✅ Enhanced landing page with CTA buttons
- ❌ Component migration (P3 - can defer)

**MVP Testing**:
1. Visit root URL → see landing page
2. Toggle dark mode → see theme change
3. Refresh page → theme persists
4. Click "Get Started" → navigate to sign up
5. Sign in → landing page redirects to tasks
6. All existing task functionality still works

**MVP Duration**: Estimated 20-30 hours (T001-T051)

### Full Feature Scope

**Complete Implementation**: All phases (T001-T090)

**Full Deliverables**:
- ✅ MVP scope (US1 + US2 + US4)
- ✅ All components migrated to shadcn/ui (US3)
- ✅ Consistent UI polish across all pages
- ✅ Complete testing and documentation

**Full Duration**: Estimated 35-45 hours (T001-T090)

### Incremental Delivery Approach

**Iteration 1** (P1 stories): 
- US4: Infrastructure Cleanup (T004-T016)
- Delivers: Simplified codebase, no external dependencies

**Iteration 2** (Foundational + P2):
- Foundational: shadcn/ui Setup (T017-T028)
- US2: Dark Mode (T029-T039)
- Delivers: Theme system working

**Iteration 3** (P1 story):
- US1: Landing Page (T040-T051)
- Delivers: MVP complete - presentable landing page with dark mode

**Iteration 4** (P3 story):
- US3: Component Migration (T052-T072)
- Delivers: Full feature complete - polished UI

**Iteration 5** (Polish):
- Phase 7: Integration & Polish (T073-T090)
- Delivers: Production-ready, fully tested and documented

---

## Task Summary

**Total Tasks**: 90

**Tasks by Phase**:
- Phase 1 (Setup): 3 tasks
- Phase 2 (US4 - Infrastructure Cleanup): 13 tasks
- Phase 3 (Foundational - shadcn/ui): 12 tasks
- Phase 4 (US2 - Dark Mode): 11 tasks
- Phase 5 (US1 - Landing Page): 12 tasks
- Phase 6 (US3 - Component Migration): 21 tasks
- Phase 7 (Integration & Polish): 18 tasks

**Tasks by Priority**:
- P1 stories (US1, US4): 25 tasks
- P2 stories (US2): 11 tasks
- P3 stories (US3): 21 tasks
- Infrastructure (Setup, Foundational, Polish): 33 tasks

**Parallelizable Tasks**: 38 tasks marked with [P] can run in parallel

**MVP Tasks**: T001-T051 (51 tasks for minimal viable product)

---

## Validation Checklist

✅ **Format Validation**:
- All 90 tasks follow checklist format: `- [ ] T### [P?] [Story?] Description with file path`
- Task IDs sequential from T001 to T090
- [P] markers present for 38 parallelizable tasks
- [Story] labels present for user story tasks (US1, US2, US3, US4)
- All task descriptions include specific file paths

✅ **Organization Validation**:
- Tasks organized by user story priority (P1 → P2 → P3)
- Each user story is independently testable
- Clear checkpoints after each phase
- Dependencies explicitly documented

✅ **Completeness Validation**:
- All 4 user stories from spec.md covered
- All functional requirements (FR-001 through FR-021) addressed
- All success criteria (SC-001 through SC-008) testable
- Infrastructure cleanup tasks present
- shadcn/ui setup tasks present
- Component migration tasks present
- Testing and documentation tasks present

✅ **Executability Validation**:
- Each task is specific enough for LLM execution
- File paths are exact and unambiguous
- Commands include working directories (cd ...)
- Prerequisites clearly stated
- No ambiguous descriptions
