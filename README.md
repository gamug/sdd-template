# SDD Template

A reusable starting point for repositories built with
**Specification-Driven Development (SDD)**.

This repository is designed to be forked. It provides a constitution template,
a configuration builder, a discovery skill, and the SDD artifacts that keep
requirements, design, implementation, and verification aligned. It is not a
finished application. The project configuration is built from scratch during
initialization from the keys the constitution template requires.

## Repository philosophy

The template is based on these principles:

- **The constitution is the governing contract.** It defines the
  architectural, operational, quality, AI/data, and Git guarantees for a
  project.
- **Specifications precede implementation.** Requirements belong in the
  specification before code relies on them. Plans describe architecture,
  risks, verification, rollout, and rollback. Tasks make the work executable
  and traceable.
- **The hierarchy is strict:** `FR > WI > Task`. Every Work Item belongs to a
  functional requirement, and every task belongs to exactly one Work Item.
- **Skills and SDD objects guide the work.** The repository uses the skill
  files and task register as its operating procedure; ad-hoc planning prompts
  are not a substitute for them.
- **Decisions are explicit and reviewable.** Missing or ambiguous information
  is recorded as a question for the user, never guessed.
- **Reproducibility beats convenience.** Use the configured package manager
  and lockfile, keep one canonical configuration per tool, and run the same
  quality gates locally and in CI.
- **Forks specialize the template rather than weakening it.** Project choices
  must be reflected consistently in the configuration, rendered constitution,
  SDD artifacts, automation, and contributor documentation.

## What this repository contains

```text
.
├── .specify/
│   └── memory/
│       ├── constitution.md         # Immutable constitution template
│       ├── SPEC.md                 # Initial specification template
│       ├── PLAN.md                 # Initial FR/WI plan
│       ├── TASKS.md                # Initial task register
│       └── CHANGELOG.md            # Changelog usage placeholder
├── skills/
│   └── tech-use-case-discovery/    # Required discovery workflow
│       ├── SKILL.md                # Six-phase discovery workflow
│       ├── references/             # One guide per phase
│       ├── templates/              # product-template.md and per-phase fragments
│       ├── examples/               # Approved sample discovery package
│       └── scripts/                # validate_discovery.py, validate_config.py, requirements.txt
├── tests/                          # Regression tests for the validators
├── .github/workflows/validators.yml  # Validates the sample and runs the tests on pull requests and pushes to master (actions pinned to SHAs)
├── .github/dependabot.yml          # Proposes updates to the pinned actions and PyYAML
├── docs/                           # Created by WI-001 (docs/PRODUCT.md)
└── README.md
```

The constitution template uses `{{key}}` placeholders for scalar values,
`{{#each key}}` blocks for collections, `{{#if key}}` blocks for optional
content, and `{{!-- --}}` comments. `validate_config.py render` implements this
subset and fails when a required value is missing.

The files under [`.specify/memory/`](./.specify/memory/) are immutable template
inputs. After discovery, root `config.yaml` becomes the authoritative
normalized configuration. WI-003 creates the canonical project artifacts
under `.sdd/`.

## Initial SDD workflow

The initial project setup is already modeled as one functional requirement and
six Work Items:

```text
FR-001 — Discover and initialize the project
├── WI-001 — Run the discovery skill and create docs/PRODUCT.md
├── WI-002 — Create root config.yaml
├── WI-003 — Create .sdd/constitution.md and synchronize SDD objects
├── WI-004 — Create folders and non-programmatic dependencies
├── WI-005 — Set up the system environment
└── WI-006 — Automate environment reproduction
```

The complete definitions and dependencies are in
[`.specify/memory/PLAN.md`](./.specify/memory/PLAN.md), and the executable
task register is in [`.specify/memory/TASKS.md`](./.specify/memory/TASKS.md).
Complete the tasks in dependency order.

### Running the tooling

`validate_config.py` needs the PyYAML version pinned in
`skills/tech-use-case-discovery/scripts/requirements.txt`. Run it from the
repository root as:

