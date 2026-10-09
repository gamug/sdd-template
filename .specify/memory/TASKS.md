# SDD Tasks

Task register for the hierarchy `FR-001 > WI > Task` defined in
[`PLAN.md`](./PLAN.md). Every task has exactly one parent Work Item.

`Status: pending` is the template value. This register is immutable, so task
status is not tracked before WI-003: TASK-010 carries it into
`.sdd/TASKS.md`, marks TASK-001 through TASK-009 done, and tracks status there
from then on.

## WI-001 — Run the discovery skill and create PRODUCT.md

### TASK-001 — Execute the discovery workflow

- **Work Item:** WI-001
- **Status:** pending
- **Depends on:** none
- **Acceptance criteria:** AC-FR001-01
- **Action:** Run all six phases of `skills/tech-use-case-discovery/SKILL.md`,
  including the Governance & Workflow checklist. Nothing else in FR-001 may
  start before this task.

### TASK-002 — Collect discovery outputs

- **Work Item:** WI-001
- **Status:** pending
- **Depends on:** TASK-001
- **Acceptance criteria:** AC-FR001-01
- **Action:** Assemble use cases, requirements, user stories, stack evaluation,
  ADRs, environment and governance decisions, risks, and roadmap.

### TASK-003 — Write PRODUCT.md

- **Work Item:** WI-001
- **Status:** pending
- **Depends on:** TASK-002
- **Acceptance criteria:** AC-FR001-01
- **Action:** Write `docs/PRODUCT.md`, mark every open decision with
  `UNRESOLVED:`, and run
  `python skills/tech-use-case-discovery/scripts/validate_discovery.py --draft docs/PRODUCT.md`
  until it passes.

### TASK-004 — Resolve open decisions and record approval

- **Work Item:** WI-001
- **Status:** pending
- **Depends on:** TASK-003
- **Acceptance criteria:** AC-FR001-01
- **Action:** Ask the user about every `UNRESOLVED:` item and update
  `docs/PRODUCT.md`. Present the document for approval and record it in its
  `## Approval` section (`Approved by:`, `Approved on: YYYY-MM-DD`, and
  `Approved content:` with the hash printed by `validate_discovery.py --hash
  docs/PRODUCT.md` once the user has approved). Run the validator without
  `--draft`; it must pass. Any later edit outside the Approval and
  Configuration Decisions sections invalidates the approval until the user
  approves again. This is the entry gate of WI-002, enforced by
  `validate_config.py`.

## WI-002 — Create config.yaml

### TASK-005 — Scaffold config.yaml and fill stated values

- **Work Item:** WI-002
- **Status:** pending
- **Depends on:** TASK-004
- **Acceptance criteria:** AC-FR001-02
- **Action:** Run `uv run --with pyyaml==6.0.2 python skills/tech-use-case-discovery/scripts/validate_config.py scaffold`. It writes the `config.yaml` skeleton,
  with the PRODUCT.md section each key usually comes from, and appends the
  `Configuration Decisions` table to `docs/PRODUCT.md`. Fill only values that
  `docs/PRODUCT.md` states explicitly, and record each one in the table with
  source `PRODUCT.md § <section>`; `check` verifies that the section exists,
  has no subsections, and contains the value (every item, for lists and maps)
  as a whole token, so `3.1` is not evidence for "3.12.2". The Approval and
  Configuration Decisions sections are never evidence. Record lists and maps as compact JSON
  and escape `|` in values as `\|`.

### TASK-006 — Define domain sections

- **Work Item:** WI-002
- **Status:** pending
- **Depends on:** TASK-005
- **Acceptance criteria:** AC-FR001-02
- **Action:** From the use cases, functional requirements, ADRs, and risks in
  `docs/PRODUCT.md`, propose the domain-specific constitution sections (for
  example models, services, storage, AI behavior, evaluation) as
  `domain_sections` entries with a `title` and `rules`. Confirm them with the
  user, write them to `config.yaml`, and record the `domain_sections` row as
  compact JSON with source `user, YYYY-MM-DD` (`check` rejects a
  `PRODUCT.md §` source here) so `check` detects any later change. An
  empty list is valid only when the user confirms the project needs none.

### TASK-007 — Ask the user for every remaining value

- **Work Item:** WI-002
- **Status:** pending
- **Depends on:** TASK-006
- **Acceptance criteria:** AC-FR001-02
- **Action:** This task is the only place configuration questions are asked.
  For every value `docs/PRODUCT.md` does not state, ask a context-rich
  question. A value the document only implies is proposed to the user and
  confirmed, never written silently. Record each answer in the table with
  source `user, YYYY-MM-DD`. Propose `.github/workflows/validators.yml` as
  `quality.ci_file`: the project's quality gates are added to that inherited
  workflow, so it stays the single CI file.

