# Hackathon II: The Evolution of Todo (Phase I)

## 1. Project Context & Stack
- [cite_start]**Phase:** Phase I (In-Memory Python Console App) [cite: 92]
- **Goal:** Build a CLI Todo app with no persistence (data lives in a global list).
- [cite_start]**Runtime:** Python 3.13+ [cite: 100]
- [cite_start]**Manager:** `uv` (Universal Package Manager) [cite: 99]
- [cite_start]**Architecture:** strictly **In-Memory** (No SQLite/JSON/DB allowed yet)[cite: 94].

## 2. Core Commands
- **Run App:** `uv run python -m src.todo_console.main`
- **Test:** `uv run pytest`
- **Lint/Format:** `uv run ruff check .`
- **Spec-Kit:**
  - Create Spec: `/sp.specify "Add [feature name] to the todo list"`
  - Plan Architecture: `/sp.plan`
  - Implement Code: `/sp.implement`

## 3. Phase I Feature Requirements
- **Data Structure:** Use a global variable (e.g., `TODOS = []`) to store task objects/dictionaries.
- **Features:**
  1. [cite_start]Add Task (Title + Description) [cite: 39]
  2. [cite_start]View Task List (Show IDs and Status) [cite: 42]
  3. [cite_start]Update Task [cite: 41]
  4. [cite_start]Delete Task (by ID) [cite: 40]
  5. [cite_start]Mark Complete [cite: 43]

---

# --- AGENT WORKFLOW & RULES (DO NOT EDIT) ---

## 4. Development Guidelines (SDD)
**Your Success is Measured By:**
- **Strict Adherence:** All code must be generated from specs in `specs/history/`.
- **Traceability:** Every function must map back to a requirement.
- **Prompt History:** You must create PHRs for every significant interaction.

### A. Authoritative Source Mandate
Agents MUST prioritize and use MCP tools and CLI commands. NEVER assume a solution; verify externally.
- **Constitution:** Obey `Constitution.md` above all else.
- **Specs:** The files in `specs/` are the single source of truth.

### B. Knowledge Capture (PHR)
After completing implementation or planning tasks, you **MUST** create a Prompt History Record (PHR).

**Process:**
1. **Detect Stage:** (spec | plan | tasks | impl | refactor)
2. **Generate Path:** `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
3. **Write File:** Use the template at `.specify/templates/phr-template.prompt.md`.
   - Fill `PROMPT_TEXT` verbatim.
   - List modified files in `FILES_YAML`.
   - List tests run in `TESTS_YAML`.

### C. Architectural Decision Records (ADR)
If you make a significant technical decision (e.g., "How to structure the global list" or "Error handling strategy"), **Suggest** an ADR:
> " Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`."
*Never auto-create ADRs; wait for user consent.*

### D. Human as Tool Strategy
You are not expected to guess.
- **Ambiguity:** If the spec is unclear, ask clarifying questions.
- **Dependencies:** If a new library is needed, ask before adding it to `pyproject.toml`.

## 5. Coding Standards
- **Python 3.13:** Use modern typing (`list[str]`, not `List[str]`) and features.
- **Clean Code:** Small functions, descriptive names, type hints everywhere.
- **Testing:** 100% of new features must be covered by `pytest` test cases in `tests/`.
- **No Boilerplate:** Do not generate "example" code; generate only the implementation defined in the spec.