```bash
uv run --with-requirements skills/tech-use-case-discovery/scripts/requirements.txt python skills/tech-use-case-discovery/scripts/validate_config.py <mode>
```

Everywhere else in this repository, `validate_config.py <mode>` (for example
`validate_config.py check`) stands for this command. `validate_discovery.py`
needs only the standard library and runs with plain `python`.

### WI-001: discover the use case

Discovery always runs first. Run
[`skills/tech-use-case-discovery/SKILL.md`](./skills/tech-use-case-discovery/SKILL.md)
through all six phases. The skill guides the user through:

- use-case definition and stakeholders;
- requirements and user stories;
- technology-stack evaluation;
- architecture decision records;
- development-environment, governance, and workflow decisions; and
- risks, validation, and roadmap.

The output is `docs/PRODUCT.md`, built from the skill's
[`product-template.md`](./skills/tech-use-case-discovery/templates/product-template.md)
with three-digit IDs (`UC-001`, `FR-002`, …). The skill must ask focused questions and must
not invent missing product, technical, or operational decisions. Open
decisions are marked `UNRESOLVED:` and must all be resolved with the user,
who then approves the document in its `## Approval` section. The approval
records who, when it was first approved, when it was last approved, and a
hash of the approved content:

```bash
python skills/tech-use-case-discovery/scripts/validate_discovery.py --hash docs/PRODUCT.md
python skills/tech-use-case-discovery/scripts/validate_discovery.py docs/PRODUCT.md
```

`validate_config.py` refuses to run until this passes. Editing
`docs/PRODUCT.md` after approval, outside the Approval and Configuration
Decisions sections, invalidates the approval until the user approves again.
A re-approval updates `Approved on` and the hash but keeps
`First approved on`, so configuration decisions recorded since the first
approval stay valid.

### WI-002: create the configuration

The constitution template is generic. Every placeholder it contains is a
decision the project must make. Generate the root configuration skeleton:

```bash
validate_config.py scaffold
```

This writes `config.yaml`, with the PRODUCT.md section each key usually comes
from, and appends a `Configuration Decisions` table (key, value, source) to
`docs/PRODUCT.md`. Then:

1. Fill the values `docs/PRODUCT.md` states, with source
   `PRODUCT.md § <section>`. The cited section must exist and contain the
   value (every item, for lists and maps) as a whole token. Lists and maps
   are recorded as compact JSON, and `|` in a value is escaped as `\|`.
2. Define the project's domain sections (`domain_sections`: a `title` and
   `rules` each), such as models, services, storage, or evaluation, from the
   use cases, requirements, and ADRs, and confirm them with the user. Their
   source is always `user, YYYY-MM-DD`.
3. Ask the user for every other value, including the coding-agent instruction
   file (for example `CLAUDE.md`, `AGENTS.md`, or
   `.github/copilot-instructions.md`). Values PRODUCT.md only implies are
   proposed and confirmed, never written silently. Record answers with source
   `user, YYYY-MM-DD`.

```bash
validate_config.py check
```

The check fails on missing or empty keys, sources that are malformed or cite
a section that doesn't contain the value, `user` dates that are invalid, in
the future, or earlier than PRODUCT.md's `First approved on`, recorded values (including
collections) that differ from `config.yaml`, and malformed table rows. A cited
section must have no subsections, and the Approval and Configuration Decisions
sections are never evidence.
Values are read as written, so dates and versions such as `1.10` render
unchanged.

### WI-003: render the constitution and create the SDD objects

```bash
validate_config.py render
```

`render` re-runs `check`, then writes `.sdd/constitution.md` and fails on any
leftover placeholder. Never edit the rendered file by hand. After any
`config.yaml` change, update its `Configuration Decisions` row and render
again; `render --verify` fails when the file is out of date.

Then create the remaining canonical objects from `docs/PRODUCT.md`:

```text
.sdd/SPEC.md
.sdd/PLAN.md
.sdd/TASKS.md
.sdd/CHANGELOG.md
```

