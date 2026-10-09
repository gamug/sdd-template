# Implementation Plan

## FR-001 — Discover and initialize the project

FR-001 is the only functional requirement. It is fulfilled by completing
WI-001 through WI-006 in order. The project remains intentionally undefined
until discovery produces `docs/PRODUCT.md`.

### Acceptance criteria

The acceptance criteria `AC-FR001-01` through `AC-FR001-06` are defined in
[`SPEC.md`](./SPEC.md#acceptance-criteria). Each Work Item below names the
criterion it satisfies.

## Work items

### WI-001 — Run the discovery skill and create PRODUCT.md

**Parent:** FR-001  
**Depends on:** none
**Acceptance criteria:** AC-FR001-01

Run [`skills/tech-use-case-discovery/SKILL.md`](../../skills/tech-use-case-discovery/SKILL.md)
through all six phases. Collect the user's problem definition, actors,
workflows, requirements, user stories, stack evaluation, ADRs, environment and
governance decisions, risks, and roadmap in `docs/PRODUCT.md`, built from the
skill's `templates/product-template.md`. Discovery runs first: no other FR-001 work starts before it, and `validate_config.py` refuses
to run until `docs/PRODUCT.md` is approved.

The skill must ask focused questions interactively. It must not guess missing
inputs. When an answer is required, the question must state what decision is
needed, why it affects the project, and what concrete options or examples the
user should consider.

**Exit criteria:** Every `UNRESOLVED:` decision has been resolved with the
user, `docs/PRODUCT.md` records the user's approval and the hash of the
approved content in its `## Approval` section, and
`validate_discovery.py docs/PRODUCT.md` passes without `--draft`.

### WI-002 — Create config.yaml

**Parent:** FR-001  
**Depends on:** WI-001 (approved `docs/PRODUCT.md`)
**Acceptance criteria:** AC-FR001-02

Build root `config.yaml` from scratch with `uv run --with-requirements skills/tech-use-case-discovery/scripts/requirements.txt python skills/tech-use-case-discovery/scripts/validate_config.py scaffold`, which lists
every key required by the generic `.specify/memory/constitution.md` template
and the PRODUCT.md section each one usually comes from.

1. Fill values that `docs/PRODUCT.md` states explicitly, with source
   `PRODUCT.md § <section>`. The cited section must have no subsections and
   contain each value (every item, for lists and maps) as a whole token.
2. Define the project's domain sections (`domain_sections`) from the use
   cases, requirements, ADRs, and risks, and confirm them with the user. The
   template carries no domain rules of its own. Their source is always
   `user, YYYY-MM-DD`.
3. Ask the user for every other value. A value PRODUCT.md only implies is
   proposed and confirmed, never written silently. Record answers with source
   `user, YYYY-MM-DD`.

Every value and its source is recorded in the `Configuration Decisions` table
of `docs/PRODUCT.md`. `uv run --with-requirements skills/tech-use-case-discovery/scripts/requirements.txt python skills/tech-use-case-discovery/scripts/validate_config.py check` must pass.

**Exit criteria:** `check` passes: every key is defined and has a recorded
source matching its value.

### WI-003 — Render constitution.md and synchronize SDD objects

**Parent:** FR-001  
**Depends on:** WI-002
**Acceptance criteria:** AC-FR001-03

Render `.sdd/constitution.md` from root `config.yaml` and the immutable
`.specify/memory/constitution.md` template with `uv run --with-requirements skills/tech-use-case-discovery/scripts/requirements.txt python skills/tech-use-case-discovery/scripts/validate_config.py render`. Rendering
re-runs `check` and fails on any missing value or leftover placeholder; no
questions are asked in this WI. The rendered file is never edited by hand:
any later `config.yaml` change updates its `Configuration Decisions` row and
re-runs `render`.

Then create or update all SDD objects under `.sdd/`—`SPEC.md`, `PLAN.md`,
`TASKS.md`, and `CHANGELOG.md`—to match the approved `docs/PRODUCT.md`
definition while preserving the `FR > WI > Task` hierarchy and traceability.
`FR-001` stays the initialization requirement; product requirements are
numbered from `FR-002`. Task status starts being tracked in `.sdd/TASKS.md`
here, with the tasks completed so far marked done.

**Exit criteria:** `uv run --with-requirements skills/tech-use-case-discovery/scripts/requirements.txt python skills/tech-use-case-discovery/scripts/validate_config.py render --verify` passes, and all SDD objects agree
with `docs/PRODUCT.md`.

### WI-004 — Create folders and non-programmatic dependencies

**Parent:** FR-001  
**Depends on:** WI-003
**Acceptance criteria:** AC-FR001-04

Create the directories, configuration locations, documentation locations,
environment templates, container metadata, and other non-programmatic
dependencies selected in `docs/PRODUCT.md`. Do not implement application
source code in this WI.

**Exit criteria:** Required non-programmatic project structure exists and
matches the approved constitution and PRODUCT definition.

### WI-005 — Set up the system environment

**Parent:** FR-001  
**Depends on:** WI-004
**Acceptance criteria:** AC-FR001-05

Set up the development environment using the approach selected in
`docs/PRODUCT.md`: devcontainer, Docker, host tooling, or an explicitly
approved no-container setup. Configure runtimes, package managers, services,
environment variables, quality tools, and CI prerequisites as applicable.

**Exit criteria:** The selected environment can be created and the documented
baseline checks can run without committed secrets.

### WI-006 — Automate environment reproduction

**Parent:** FR-001  
**Depends on:** WI-005
**Acceptance criteria:** AC-FR001-06

Create the automation needed to reproduce the environment setup from a clean
checkout. Prefer `scripts/init.sh` when compatible with the approved
environment; otherwise use the project-appropriate equivalent and document why.
Add the initialization checks (`validate_discovery.py`, `validate_config.py
check`, and `validate_config.py render --verify`) to the fork's pre-commit
hook and as steps in `.github/workflows/validators.yml`, so the rendered
constitution stays in sync after WI-003.

**Exit criteria:** Re-running the initialization automation produces the
documented environment or reports actionable errors, the procedure is
documented for contributors, and pre-commit and CI fail when
`docs/PRODUCT.md`, `config.yaml`, or `.sdd/constitution.md` drift.

## Planning rules

- `TASKS.md` must contain the tasks for these Work Items, with one explicit
  parent WI per task.
- Work Items and tasks must be completed in dependency order.
- Material ambiguity is a question for the user, not an implementation guess.
