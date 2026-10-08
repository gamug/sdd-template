# Implementation Plan

## FR-001 — Discover and initialize the project

FR-001 is the only functional requirement. It is fulfilled by completing
WI-001 through WI-006 in order. The project remains intentionally undefined
until discovery produces `docs/PRODUCT.md`.

## Work items

### WI-001 — Run the discovery skill and create PRODUCT.md

**Parent:** FR-001  
**Depends on:** none

Run [`skills/tech-use-case-discovery/SKILL.md`](../../skills/tech-use-case-discovery/SKILL.md)
through all six phases. Collect the user's problem definition, actors,
workflows, requirements, user stories, stack evaluation, ADRs, environment
decisions, risks, and roadmap in `docs/PRODUCT.md`.

The skill must ask focused questions interactively. It must not guess missing
inputs. When an answer is required, the question must state what decision is
needed, why it affects the project, and what concrete options or examples the
user should consider.

**Exit criteria:** `docs/PRODUCT.md` exists, contains the complete discovery
package, and unresolved decisions are clearly marked for user approval.

### WI-002 — Create config.yaml

**Parent:** FR-001  
**Depends on:** WI-001

Create root `config.yaml` from `constitution.yaml.example` using only the
approved decisions in `docs/PRODUCT.md`. For every missing value, ask a clear,
context-rich question before writing the field. Do not infer or silently retain
an example value.

**Exit criteria:** `config.yaml` contains approved project values and
each non-obvious value can be traced to `docs/PRODUCT.md` or an explicit user
decision.

### WI-003 — Render constitution.md and synchronize SDD objects

**Parent:** FR-001  
**Depends on:** WI-002

Use root `config.yaml` and the approved `docs/PRODUCT.md` decisions to create
`.sdd/constitution.md` from the immutable `.specify/memory/constitution.md`
template. Any pending input must be presented as a
clear question with the decision context, impact, and acceptable answer
format; it must never be guessed.

Then create or update all SDD objects under `.sdd/`—`SPEC.md`, `PLAN.md`,
`TASKS.md`, and the constitution—to match the approved `docs/PRODUCT.md` definition while
preserving the `FR > WI > Task` hierarchy and traceability.

**Exit criteria:** The constitution and all SDD objects agree with
`docs/PRODUCT.md`, contain no unresolved placeholders, and record any
remaining user decisions explicitly.

### WI-004 — Create folders and non-programmatic dependencies

**Parent:** FR-001  
**Depends on:** WI-003

Create the directories, configuration locations, documentation locations,
environment templates, container metadata, and other non-programmatic
dependencies selected in `docs/PRODUCT.md`. Do not implement application
source code in this WI.

**Exit criteria:** Required non-programmatic project structure exists and
matches the approved constitution and PRODUCT definition.

### WI-005 — Set up the system environment

**Parent:** FR-001  
**Depends on:** WI-004

Set up the development environment using the approach selected in
`docs/PRODUCT.md`: devcontainer, Docker, host tooling, or an explicitly
approved no-container setup. Configure runtimes, package managers, services,
environment variables, quality tools, and CI prerequisites as applicable.

**Exit criteria:** The selected environment can be created and the documented
baseline checks can run without committed secrets.

### WI-006 — Automate environment reproduction

**Parent:** FR-001  
**Depends on:** WI-005

Create the automation needed to reproduce the environment setup from a clean
checkout. Prefer `scripts/init.sh` when compatible with the approved
environment; otherwise use the project-appropriate equivalent and document why.

**Exit criteria:** Re-running the initialization automation produces the
documented environment or reports actionable errors, and the procedure is
documented for contributors.

## Planning rules

- `TASKS.md` must contain the tasks for these Work Items, with one explicit
  parent WI per task.
- Work Items and tasks must be completed in dependency order.
- Material ambiguity is a question for the user, not an implementation guess.
