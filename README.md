# SDD Template

A reusable starting point for repositories built with **Specification-Driven Development (SDD)**.

This repository is designed to be forked. It provides a constitution template, a configuration builder, a discovery skill, and the SDD artifacts that keep requirements, design, implementation, and verification aligned. It is not a finished application. The project configuration is built from scratch during initialization from the keys the constitution template requires.

## Repository philosophy

The template is based on these principles:

- **The constitution is the governing contract.** It defines the architectural, operational, quality, AI/data, and Git guarantees for a project.
- **Specifications precede implementation.** Requirements belong in the specification before code relies on them. Plans describe architecture, risks, verification, rollout, and rollback. Tasks make the work executable and traceable.
- **The hierarchy is strict:** `FR > WI > Task`. Every Work Item belongs to a functional requirement, and every task belongs to exactly one Work Item.
- **Skills and SDD objects guide the work.** The repository uses the skill files and task register as its operating procedure; ad-hoc planning prompts are not a substitute for them.
- **Decisions are explicit and reviewable.** Missing or ambiguous information is recorded as a question for the user, never guessed.
- **Reproducibility beats convenience.** Use the configured package manager and lockfile, keep one canonical configuration per tool, and run the same quality gates locally and in CI.
- **Forks specialize the template rather than weakening it.** Project choices must be reflected consistently in the configuration, rendered constitution, SDD artifacts, automation, and contributor documentation.

## What this repository contains

```text
.
├── skills/
│   └── sdd-init/                   # The whole template: one skill
│       ├── SKILL.md                # Discovery (phases 1-6) and initialization (WI-002..006)
│       ├── memory/                 # Immutable template inputs
│       │   ├── constitution.md     # Constitution template
│       │   ├── SPEC.md             # Initial specification template
│       │   ├── PLAN.md             # Initial FR/WI plan
│       │   ├── TASKS.md            # Initial task register
│       │   └── CHANGELOG.md        # Changelog usage placeholder
│       ├── references/             # One guide per discovery phase
│       ├── templates/              # product-template.md, per-phase fragments, adr-log-template.md (adr.md)
│       ├── examples/               # Approved sample discovery package
│       └── scripts/                # validate_discovery.py, validate_config.py, requirements.txt
├── tests/                          # Regression tests for the validators
├── .github/workflows/validators.yml  # Validates the sample, runs the tests (actions pinned to SHAs)
├── .github/dependabot.yml          # Proposes updates to the pinned actions and PyYAML
├── .github/CODEOWNERS              # Code owner of the template repository
├── docs/                           # Created by WI-001 (docs/PRODUCT.md)
├── adr.md                          # Created by WI-001: the live ADR record, seeded from docs/PRODUCT.md § 5
├── LICENSE                         # MIT license of the template and the skill
└── README.md
```

The constitution template uses `{{key}}` placeholders for scalar values, `{{#each key}}` blocks for collections, `{{#if key}}` blocks for optional content, and `{{!-- --}}` comments. `validate_config.py render` implements this subset and fails when a required value is missing.

The files under [`skills/sdd-init/memory/`](./skills/sdd-init/memory/) are immutable template inputs. After discovery, root `config.yaml` becomes the authoritative normalized configuration. WI-003 creates the canonical project artifacts under `.sdd/`.

## Initial SDD workflow

The initial project setup is already modeled as one functional requirement and six Work Items:

```text
FR-001 — Discover and initialize the project
├── WI-001 — Run the discovery skill and create docs/PRODUCT.md
├── WI-002 — Create root config.yaml
├── WI-003 — Create .sdd/constitution.md and synchronize SDD objects
├── WI-004 — Create folders and non-programmatic dependencies
├── WI-005 — Set up the system environment
└── WI-006 — Automate environment reproduction
```

The complete definitions and dependencies are in [`skills/sdd-init/memory/PLAN.md`](./skills/sdd-init/memory/PLAN.md), and the executable task register is in [`skills/sdd-init/memory/TASKS.md`](./skills/sdd-init/memory/TASKS.md). Complete the tasks in dependency order.

### Running the tooling

`validate_config.py` needs the PyYAML version pinned in `skills/sdd-init/scripts/requirements.txt`. Run it from the repository root as:

