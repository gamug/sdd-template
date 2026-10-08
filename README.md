# SDD Template

A reusable starting point for repositories built with **Specification-Driven
Development (SDD)**.

This repository is designed to be forked. It provides a project constitution
template, a structured YAML configuration example, and a place for the SDD
artifacts that keep requirements, design, implementation, and verification
aligned. It is not a finished application and the values in
[`constitution.yaml.example`](./constitution.yaml.example) describe one
possible project rather than defaults that every fork must keep.

## Repository philosophy

The template is based on a few non-negotiable ideas:

- **The constitution is the governing contract.** It defines the architectural,
  operational, quality, AI/data, and Git guarantees for a project. When an
  ad-hoc convention conflicts with it, the constitution wins.
- **Specifications precede implementation.** Required behavior belongs in the
  specification before code relies on it. The plan describes architecture,
  risks, verification, rollout, and rollback; tasks make the work traceable.
- **Changes are explicit and reviewable.** Ambiguity, scope expansion, schema
  changes, dependency changes, model changes, and changes to documented
  guarantees must be resolved in the SDD artifacts and reviewed through the
  normal pull-request path.
- **Reliability is part of the design.** Public contracts define inputs,
  outputs, errors, compatibility, and ownership. External inputs are validated,
  failures are observable, and errors are not silently turned into successful
  results.
- **Reproducibility beats convenience.** Use the configured package manager and
  lockfile, keep one canonical configuration per tool, pin model and dependency
  choices where required, and run the same quality gates locally and in CI.
- **Forks specialize the template rather than weakening it.** A fork may choose
  a different runtime, layout, framework, or domain, but those choices should
  be recorded in the project configuration and reflected consistently in the
  rendered constitution, SDD artifacts, automation, and contributor
  documentation.

## What this repository contains

```text
.
├── constitution.yaml.example       # Fork-specific values and project shape
├── .specify/
│   └── memory/
│       └── constitution.md         # Reusable constitution template
├── .env.example                    # Placeholder environment variables
└── README.md
```

The constitution template uses `{{ ... }}` placeholders for scalar values and
`{{#each ...}}` blocks for collections. Rendering is expected to fail when a
required value is missing. The YAML file is intentionally named
`constitution.yaml.example` so a fork can create its own project-specific
configuration without treating this example as authoritative runtime
configuration.

## SDD artifact workflow

The recommended lifecycle is:

1. **Fork and identify the project.** Rename the project, select its runtime
   and package manager, define the source/test/docs layout, and remove
   components the project will not use.
2. **Discover the use case with an AI assistant.** Hold a structured
   brainstorming session to clarify the problem, users, inputs, outputs,
   constraints, risks, success criteria, and likely technical boundaries
   before filling in configuration values.
3. **Create the project configuration.** Copy
   `constitution.yaml.example` to the configured YAML filename, then replace
   every example value with an intentional project value informed by the
   discovery brief.
4. **Render and review the constitution.** Render
   `.specify/memory/constitution.md` from the YAML configuration. Check that
   paths, commands, dependency policy, interfaces, quality gates, and
   constraints describe the fork accurately.
5. **Write the specification.** Create the configured `SPEC.md` with required
   behavior, public contracts, edge cases, and acceptance criteria.
6. **Write the plan.** Create `PLAN.md` with architecture, risks, verification,
   rollout, rollback, and any necessary migrations.
7. **Track implementation.** Create stable, traceable entries in `TASKS.md`.
   Keep task status synchronized with the actual change.
8. **Implement and verify.** Read the constitution and specification before
   planning or editing. Follow the configured commands, tests, lint/type checks,
   pre-commit hooks, and CI gates.
9. **Record completion.** Move completed work to `CHANGELOG.md` and update
   affected architecture or documentation artifacts in the same change.
10. **Amend deliberately.** If implementation requires changing a guarantee,
   document the affected section, exact change, rationale, migration impact,
   and semantic version impact before relying on the amendment.

The paths above are examples from the template. The canonical paths for a fork
are the values under the `sdd` and `project` sections of its YAML
configuration.

## Getting started after forking

From the new repository:

```text
cp constitution.yaml.example constitution.yaml
```

On Windows PowerShell, use:

```powershell
Copy-Item constitution.yaml.example constitution.yaml
```

Then:

1. Replace example values in `constitution.yaml`, including project identity,
   runtime, structure, commands, quality gates, and constraints.
2. Ensure the configured environment example contains placeholders only, and
   keep the real `.env` out of version control.
3. Render the constitution with the renderer used by your project and review
   the generated file.
