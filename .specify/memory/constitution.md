<!--
SYNC IMPACT REPORT
Version: 1.0.0 → 2.0.0
Version Bump Rationale: MINOR - Added three new principles (PHR Mandate, ADR Requirement, Spec-Driven Governance) and Governance section; Spec-Kit-Plus alignment requirement.
Modified Principles:
  - [PRINCIPLE_1_NAME] → I. Spec-Driven Development (SDD)
  - [PRINCIPLE_2_NAME] → II. Prompt History Records (PHR Mandate)
  - [PRINCIPLE_3_NAME] → III. Architectural Decision Records (ADR)
  - [PRINCIPLE_4_NAME] → IV. Test-First Development
  - [PRINCIPLE_5_NAME] → V. Library-First Design
  - [PRINCIPLE_6_NAME] → VI. Simplicity & YAGNI
Added Sections:
  - Development Workflow: Code review, testing gates, deployment approval
  - Spec-Kit-Plus Governance: Alignment with spec-kit-plus tooling
Removed Sections: None
Templates Updated:
  ✅ plan-template.md: aligns with PHR mandate and ADR requirement
  ✅ spec-template.md: includes constitution compliance checks
  ✅ tasks-template.md: task categorization reflects PHR and ADR principles
  ⚠ commands: Review all .claude/commands for spec-kit-plus references
Deferred Items: None
-->

# Todo Evolution - Hackathon II Constitution

## Core Principles

### I. Spec-Driven Development (SDD)

All features begin with a formal specification in `specs/<feature>/spec.md`. Specifications MUST precede any implementation work. Every feature progresses through defined stages: spec → plan → tasks → implementation. Specs are the source of truth for requirements and acceptance criteria. Deviations from spec require formal amendment with user approval.

**Rationale:** Preventing rework and misalignment by establishing contracts before code.

### II. Prompt History Records (PHR Mandate)

Every user prompt MUST result in a Prompt History Record (PHR) created immediately after completion of the associated work. PHRs are not optional and serve as the project's authoritative audit trail and learning repository.

**Requirements:**
- PHR created for ALL work: implementation, planning, debugging, spec creation, multi-step workflows
- PHR routing: Constitution work → `history/prompts/constitution/`; Feature-specific → `history/prompts/<feature-name>/`; General → `history/prompts/general/`
- Full verbatim PROMPT_TEXT preserved (no truncation)
- Key RESPONSE_TEXT captured (concise summary of output)
- ID, title, stage, date, files, tests, and outcome metadata mandatory
- No unresolved placeholders; validation checks pass before file written

**Rationale:** PHRs create continuity, enable learning from past decisions, support audit trails, and facilitate onboarding.

### III. Architectural Decision Records (ADR)

Significant architectural decisions MUST be documented in Architecture Decision Records (ADRs). ADR creation is REQUIRED when:
- Decision has long-term consequences (framework choice, data model, API design, security model, platform choice)
- Multiple viable alternatives existed and tradeoffs were explicitly considered
- Decision is cross-cutting and influences system design

**Requirements:**
- After design/planning work, evaluate decision significance using three-part test
- If ALL criteria met, suggest ADR creation: "📋 Architectural decision detected: <brief> — Document? Run `/sp.adr <title>`"
- Wait for explicit user consent before creating ADR file
- Group related decisions into single ADR when appropriate (e.g., auth stack, deployment strategy)
- Never auto-create ADRs; require user approval

**Rationale:** Preserves architectural reasoning, prevents repeated debates, supports future maintainers.

### IV. Test-First Development (NON-NEGOTIABLE)

Test-Driven Development (TDD) is mandatory for all implementation work. The Red-Green-Refactor cycle MUST be strictly enforced:
1. Write tests first (RED: tests fail)
2. Get user approval on test approach
3. Implement to pass tests (GREEN: tests pass)
4. Refactor only after tests pass