```bash
uv run --with-requirements skills/sdd-init/scripts/requirements.txt python skills/sdd-init/scripts/validate_config.py <mode>
```

Everywhere else in this repository, `validate_config.py <mode>` (for example `validate_config.py check`) stands for this command. `validate_discovery.py` needs only the standard library and runs with plain `python`.

### WI-001: discover the use case

Discovery always runs first. Run [`skills/sdd-init/SKILL.md`](./skills/sdd-init/SKILL.md) through all six phases. The skill guides the user through:

- use-case definition and stakeholders;
- requirements and user stories;
- technology-stack evaluation;
- architecture decision records;
- development-environment, governance, and workflow decisions; and
- risks, validation, and roadmap.

The output is `docs/PRODUCT.md`, built from the skill's [`product-template.md`](./skills/sdd-init/templates/product-template.md) with three-digit IDs (`UC-001`, `FR-002`, …), and the root `adr.md`, seeded in Phase 4 from the ADRs in `docs/PRODUCT.md` section 5 with the skill's [`adr-log-template.md`](./skills/sdd-init/templates/adr-log-template.md). The skill must ask focused questions and must not invent missing product, technical, or operational decisions. Open decisions are marked `UNRESOLVED:` and must all be resolved with the user, who then approves the document in its `## Approval` section. The approval records who, when it was first approved, when it was last approved, and a hash of the approved content:

```bash
python skills/sdd-init/scripts/validate_discovery.py --hash docs/PRODUCT.md
python skills/sdd-init/scripts/validate_discovery.py docs/PRODUCT.md
```

`validate_config.py` refuses to run until this passes. It does not check `adr.md`; accepting the seeded ADRs is a manual step before WI-002, described in Phase 6 step 5 of the skill. Editing `docs/PRODUCT.md` after approval, outside the Approval and Configuration Decisions sections, invalidates the approval until the user approves again. A re-approval updates `Approved on` and the hash but keeps `First approved on`, so configuration decisions recorded since the first approval stay valid.

### WI-002: create the configuration

Every placeholder in the constitution template is a decision the project must make. The skill's [Initialization Workflow](./skills/sdd-init/SKILL.md#wi-002-create-the-configuration) walks through `validate_config.py scaffold` and `check`: it builds root `config.yaml` and the `Configuration Decisions` table in `docs/PRODUCT.md`, recording the source of every value (`PRODUCT.md § <section>` or `user, YYYY-MM-DD`). Values PRODUCT.md only implies are proposed and confirmed with the user, never written silently.

### WI-003: render the constitution and create the SDD objects

`validate_config.py render` writes `.sdd/constitution.md` (never edit it by hand; `render --verify` fails when it is out of date). The remaining objects, `.sdd/SPEC.md`, `.sdd/PLAN.md`, `.sdd/TASKS.md` and `.sdd/CHANGELOG.md`, are created from `docs/PRODUCT.md`. Details are in the skill's [Initialization Workflow](./skills/sdd-init/SKILL.md#wi-003-render-the-constitution-and-create-the-sdd-objects).

### WI-004 through WI-006: prepare and reproduce the environment

Create the approved folders and non-programmatic dependencies in WI-004. Set up the approved devcontainer, Docker, host-only, or no-container environment in WI-005. In WI-006, create `scripts/init.sh` or the approved equivalent so the environment can be reproduced from a clean checkout, and add the initialization checks to the fork's pre-commit hook and CI (see [Ongoing development workflow](#ongoing-development-workflow)).

## Getting started after forking

This repository is an agent-guided initialization framework. A fork is not initialized by manually following a checklist alone; a coding agent must read the SDD artifacts, execute the tasks, update the artifacts, and ask for human decisions when the workflow reaches an unresolved input.

### Prerequisites

Before starting the agent, prepare:

1. A fork of this repository with a clean Git working tree and permission to create branches and commits.
2. A coding-agent framework installed and authenticated. Supported examples include:
   - **GitHub Copilot**, using the Copilot SDK agent workflow;
   - **Claude Code**;
   - **OpenAI Codex**; or
   - another framework that can read and edit repository files, run shell commands, and report results.