### TASK-008 — Validate config.yaml

- **Work Item:** WI-002
- **Status:** pending
- **Depends on:** TASK-007
- **Acceptance criteria:** AC-FR001-02
- **Action:** Run `uv run --with pyyaml==6.0.2 python skills/tech-use-case-discovery/scripts/validate_config.py check`. It fails on missing or empty keys, keys
  without a valid recorded source, and recorded values that differ from
  `config.yaml`. Return to TASK-007 for every reported key.

## WI-003 — Render constitution.md and synchronize SDD objects

### TASK-009 — Render constitution.md

- **Work Item:** WI-003
- **Status:** pending
- **Depends on:** TASK-008
- **Acceptance criteria:** AC-FR001-03
- **Action:** Run `uv run --with pyyaml==6.0.2 python skills/tech-use-case-discovery/scripts/validate_config.py render` to create `.sdd/constitution.md` from root
  `config.yaml` and the immutable `.specify/memory/constitution.md`. Rendering
  re-runs `check` and fails on any missing value or leftover placeholder. Do
  not edit the rendered file by hand; re-run `render` after any
  `config.yaml` change.

### TASK-010 — Synchronize all SDD objects

- **Work Item:** WI-003
- **Status:** pending
- **Depends on:** TASK-009
- **Acceptance criteria:** AC-FR001-03
- **Action:** Create or update `.sdd/SPEC.md`, `.sdd/PLAN.md`, `.sdd/TASKS.md`,
  and `.sdd/CHANGELOG.md` to match the approved `docs/PRODUCT.md` and preserve
  traceability. Keep `FR-001` and its Work Items as the initialization
  requirement and add the product requirements from `docs/PRODUCT.md`, which
  are numbered from `FR-002`. Carry this task register into `.sdd/TASKS.md`
  with TASK-001 through TASK-009 marked done; status is tracked there from now
  on. Finish with `uv run --with pyyaml==6.0.2 python skills/tech-use-case-discovery/scripts/validate_config.py render --verify`.

## WI-004 — Create folders and non-programmatic dependencies

### TASK-011 — Create the approved project structure

- **Work Item:** WI-004
- **Status:** pending
- **Depends on:** TASK-010
- **Acceptance criteria:** AC-FR001-04
- **Action:** Create approved folders, configuration locations, documentation
  paths, environment templates, and other non-programmatic dependencies.

### TASK-012 — Verify non-programmatic dependencies

- **Work Item:** WI-004
- **Status:** pending
- **Depends on:** TASK-011
- **Acceptance criteria:** AC-FR001-04
- **Action:** Check that the structure matches PRODUCT.md and constitution.md
  without adding application source code.

## WI-005 — Set up the system environment

### TASK-013 — Implement the selected environment setup

- **Work Item:** WI-005
- **Status:** pending
- **Depends on:** TASK-012
- **Acceptance criteria:** AC-FR001-05
- **Action:** Configure the approved devcontainer, Docker, host-only, or
  explicitly no-container environment.

### TASK-014 — Run baseline environment checks

- **Work Item:** WI-005
- **Status:** pending
- **Depends on:** TASK-013
- **Acceptance criteria:** AC-FR001-05
- **Action:** Create the environment and run the documented baseline checks
  without committing secrets.

## WI-006 — Automate environment reproduction

### TASK-015 — Create initialization automation

- **Work Item:** WI-006
- **Status:** pending
- **Depends on:** TASK-014
- **Acceptance criteria:** AC-FR001-06
- **Action:** Create `scripts/init.sh` or the approved equivalent to reproduce
  the environment from a clean checkout. Wire these checks into the fork's
  pre-commit hook (the configured `quality.commit_hook`) and add them as
  steps to the inherited `.github/workflows/validators.yml`, keeping its
  template sample and test steps, so `docs/PRODUCT.md`, `config.yaml`, and
  `.sdd/constitution.md` cannot drift after initialization:
  - `python skills/tech-use-case-discovery/scripts/validate_discovery.py docs/PRODUCT.md`
  - `uv run --with pyyaml==6.0.2 python skills/tech-use-case-discovery/scripts/validate_config.py check`
  - `uv run --with pyyaml==6.0.2 python skills/tech-use-case-discovery/scripts/validate_config.py render --verify`

  Show that a hand edit to `.sdd/constitution.md` fails the hook.

### TASK-016 — Verify reproducibility and document recovery

- **Work Item:** WI-006
- **Status:** pending
- **Depends on:** TASK-015
- **Acceptance criteria:** AC-FR001-06
- **Action:** Re-run initialization, verify actionable failures, and document
  the recovery/reproduction procedure for contributors.