4. Create the configured `SPEC.md`, `PLAN.md`, `TASKS.md`, and `CHANGELOG.md`.
5. Add the project’s source, tests, CI, and automation only after their
   intended behavior and verification are represented in the SDD artifacts.

This template does not prescribe a renderer or a CLI because forks may use
different tooling. The fork should document that choice in its configuration
and make the render/validate command part of its normal quality gates.

## Working agreement for contributors and coding agents

Before changing a fork:

- Read the constitution and the current specification.
- Check branch freshness and worktree state.
- Find the existing placement, naming, bootstrap, and configuration patterns
  before introducing new structure.
- Prefer the smallest complete change and avoid unrelated refactors.
- Ask for approval before expanding scope in any category named by the
  constitution.
- Update documentation and architecture records when implementation changes
  their documented state.
- Never weaken a check, fabricate repository state, commit secrets, or hide a
  failure to make a change pass.

The constitution’s configured package manager is the only supported way to run
dependency, test, lint, formatting, type-checking, and operational commands.
The concrete commands belong to the fork’s YAML configuration; do not copy the
example commands without reviewing them.

## Prompt example: discover the use case

Before creating `constitution.yaml`, use a prompt like this with an AI
assistant. The goal is a collaborative discovery session, not an attempt to
generate a constitution from incomplete assumptions:

```text
You are my SDD discovery partner. We are starting from this template, and I
need to understand the use case before configuring the project constitution.

Read:
- README.md
- .specify/memory/constitution.md
- constitution.yaml.example

Interview me in a structured brainstorming session. Ask one focused question at
a time and challenge unclear or contradictory assumptions. Explore:
- the problem and why it matters,
- target users, operators, and affected stakeholders,
- primary workflows and important non-goals,
- inputs, outputs, public interfaces, and error behavior,
- data sources, storage, privacy, and security boundaries,
- runtime, deployment, integrations, and operational constraints,
- performance, reliability, accessibility, and platform requirements,
- AI/model behavior, human review, evaluation, and prohibited claims when
  applicable,
- quality gates, testing expectations, and success criteria.

Do not write application code or invent final configuration values. At the end,
produce a concise discovery brief with:
1. confirmed facts,
2. explicit assumptions,
3. open decisions requiring my approval,
4. proposed values or options for relevant constitution.yaml fields,
5. constraints and risks that should become SDD requirements.

Wait for my approval of the discovery brief before treating proposed values as
project decisions.
```

Save the approved discovery brief with the project’s planning materials, or
include its confirmed decisions in `SPEC.md` and `PLAN.md`. Do not silently
turn brainstorming assumptions into constitutional guarantees.

## Prompt example: integrate the constitution and YAML

After the discovery brief is approved, use a prompt like the following with a
coding agent:

```text
You are initializing a new project from this SDD template.

Read these files first:
- .specify/memory/constitution.md
- constitution.yaml.example
- README.md
- the approved use-case discovery brief

Use the approved discovery brief as context, but distinguish confirmed facts,
assumptions, and unresolved decisions. Create the project-specific constitution
configuration by copying constitution.yaml.example to constitution.yaml. Map
confirmed decisions to the appropriate YAML fields and ask me about every
unresolved decision that affects a constitutional guarantee. Do not retain
example-specific names, paths, commands, ML models, databases, or constraints
unless they are explicitly approved for this project.

Then render .specify/memory/constitution.md from constitution.yaml using the
repository's chosen renderer. If no renderer exists, propose the smallest
documented rendering approach before implementing it. Rendering must fail for
missing required values. Review the rendered constitution for contradictions,
unresolved placeholders, stale paths, and commands that do not match the
chosen runtime.

After the constitution is valid:
1. Create the configured SDD artifacts: SPEC.md, PLAN.md, TASKS.md, and
   CHANGELOG.md.
2. Transfer confirmed use-case requirements and acceptance criteria to SPEC.md.
3. Put architecture, risks, verification, rollout, and rollback in PLAN.md.
4. Put stable, traceable implementation tasks in TASKS.md.
5. Record the discovery decisions, initialization, and approved amendments in
   CHANGELOG.md.
6. Update README.md with the fork-specific setup and verification commands.

Do not implement product features yet. Report:
- which discovery decisions were used,
- the final configuration values and any assumptions,
- the rendered artifact paths,
- validation commands and their results,
- unresolved decisions that require my approval.
```

This prompt intentionally asks the agent to integrate both files: the YAML
supplies project-specific values, while the Markdown constitution supplies the
principles and rules those values instantiate.

## License and ownership

Add the license, maintainers, contribution process, and support policy for the
forked project. This template does not assume that those policies are shared
by every downstream repository.