Integration tests are required for:
- New library contract tests
- Contract changes
- Inter-service communication
- Shared schema modifications
- API endpoint integration

**Rationale:** Ensures correctness, prevents regression, improves design.

### V. Library-First Design

Every significant feature starts as a standalone library. Libraries MUST be:
- Self-contained and independently testable
- Have clear, documented purpose (no organizational-only libraries)
- Expose functionality via CLI with text-based I/O protocol: stdin/args → stdout; errors → stderr
- Support both JSON and human-readable output formats

**Rationale:** Maximizes reusability and testability; enforces clean boundaries.

### VI. Simplicity & YAGNI

Start simple. Do not add features, refactoring, or abstractions for hypothetical future requirements. The right amount of complexity is the minimum needed for the current task. Three similar lines of code is better than premature abstraction.

**Implementation rules:**
- No over-engineering of error handling, fallbacks, or validation for scenarios that cannot occur
- Trust internal code and framework guarantees; validate only at system boundaries (user input, external APIs)
- Delete unused code completely; avoid backwards-compatibility hacks or re-exports
- Smallest viable change; do not refactor surrounding code unless directly requested

**Rationale:** Faster delivery, easier maintenance, reduced cognitive load.

## Development Workflow

### Code Review Requirements

- All PRs MUST reference associated spec, plan, tasks, or PHR
- Code MUST comply with all Constitution principles
- Changes MUST be small and testable (reference code by file:line)
- All type errors, linting violations, and test failures MUST be resolved before merge

### Quality Gates

- Test suite MUST pass (100% of written tests)
- Type checking MUST pass (no errors, only approved warnings)
- Linting MUST pass (project-configured rules)
- PHR MUST exist and be complete (no unresolved placeholders)
- If ADR-significant decision made, ADR MUST be created or explicit deferral documented

### Deployment Approval Process

- Feature branches require approval from at least one reviewer
- Merges to main require passing all automated checks
- Release branches require approval plus verification of version bump

## Spec-Kit-Plus Governance

This project operates under **Spec-Kit-Plus**, a formal spec-driven development framework. All tools and commands (sp.spec, sp.plan, sp.tasks, sp.phr, sp.adr, etc.) are authoritative sources for workflow execution.

**Tool Compliance:**
- `/sp.specify` — Create or update feature specifications
- `/sp.plan` — Generate architecture and implementation plans
- `/sp.tasks` — Generate testable, dependency-ordered tasks
- `/sp.phr` — Record user inputs and AI responses as PHRs
- `/sp.adr` — Create Architecture Decision Records
- `/sp.analyze` — Cross-artifact consistency analysis
- `/sp.checklist` — Generate custom feature checklists

All artifacts created by these commands MUST be treated as formal project documentation and are subject to Constitution review.

## Governance

**Constitution Authority:**
This Constitution supersedes all other practices, guidelines, and coding standards. When conflicts arise, Constitution principles take precedence.

**Amendment Procedure:**
- Amendments require explicit user request or detected inconsistency
- Proposed amendments MUST include rationale and impact analysis
- Version number MUST increment according to semantic versioning:
  - MAJOR: Backward-incompatible principle removals or redefinitions
  - MINOR: New principle/section added or materially expanded guidance
  - PATCH: Clarifications, wording, typo fixes, non-semantic refinements
- Amendment MUST be documented in commit message and flagged in header comment

**Compliance Review:**
- Every spec, plan, tasks, and PHR MUST be validated against Constitution before merge
- Automated tools (linters, type checkers) MUST pass
- Manual review MUST confirm principle alignment

**Runtime Guidance:**
Development guidance is documented in:
- `CLAUDE.md` — AI agent-specific rules and execution contract
- `.specify/memory/constitution.md` — This file (project-wide principles)
- Feature-specific docs in `specs/<feature>/` (feature requirements and architecture)

**Version**: 2.0.0 | **Ratified**: 2025-01-10 | **Last Amended**: 2026-01-10
