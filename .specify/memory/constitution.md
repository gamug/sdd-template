# Project Constitution

{{!--
Template input. Values come from the root config.yaml and are rendered with
`validate_config.py render`; rendering fails when a required value is missing.
Syntax: {{key}} scalar, {{#each key}} collection, {{#if key}} optional block.
--}}

Governing principles for **{{project.name}}** under a specification-driven development workflow. Specifications and plans precede implementation and may not silently contradict this constitution.

## Governance framework and rendering

- Project-specific parameters and operational variables are defined exclusively
  in the root `config.yaml`; informal task notes and prompts cannot replace
  configuration.
- The files under `.specify/memory/` are immutable template inputs.
  Initialization creates the canonical project artifacts under `.sdd/`,
  including `.sdd/constitution.md`; from then on, `.sdd/constitution.md` is the
  generated governance contract and is not an independent source of project
  decisions.
- Renderers, build scripts, CLI harnesses, and AI context generators must
  validate the configuration before execution. Missing required configuration
  keys, mandatory environment variables, or schema parameters must fail
  immediately with an explicit, actionable error.
- This constitution and its approved SDD artifacts have precedence over
  informal prompts, ephemeral task notes, or developer preferences.

## Technological foundation

- **Runtime**: {{runtime.language}} {{runtime.version}}, managed by `{{runtime.package_manager}}` using `{{runtime.lockfile}}` and `{{runtime.dependency_manifest}}`.
- The configured runtime, language version, and package manager are locked.
  Lockfiles must be versioned and enforced by CI for every dependency
  installation or build.
- **Service type**: {{project.kind}}. Excluded components:
{{#each project.excluded_components}}
  - {{this}}
{{/each}}
- Where the project has core business logic, it remains independent from web
  frameworks, UI libraries, and ORMs. Dependencies point inward toward stable
  domain abstractions rather than outward toward volatile concrete tools.
- Optional heavy dependency groups must remain isolated from normal package imports.
- New libraries, frameworks, model checkpoints, storage engines, or platform dependencies require a reviewed rationale and a constitution amendment when they alter these guarantees.
- Public API contracts, storage schemas, security boundaries, and architectural
  layer boundaries are stable guarantees across minor releases unless an
  approved amendment explicitly changes them.
- Changes to runtime versions, core frameworks, breaking API contracts, or
  zero-trust security boundaries require constitutional review and a MAJOR
  version change.
- Where the project has layered domain logic, every Work Item architecture
  decision must preserve its Clean Architecture boundaries. An exception
  requires explicit rationale, impact analysis, human approval, and a
  constitutional amendment.

## Project structure

- Source: `{{project.source_dir}}/`; tests: `{{project.tests_dir}}/`; docs: `docs/`; SDD artifacts: `.sdd/` (fixed template conventions).
- Tests follow this layout and hermetic fixture policy:
{{#each project_structure.tests}}
  - {{@key}}: {{this}}
{{/each}}
- Each tool has one canonical configuration:
{{#each project_structure.config}}
  - {{@key}}: {{this}}
{{/each}}
- Application settings must be injected through validated environment
  variables or the configured equivalent; secrets must never be hardcoded or
  committed to Git history.
- Naming follows these mappings; do not create a new term for an established stage or storage concept:
{{#each naming.mappings}}
  - {{@key}}: {{this}}
{{/each}}

## Specification-driven development

- `.sdd/SPEC.md` defines required behavior.
- `.sdd/PLAN.md` translates requirements into architecture, risks, verification, rollout, and rollback.
- `.sdd/TASKS.md` contains active, traceable work with stable identifiers.
- The planning hierarchy is strict: functional requirements contain Work Items
  (WI), and each WI contains implementation tasks.
- Every Work Item in `.sdd/PLAN.md` must reference its parent functional
  requirement, and every task in `.sdd/TASKS.md` must reference exactly
  one parent WI. Missing links are invalid and must not be started.
- Product functional requirements define business intent and testable
  acceptance criteria without technical implementation details. Repository
  initialization and governance requirements may name the concrete artifacts
  and workflow steps needed to enforce this constitution. Work Items define
  architecture, contracts, schemas, and boundaries. Tasks define ordered,
  dependency-aware execution.
- Every production code commit must reference its Task ID, WI, and FR, in the
  commit format defined under Code and Git.
- Acceptance criteria use stable identifiers such as `AC-FR001-01`; every task
  must reference the acceptance-criteria IDs it implements.
- Work Item status and task status must remain synchronized.
- Project-specific decisions are collected and approved in `docs/PRODUCT.md`
  during discovery, normalized into root `config.yaml` with the source of
  every value recorded in the `Configuration Decisions` table of
  `docs/PRODUCT.md`, and rendered into `.sdd/constitution.md` by
  `validate_config.py render`. `.sdd/SPEC.md`, `.sdd/PLAN.md`, and
  `.sdd/TASKS.md` are then derived from `docs/PRODUCT.md`. `FR-001` is the
  initialization requirement; product requirements are numbered from `FR-002`.
- `docs/PRODUCT.md` is the decision source; `config.yaml` is the
  authoritative normalized configuration. Any edit to `config.yaml` must
  update its `Configuration Decisions` row, be synchronized to the affected
  SDD artifacts, and be followed by `validate_config.py render`.
- Missing or ambiguous inputs must be presented as explicit, context-rich
  questions that identify the decision, explain its impact, and provide
  concrete options or an expected answer format. Agents must not guess or
  silently preserve example values.
- Completed work moves to `.sdd/CHANGELOG.md`, and status references are updated in the same change.
- Material ambiguity and scope changes are resolved in the SDD artifacts before implementation relies on them.
- SDD acceptance criteria should use a consistent executable form such as
  GIVEN-WHEN-THEN where applicable.

## Coding-agent conduct

- Read this constitution and `.sdd/SPEC.md` before planning or editing.
- Match existing placement, naming, imports, and bootstrap conventions before introducing structure.
- Prefer the smallest complete change; avoid unrelated refactors and abstractions.
- `{{agent.instruction_file}}` cannot override version-controlled SDD artifacts. Must exist: {{agent.must_exist}}; tracked in Git: {{agent.tracked}}; created with `{{agent.init_command_if_missing}}` when missing. It must reference:
{{#each agent.must_reference}}
  - `{{this}}`
{{/each}}
- Respect this destructive-history boundary before checkout or reset operations:
{{#each agent.destructive_history_boundary}}
  - {{@key}}: {{this}}
{{/each}}
- Obtain approval for every item below:
{{#each agent.scope_expansion_requires_approval}}
  - {{this}}
{{/each}}
- Update all affected product, SDD, configuration, constitution, template,
  automation, CI, and contributor artifacts when implementation changes their
  documented state.
- Never fabricate repository state, and never weaken, disable, or delete
  tests, static-analysis rules, checks, or SDD artifacts to obtain a passing
  result.

## Interfaces, data, and reliability

- Public contracts define inputs, outputs, errors, versions, compatibility, and ownership.
- Validate external inputs at trust boundaries.
- Schema changes are migration-driven and require explicit scope approval.
- Time, ordering, retries, idempotency, and data provenance are explicit where applicable.
- Failures are observable and are never silently converted to successful results.
- Where the project makes external network calls, database queries, or
  system-process calls, each uses explicit timeouts, resource limits, circuit
  breakers, and bounded retries with exponential backoff.
- Where the project exposes external or inter-service interfaces, they use
  strict, versioned schemas such as OpenAPI, gRPC/Protobuf, or JSON Schema
  before implementation.
- Where the project has persistence, domain logic accesses it through
  repositories or gateways; direct SQL or storage calls do not belong in
  business or presentation layers.
- Failures must be logged with structured context, error codes, and tracing
  identifiers where available. Silent exception handling and empty catch
  blocks are prohibited.

## Executable commands

```text
{{commands.dependency_install}}     # base dependencies
{{commands.test}}                   # full test suite
{{commands.ci_test}}                # CI tests
{{commands.lint}}                   # lint
{{commands.format_check}}           # format verification
{{commands.type_check}}             # type analysis
{{commands.pre_commit}}             # all local gates
```

- CI configuration: `{{quality.ci_file}}`; ordered gates:
{{#each quality.ci_gate_order}}
  - {{this}}
{{/each}}
- Commands must use the configured package manager and locked environment.
- All canonical validation commands must run in isolated, deterministic CI
  before integration.

## Code and Git

- Commit subjects use imperative Conventional Commits syntax with the full
  FR/WI/Task traceability suffix, enforced by {{quality.commit_hook}}:
  `type(scope): imperative summary [FR-002][WI-003][TASK-007]`.
- Integration branch: `{{project.integration_branch}}`; direct commits allowed: {{code_git.direct_commits_to_integration_branch}}.
- Verify branch freshness before editing.
- Feature branches are short-lived and pull requests contain isolated,
  self-contained functional changes.
- Unrelated development on an in-flight PR: {{code_git.unrelated_work_on_inflight_pr}}.
- Required hooks and CI checks must pass before merge.
- Pre-commit and pre-push hooks must run the configured fast quality checks,
  including secret scanning with `{{quality.secret_scanner}}`. CI must reject
  detected secrets.
- Secrets must not be committed; example environment files contain placeholders only.
- Leave the working tree on the pushed PR branch: {{agent.leave_on_pr_branch}}. Include the complete PR URL in the final handoff.

{{#if domain_sections}}
{{#each domain_sections}}
## {{this.title}}

{{#each this.rules}}
- {{this}}
{{/each}}

{{/each}}
{{/if}}
## Project-specific constraints

{{#each known_constraints}}
- {{this}}
{{/each}}

## Governance

This constitution supersedes ad-hoc convention when the two conflict.

- Amendments identify the affected section, exact change, rationale, and migration impact.
- Amendments that change architecture or governance include an ADR describing
  business rationale, technical impact, trade-offs, and migration steps.
- Amendments are reviewed through the normal pull-request path before being relied upon.
- Use semantic versioning: MAJOR for removed or redefined guarantees, MINOR for new or materially expanded principles, PATCH for non-semantic corrections.
- The highest applicable impact wins: MAJOR overrides MINOR, and MINOR
  overrides PATCH. Runtime, framework, breaking API, and security-boundary
  changes are MAJOR.
- When an amendment is approved, update every affected artifact together,
  including `docs/PRODUCT.md`, `.sdd/SPEC.md`, `.sdd/PLAN.md`,
  `.sdd/TASKS.md`, root `config.yaml`, `.sdd/constitution.md`, templates,
  architecture records, automation, CI workflows, and contributor
  documentation.
- Reviewers cite the conflicting section when rejecting non-compliant work.
- The rendered constitution records its version, effective date, and governance
  status from the approved project configuration.

**Version**: {{governance.version}}  
**Ratified**: {{governance.ratified}}  
**Last Amended**: {{governance.last_amended}}  

**Amendment log source**: {{governance.amendment_log_source}}
