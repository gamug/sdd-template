# SDD Template

A reusable starting point for repositories built with
**Specification-Driven Development (SDD)**.

This repository is designed to be forked. It provides a constitution template,
a configuration example, a discovery skill, and the SDD artifacts that keep
requirements, design, implementation, and verification aligned. It is not a
finished application. The values in
[`constitution.yaml.example`](./constitution.yaml.example) are examples and
must be replaced during project initialization.

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
├── constitution.yaml.example       # Starting point for root config.yaml
├── .specify/
│   ├── scripts/
│   │   └── validate_config.py      # Config consistency checks
│   └── memory/
│       ├── constitution.md         # Immutable constitution template
│       ├── SPEC.md                 # Initial specification template
│       ├── PLAN.md                 # Initial FR/WI plan
│       ├── TASKS.md                # Initial task register
│       └── CHANGELOG.md            # Changelog usage placeholder
├── skills/
│   └── tech-use-case-discovery/    # Required discovery workflow
├── docs/                           # Product discovery output location
└── README.md
```

The constitution template uses `{{ ... }}` placeholders for scalar values and
`{{#each ...}}` blocks for collections. Rendering must fail when a required
value is missing.

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

### WI-001: discover the use case

Run [`skills/tech-use-case-discovery/SKILL.md`](./skills/tech-use-case-discovery/SKILL.md)
through all six phases. The skill guides the user through:

- use-case definition and stakeholders;
- requirements and user stories;
- technology-stack evaluation;
- architecture decision records;
- development-environment decisions; and
- risks, validation, and roadmap.

The output is `docs/PRODUCT.md`. The skill must ask focused questions and must
not invent missing product, technical, or operational decisions.

### WI-002: create the configuration

Copy the example to the authoritative root configuration:

```powershell
Copy-Item constitution.yaml.example config.yaml
```

Replace every example value with an approved decision from
`docs/PRODUCT.md`. Validate every required field and ask the user about
missing or ambiguous values before writing them.

Check that related values have not drifted apart:

```bash
uv run --with pyyaml python .specify/scripts/validate_config.py config.yaml
```

### WI-003: create the canonical SDD objects

Use root `config.yaml` and the immutable template constitution to create:

```text
.sdd/constitution.md
.sdd/SPEC.md
.sdd/PLAN.md
.sdd/TASKS.md
.sdd/CHANGELOG.md
```

Synchronize the objects with `docs/PRODUCT.md`. Preserve the `FR > WI > Task`
hierarchy, acceptance-criteria traceability, and explicit unresolved decisions.
Do not modify the template inputs in `.specify/memory/`.

### WI-004 through WI-006: prepare and reproduce the environment

Create the approved folders and non-programmatic dependencies in WI-004. Set
up the approved devcontainer, Docker, host-only, or no-container environment
in WI-005. In WI-006, create `scripts/init.sh` or the approved equivalent so
the environment can be reproduced from a clean checkout.

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

Do not create `config.yaml` or application source code manually before the
agent starts. The initial tasks define when those files are created. The
runtime, package manager, container tooling, and other project prerequisites
are discovered and configured by WI-001 through WI-006.

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
before proceeding to WI-002. Do not skip tasks, invent unresolved decisions,
or implement application code before the plan allows it.

After each task:
- update its status and the parent Work Item status;
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
2. Execute WI-002 to create root `config.yaml` from
   [`constitution.yaml.example`](./constitution.yaml.example), replacing
   example values only with approved decisions.
3. Execute WI-003 to create `.sdd/constitution.md`, `.sdd/SPEC.md`,
   `.sdd/PLAN.md`, `.sdd/TASKS.md`, and `.sdd/CHANGELOG.md`.
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
6. Update affected SDD and architecture artifacts.
7. Move completed work to `.sdd/CHANGELOG.md`.

Every production code commit must use Conventional Commits and include the
traceability suffix required by the constitution:

```text
type(scope): imperative summary [FR-001][WI-002][TASK-004]
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

## Commands and environment

The rendered constitution's configured package manager is the only supported
way to run dependency, test, lint, formatting, type-checking, and operational
commands. The concrete commands belong to the fork's `config.yaml`; do not
copy example commands without reviewing them.

Keep real environment files out of Git:

- commit placeholder values only in environment examples;
- never commit secrets; and
- reproduce setup through the approved initialization script or equivalent.

## License and ownership

Add the license, maintainers, contribution process, and support policy for the
forked project. This template does not assume that those policies are shared
by every downstream repository.