Preserve the `FR > WI > Task` hierarchy and acceptance-criteria traceability.
`FR-001` stays the initialization requirement, and product requirements are
numbered from `FR-002` (discovery rejects an `FR-001` row in `docs/PRODUCT.md`).
Do not modify the template inputs in `.specify/memory/`: task status is not
tracked before this step, and `.sdd/TASKS.md` starts tracking it with the
completed initialization tasks marked done.

### WI-004 through WI-006: prepare and reproduce the environment

Create the approved folders and non-programmatic dependencies in WI-004. Set
up the approved devcontainer, Docker, host-only, or no-container environment
in WI-005. In WI-006, create `scripts/init.sh` or the approved equivalent so
the environment can be reproduced from a clean checkout, and add the
initialization checks to the fork's pre-commit hook and CI (see
[Ongoing development workflow](#ongoing-development-workflow)).

## Getting started after forking

This repository is an agent-guided initialization framework. A fork is not
initialized by manually following a checklist alone; a coding agent must read
the SDD artifacts, execute the tasks, update the artifacts, and ask for human
decisions when the workflow reaches an unresolved input.

### Prerequisites

Before starting the agent, prepare:

1. A fork of this repository with a clean Git working tree and permission to
   create branches and commits.
2. A coding-agent framework installed and authenticated. Supported examples
   include:
   - **GitHub Copilot**, using the Copilot SDK agent workflow;
   - **Claude Code**;
   - **OpenAI Codex**; or
   - another framework that can read and edit repository files, run shell
     commands, and report results.
3. The agent's workspace set to the root of the fork, with access to the
   repository's terminal and Git history.
4. Any framework-specific configuration required to allow file edits,
   command execution, and human approval for consequential actions.
5. Access to the user who will answer discovery questions. The agent must not
   invent answers when the project has not yet defined its use case.
6. Python 3.10 or later and [`uv`](https://docs.astral.sh/uv/) on the host.
   The initialization tooling (`validate_discovery.py` and
   `validate_config.py`, which needs the PyYAML version pinned in
   `skills/tech-use-case-discovery/scripts/requirements.txt`, installed by
   `uv run --with-requirements`) runs in WI-001 to WI-003, before the
   project's own environment exists.

Do not create `config.yaml` or application source code manually before the
agent starts. The initial tasks define when those files are created. Apart
from the initialization tooling above, the project's runtime, package manager,
container tooling, and other prerequisites are discovered and configured by
WI-001 through WI-006.

### Start the initialization agent

Launch the coding agent from the fork root and instruct it to execute the
initial SDD plan. Use the equivalent action command or task instruction for
the selected framework:

```text
Act as the implementation agent for this SDD repository.

Read README.md, .specify/memory/constitution.md,
.specify/memory/SPEC.md, .specify/memory/PLAN.md,
.specify/memory/TASKS.md, and the skills available under skills/.

Start the development described in .specify/memory/PLAN.md. Execute the
tasks in .specify/memory/TASKS.md in dependency order, beginning with TASK-001
under WI-001. Run the tech-use-case-discovery skill and produce docs/PRODUCT.md
from its product template before proceeding to WI-002. Do not skip tasks, invent unresolved decisions,
or implement application code before the plan allows it.

After each task:
- from WI-003 on, update the task and Work Item status in .sdd/TASKS.md;
  before that, report progress in your handoff (status is not tracked
  before WI-003);
- record decisions and outputs in the required SDD artifact;
- run the relevant validation;
- report what changed and what evidence was produced.

When required information is missing, stop and ask one clear, context-rich
question explaining the decision, its impact, and the acceptable answers.
Continue only after the user resolves it. Preserve the FR > WI > Task
hierarchy and do not modify the immutable .specify/memory/ templates.
```

The text above is an execution instruction, not a brainstorming prompt. The
skill, [`.specify/memory/PLAN.md`](./.specify/memory/PLAN.md), and
[`.specify/memory/TASKS.md`](./.specify/memory/TASKS.md) contain the workflow
the agent must follow.

### Agent initialization responsibilities

The agent must:

1. Execute WI-001 and use
   [`skills/tech-use-case-discovery/SKILL.md`](./skills/tech-use-case-discovery/SKILL.md)
   to create `docs/PRODUCT.md`.
2. Execute WI-002 to build root `config.yaml` with
   [`validate_config.py`](./skills/tech-use-case-discovery/scripts/validate_config.py), recording the source of every
   value (`docs/PRODUCT.md` or an explicit user decision).
3. Execute WI-003 to render `.sdd/constitution.md` with
   `validate_config.py render` and create `.sdd/SPEC.md`, `.sdd/PLAN.md`,
   `.sdd/TASKS.md`, and `.sdd/CHANGELOG.md`.
4. Execute WI-004 through WI-006 to create the approved project structure,
   configure the environment, and automate its reproduction.
5. Validate each result, preserve task traceability, and leave a clear
   handoff when user input or external access blocks progress.

The user remains the decision authority. The agent may recommend options and
perform approved changes, but it must not silently select the project's
purpose, scope, stack, architecture, environment, or constitutional values.

## Ongoing development workflow

After initialization, every product change follows this cycle:

1. Update the relevant functional requirement in `.sdd/SPEC.md`.
2. Add or update a Work Item in `.sdd/PLAN.md`, including dependencies,
   acceptance criteria, architecture, risks, and verification.
3. Decompose the Work Item into traceable tasks in `.sdd/TASKS.md`.
4. Execute tasks in dependency order, using applicable skills.
5. Run the configured tests, linting, type checks, security scans, and other
   validation commands.
6. Update affected SDD and architecture artifacts. A change to
   `config.yaml` also updates its `Configuration Decisions` row and is
   followed by `validate_config.py render`; a change to the approved
   content of `docs/PRODUCT.md` needs the user's re-approval.
7. Move completed work to `.sdd/CHANGELOG.md`.

The pre-commit hook and the steps WI-006 adds to
`.github/workflows/validators.yml` run the initialization checks on every
change, so these artifacts cannot drift silently:

```bash
python skills/tech-use-case-discovery/scripts/validate_discovery.py docs/PRODUCT.md
validate_config.py check
validate_config.py render --verify
```

Every production code commit must use Conventional Commits and include the
traceability suffix required by the constitution:

```text
type(scope): imperative summary [FR-001][WI-002][TASK-005]
```

## Working agreement for contributors and coding agents

Before changing a fork:

- Read the rendered constitution and current `.sdd/SPEC.md`.
- Inspect `.sdd/PLAN.md` and `.sdd/TASKS.md` before creating work.
- Check branch freshness and worktree state.
- Match existing placement, naming, bootstrap, and configuration patterns.
- Prefer the smallest complete change and avoid unrelated refactors.
- Obtain approval before expanding scope covered by the constitution.
- Update documentation and architecture records when implementation changes
  their documented state.
- Never weaken a check, fabricate repository state, commit secrets, or hide a
  failure to make a change pass.

Commits that maintain this template itself (validators, skill, docs, tests)
use plain Conventional Commits, `type(scope): summary`, without the
`[FR][WI][TASK]` suffix. That suffix traces a fork's FR-001 initialization
and product work, and template maintenance is not part of it.

## Commands and environment

The rendered constitution's configured package manager is the only supported
way to run dependency, test, lint, formatting, type-checking, and operational
commands. The concrete commands belong to the fork's `config.yaml`.

Keep real environment files out of Git:

- commit placeholder values only in environment examples;
- never commit secrets; and
- reproduce setup through the approved initialization script or equivalent.

## Testing the template tooling

The validators carry a stdlib `unittest` regression suite under `tests/`,
which `.github/workflows/validators.yml` runs on Python 3.10 and the latest
Python for every pull request:

```bash
uv run --no-project --with-requirements skills/tech-use-case-discovery/scripts/requirements.txt python -m unittest discover -s tests
```

## License and ownership

Add the license, maintainers, contribution process, and support policy for the
forked project. This template does not assume that those policies are shared
by every downstream repository.