3. The agent's workspace set to the root of the fork, with access to the repository's terminal and Git history.
4. Any framework-specific configuration required to allow file edits, command execution, and human approval for consequential actions.
5. Access to the user who will answer discovery questions. The agent must not invent answers when the project has not yet defined its use case.
6. Python 3.10 or later and [`uv`](https://docs.astral.sh/uv/) on the host. The initialization tooling (`validate_discovery.py` and `validate_config.py`, which needs the PyYAML version pinned in `skills/sdd-init/scripts/requirements.txt`, installed by `uv run --with-requirements`) runs in WI-001 to WI-003, before the project's own environment exists.

Do not create `config.yaml` or application source code manually before the agent starts. The initial tasks define when those files are created. Apart from the initialization tooling above, the project's runtime, package manager, container tooling, and other prerequisites are discovered and configured by WI-001 through WI-006.

### Start the initialization agent

Launch the coding agent from the fork root and instruct it to execute the initial SDD plan. Use the equivalent action command or task instruction for the selected framework:

```text
Use the sdd-init skill (skills/sdd-init/SKILL.md) to initialize this project.
```

The text above is an execution instruction, not a brainstorming prompt. The skill, [`skills/sdd-init/memory/PLAN.md`](./skills/sdd-init/memory/PLAN.md), and [`skills/sdd-init/memory/TASKS.md`](./skills/sdd-init/memory/TASKS.md) contain the workflow the agent must follow.

### Agent initialization responsibilities

The agent must:

1. Execute WI-001 and use [`skills/sdd-init/SKILL.md`](./skills/sdd-init/SKILL.md) to create `docs/PRODUCT.md` and the root `adr.md`, and to accept the seeded ADRs once the user approves `docs/PRODUCT.md`.
2. Execute WI-002 to build root `config.yaml` with [`validate_config.py`](./skills/sdd-init/scripts/validate_config.py), recording the source of every value (`docs/PRODUCT.md` or an explicit user decision).
3. Execute WI-003 to render `.sdd/constitution.md` with `validate_config.py render` and create `.sdd/SPEC.md`, `.sdd/PLAN.md`, `.sdd/TASKS.md`, and `.sdd/CHANGELOG.md`.
4. Execute WI-004 through WI-006 to create the approved project structure, configure the environment, and automate its reproduction.
5. Validate each result, preserve task traceability, and leave a clear handoff when user input or external access blocks progress.

The user remains the decision authority. The agent may recommend options and perform approved changes, but it must not silently select the project's purpose, scope, stack, architecture, environment, or constitutional values.

### Upgrading a fork created before the rename

A fork initialized before the lowercase `adr` rename may still have `ADR.md`. Merge or close any open pull request that edits `ADR.md` first, or do the rename in a pull request of its own, because a rename conflicts with those edits.

1. Bring in the upstream template's changes first (for example `git fetch` the template repository and merge it), because the fork's own `skills/` files are the older versions. Before renaming, list what points at the old name with `git grep -l "ADR.md"`. Do not edit `.sdd/constitution.md` by hand: take the updated `skills/sdd-init/memory/constitution.md` from the upstream template, then run `validate_config.py render` and `render --verify` so the rendered file is regenerated. Update the references in `.sdd/SPEC.md`, `.sdd/PLAN.md`, `.sdd/TASKS.md`, and every other file the grep lists, such as `docs/PRODUCT.md`, `config.yaml`, and your templates. A change of file name alone does not normally need a constitution amendment; follow your own Governance section if it says otherwise.
2. Rename the file in two steps, because Windows and macOS treat `ADR.md` and `adr.md` as the same file: `git mv ADR.md adr.tmp && git mv adr.tmp adr.md`.
3. `adr-001` style IDs are matched case-insensitively, so existing `ADR-001` headings still validate. The validator now reports them as `adr-001`, so update any test of your own that asserts the old uppercase messages, such as `Duplicate ID definition(s): ADR-001`.

Until the rename is done, on a case-sensitive filesystem the docs and agents refer to a different file than the one you have.

## Ongoing development workflow

After initialization, every product change follows this cycle:

1. Update the relevant functional requirement in `.sdd/SPEC.md`.
2. Add or update a Work Item in `.sdd/PLAN.md`, including dependencies, acceptance criteria, architecture, risks, and verification.
3. Decompose the Work Item into traceable tasks in `.sdd/TASKS.md`.
4. Execute tasks in dependency order, using applicable skills.
5. Run the configured tests, linting, type checks, security scans, and other validation commands.
6. Update affected SDD and architecture artifacts. A change to `config.yaml` also updates its `Configuration Decisions` row and is followed by `validate_config.py render`; a change to the approved content of `docs/PRODUCT.md` needs the user's re-approval.
7. Check each completed task's box in `.sdd/TASKS.md` and, once all its tasks are checked, its Work Item's box; then move completed work to `.sdd/CHANGELOG.md`.

An architecture change (for example a new runtime version, framework, library, storage engine, API contract, or schema) also needs an ADR in `adr.md`, which the user accepts before the change is implemented; the constitution's "Architecture decisions" section has the rule. `docs/PRODUCT.md` section 5 stays a frozen discovery snapshot.

When a fork merges a template update that changes `skills/sdd-init/memory/constitution.md`, it must also re-run `validate_config.py render`, because `render --verify` fails while `.sdd/constitution.md` is out of date.

The validators, the template tests and the sample check prepare the repository; the pre-commit hook and CI that WI-006 configures run the project's own quality gates, not the skill's.

Every production code commit must use Conventional Commits and include the traceability suffix required by the constitution:

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
- Update documentation and architecture records (`adr.md`) when implementation changes their documented state.
- Never weaken a check, fabricate repository state, commit secrets, or hide a failure to make a change pass.
- Write Markdown with one paragraph or list item per line; do not hard-wrap at a column. This is a template-maintenance rule: `tests/test_markdown_format.py` enforces it in CI for the tracked `.md` files, and a fork that keeps `tests/` inherits it. The constitution does not impose it on projects.
- Write ADR in uppercase in Markdown prose and headings; keep `adr` lowercase in filenames (`adr.md`), IDs (`adr-001`), and code identifiers. `tests/test_markdown_format.py` flags a lowercase `adr` in the tracked `.md` prose; the validator messages are covered by the assertions in `tests/test_validate_discovery.py`.

Commits that maintain this template itself (validators, skill, docs, tests) use plain Conventional Commits, `type(scope): summary`, without the `[FR][WI][TASK]` suffix. That suffix traces a fork's FR-001 initialization and product work, and template maintenance is not part of it.

## Commands and environment

The rendered constitution's configured package manager is the only supported way to run dependency, test, lint, formatting, type-checking, and operational commands. The concrete commands belong to the fork's `config.yaml`.

Keep real environment files out of Git:

- commit placeholder values only in environment examples;
- never commit secrets; and
- reproduce setup through the approved initialization script or equivalent.

## Testing the template tooling

The tests live outside the skill: the skill ships only what a project needs to start, while `tests/` and `.github/workflows/validators.yml` maintain this template.

The validators carry a stdlib `unittest` regression suite under `tests/`. It also includes `test_markdown_format.py`, which fails on hard-wrapped Markdown. `.github/workflows/validators.yml` runs the suite on Python 3.10 and the latest Python for every pull request:

```bash
uv run --no-project --with-requirements skills/sdd-init/scripts/requirements.txt python -m unittest discover -s tests
```

## License and ownership

This template and the `sdd-init` skill are released under the [MIT License](./LICENSE). Copyright (c) 2026 Gabriel Jaime Múnera González. Contributions are accepted under the same license.

[@gamug](https://github.com/gamug) owns and maintains this template repository and is its code owner in [`.github/CODEOWNERS`](./.github/CODEOWNERS), which requests that review automatically on pull requests; it does not by itself block a merge.

To contribute, fork the repository, make the change on a branch in your fork, and open a pull request against `master`. Follow the [working agreement](#working-agreement-for-contributors-and-coding-agents), and make sure the CI checks pass. Issues are welcome for questions, bugs, and suggestions. There is no separate security channel: open an issue and leave exploit details out.

A fork keeps `LICENSE` and adds its own copyright line to it, and replaces `.github/CODEOWNERS` with its own owners. This section describes the template; a fork replaces it with its own.

Optional: a fork's own README may credit this template, for example "Built from [SDD Template](https://github.com/gamug/sdd-template) by Gabriel Jaime Múnera González". The MIT License only requires keeping the copyright notice; a citation is appreciated but not required.
