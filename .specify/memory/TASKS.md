# SDD Tasks

Task register for the hierarchy `FR-001 > WI > Task` defined in
[`PLAN.md`](./PLAN.md). Every task has exactly one parent Work Item.

## WI-001 — Run the discovery skill and create PRODUCT.md

### TASK-001 — Execute the discovery workflow

- **Work Item:** WI-001
- **Status:** pending
- **Depends on:** none
- **Acceptance criteria:** AC-FR001-01
- **Action:** Run all six phases of `skills/tech-use-case-discovery/SKILL.md`.

### TASK-002 — Collect discovery outputs

- **Work Item:** WI-001
- **Status:** pending
- **Depends on:** TASK-001
- **Acceptance criteria:** AC-FR001-01
- **Action:** Assemble use cases, requirements, user stories, stack evaluation,
  ADRs, environment decisions, risks, and roadmap.

### TASK-003 — Write and validate PRODUCT.md

- **Work Item:** WI-001
- **Status:** pending
- **Depends on:** TASK-002
- **Acceptance criteria:** AC-FR001-01
- **Action:** Write `docs/PRODUCT.md`, mark unresolved decisions, and run the
  skill validation script against the discovery package.

## WI-002 — Create config.yaml

### TASK-004 — Map approved PRODUCT decisions to YAML

- **Work Item:** WI-002
- **Status:** pending
- **Depends on:** TASK-003
- **Acceptance criteria:** AC-FR001-02
- **Action:** Copy `constitution.yaml.example` to root `config.yaml` and map
  only approved values from `docs/PRODUCT.md`.

### TASK-005 — Resolve missing YAML inputs explicitly

- **Work Item:** WI-002
- **Status:** pending
- **Depends on:** TASK-004
- **Acceptance criteria:** AC-FR001-02
- **Action:** Ask context-rich questions for every missing or ambiguous value;
  do not guess or silently retain example values.

### TASK-006 — Validate config.yaml

- **Work Item:** WI-002
- **Status:** pending
- **Depends on:** TASK-005
- **Acceptance criteria:** AC-FR001-02
- **Action:** Validate required fields in `config.yaml` and trace each non-obvious value to
  PRODUCT.md or an explicit user decision. Run
  `uv run --with pyyaml python .specify/scripts/validate_config.py config.yaml`
  so related values, such as `runtime.version` and `devcontainer.image`,
  cannot drift.

## WI-003 — Render constitution.md and synchronize SDD objects

### TASK-007 — Render constitution.md

- **Work Item:** WI-003
- **Status:** pending
- **Depends on:** TASK-006
- **Acceptance criteria:** AC-FR001-03
- **Action:** Render `.sdd/constitution.md` from root `config.yaml` and the
  immutable `.specify/memory/constitution.md` template, asking clear
  questions instead of guessing pending inputs.

### TASK-008 — Synchronize all SDD objects

- **Work Item:** WI-003
- **Status:** pending
- **Depends on:** TASK-007
- **Acceptance criteria:** AC-FR001-03
- **Action:** Create or update `.sdd/SPEC.md`, `.sdd/PLAN.md`, `.sdd/TASKS.md`,
  and `.sdd/constitution.md` to match the approved PRODUCT.md definition and
  preserve traceability.

## WI-004 — Create folders and non-programmatic dependencies

### TASK-009 — Create the approved project structure

- **Work Item:** WI-004
- **Status:** pending
- **Depends on:** TASK-008
- **Acceptance criteria:** AC-FR001-04
- **Action:** Create approved folders, configuration locations, documentation
  paths, environment templates, and other non-programmatic dependencies.

### TASK-010 — Verify non-programmatic dependencies

- **Work Item:** WI-004
- **Status:** pending
- **Depends on:** TASK-009
- **Acceptance criteria:** AC-FR001-04
- **Action:** Check that the structure matches PRODUCT.md and constitution.md
  without adding application source code.

## WI-005 — Set up the system environment

### TASK-011 — Implement the selected environment setup

- **Work Item:** WI-005
- **Status:** pending
- **Depends on:** TASK-010
- **Acceptance criteria:** AC-FR001-05
- **Action:** Configure the approved devcontainer, Docker, host-only, or
  explicitly no-container environment.

### TASK-012 — Run baseline environment checks

- **Work Item:** WI-005
- **Status:** pending
- **Depends on:** TASK-011
- **Acceptance criteria:** AC-FR001-05
- **Action:** Create the environment and run the documented baseline checks
  without committing secrets.

## WI-006 — Automate environment reproduction

### TASK-013 — Create initialization automation

- **Work Item:** WI-006
- **Status:** pending
- **Depends on:** TASK-012
- **Acceptance criteria:** AC-FR001-06
- **Action:** Create `scripts/init.sh` or the approved equivalent to reproduce
  the environment from a clean checkout.

### TASK-014 — Verify reproducibility and document recovery

- **Work Item:** WI-006
- **Status:** pending
- **Depends on:** TASK-013
- **Acceptance criteria:** AC-FR001-06
- **Action:** Re-run initialization, verify actionable failures, and document
  the recovery/reproduction procedure for contributors.
