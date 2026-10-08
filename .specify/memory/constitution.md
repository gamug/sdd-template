## Project Constitution

> Project-specific values are supplied by the root `config.yaml`.
> `{{ ... }}` represents a required scalar; `{{#each ...}}` iterates a collection.
> Rendering must fail when a required value is missing.

Governing principles for **{{project.name}}** under a specification-driven development workflow. Specifications and plans precede implementation and may not silently contradict this constitution.

### Governance framework and rendering

- Project-specific parameters and operational variables are defined exclusively
  in the root `config.yaml`; informal task notes and prompts cannot replace
  configuration.
- The files under `.specify/memory/` are immutable template inputs. WI-003
  creates the canonical project artifacts under `.sdd/`, including
  `.sdd/constitution.md`; after WI-003, `.sdd/constitution.md` is the
  generated governance contract and is not an independent source of project
  decisions.
- Renderers, build scripts, CLI harnesses, and AI context generators must
  validate the configuration before execution. Missing required configuration
  keys, mandatory environment variables, or schema parameters must fail
  immediately with an explicit, actionable error.
- This constitution and its approved SDD artifacts have precedence over
  informal prompts, ephemeral task notes, or developer preferences.

### Technological foundation

- **Runtime**: {{runtime.language}} {{runtime.version}}, managed by `{{runtime.package_manager}}` using `{{runtime.lockfile}}` and `{{runtime.dependency_manifest}}`.
- The configured runtime, language version, and package manager are locked.
  Lockfiles must be versioned and enforced by CI for every dependency
  installation or build.
- **Service type**: {{project.kind}}. Project exclusions are declared in `project.excluded_components`.
- Core business logic remains independent from web frameworks, UI libraries,
  and ORMs. Dependencies point inward toward stable domain abstractions rather
  than outward toward volatile concrete tools.
- **ML/NLP framework**: {{ml_nlp.framework}} {{ml_nlp.torch_version}}. All model stages must work under `{{ml_nlp.device_policy}}`.
- **Pinned models**:
{{#each ml_nlp.models}}
  - {{@key}}: `{{this.checkpoint}}` (optional: {{this.optional}})
{{/each}}
- Model selection is `{{ml_nlp.model_selection}}`; replacement requires every item under `ml_nlp.model_change_requires`.
- Model checkpoints, context-window limits, tokenizers, and external AI
  endpoints must be explicitly pinned; floating production model or endpoint
  versions are prohibited.
- **Service layer**: {{service.framework}} {{service.framework_version}} with {{service.server}}, application `{{service.application}}`, default port {{service.default_port}}.
- **Storage**: {{storage.engine}} with the configured SOURCE/RESULTS topology, accessed through `{{storage.access_library}}` pinned to {{storage.access_library_version}}.
- Optional heavy dependency groups must remain isolated from normal package imports.
- New libraries, frameworks, model checkpoints, storage engines, or platform dependencies require a reviewed rationale and a constitution amendment when they alter these guarantees.
- Public API contracts, storage schemas, security boundaries, and architectural
  layer boundaries are stable guarantees across minor releases unless an
  approved amendment explicitly changes them.
- Changes to runtime versions, core frameworks, breaking API contracts, or
  zero-trust security boundaries require constitutional review and a MAJOR
  version change.
- Every Work Item architecture decision must preserve Clean Architecture
  boundaries. An exception requires explicit rationale, impact analysis,
  human approval, and a constitutional amendment.

### Project structure

- Source: `{{project.source_dir}}/`; tests: `{{project.tests_dir}}/`; docs: `{{project.docs_dir}}/`; SDD artifacts: `{{project.sdd_dir}}/`.
- Source layout: {{architecture.source_layout}}. The configured local package is `{{architecture.local_package}}`.
- Entrypoints are organized by kind under `{{project.apps_dir}}/`, `{{project.cli_dir}}/`, and `{{project.scripts_dir}}/`, using `{{architecture.entrypoints.bootstrap}}`.
- Tests follow the configured mirrored layout and hermetic fixture policy under `project_structure.tests`.
- Each tool has one canonical configuration, as declared in `project_structure.config`.
- `.env` loading occurs only at `{{environment.load_location}}`; `{{environment.example_file}}` stays synchronized with configured variables.
- Application settings must be injected through validated environment
  variables or the configured equivalent; secrets must never be hardcoded or
  committed to Git history.
- Naming follows `naming.mappings`; do not create a new term for an established stage or storage concept.

### Specification-driven development

- `{{sdd.spec_file}}` defines required behavior.
- `{{sdd.plan_file}}` translates requirements into architecture, risks, verification, rollout, and rollback.
- `{{sdd.tasks_file}}` contains active, traceable work with stable identifiers.
- The planning hierarchy is strict: functional requirements contain Work Items
  (WI), and each WI contains implementation tasks.
- Every Work Item in `{{sdd.plan_file}}` must reference its parent functional
  requirement, and every task in `{{sdd.tasks_file}}` must reference exactly
  one parent WI. Missing links are invalid and must not be started.
- Product functional requirements define business intent and testable
  acceptance criteria without technical implementation details. Repository
  initialization and governance requirements may name the concrete artifacts
  and workflow steps needed to enforce this constitution. Work Items define
  architecture, contracts, schemas, and boundaries. Tasks define ordered,
  dependency-aware execution.
- Every production code commit must reference its Task ID, WI, and FR.
- Commit subjects must use Conventional Commits syntax and include the full
  FR/WI/Task traceability suffix:
  `type(scope): imperative summary [FR-001][WI-002][TASK-004]`.
- Acceptance criteria use stable identifiers such as `AC-FR001-01`; every task
  must reference the acceptance-criteria IDs it implements.
- Work Item status and task status must remain synchronized.
- Project-specific decisions are collected in `docs/PRODUCT.md`, transformed
  into the approved `.sdd/SPEC.md`, and normalized into root `config.yaml`.
  The resulting configuration renders `.sdd/constitution.md`. Before WI-003,
  the corresponding files under `.specify/memory/` are template inputs only.
- `docs/PRODUCT.md` and `.sdd/SPEC.md` are the decision sources; `config.yaml`
  is the authoritative normalized configuration. Direct edits to
  `config.yaml` must be synchronized back to the affected decision and SDD
  artifacts.
- Missing or ambiguous inputs must be presented as explicit, context-rich
  questions that identify the decision, explain its impact, and provide
  concrete options or an expected answer format. Agents must not guess or
  silently preserve example values.
- Completed work moves to `{{sdd.changelog_file}}`, and status references are updated in the same change.
- Material ambiguity and scope changes are resolved in the SDD artifacts before implementation relies on them.
- SDD acceptance criteria should use a consistent executable form such as
  GIVEN-WHEN-THEN where applicable.

### AI behavior

- Production model checkpoints, context-window limits, tokenizers, and AI
  endpoints must be explicitly pinned and must not be selected dynamically.
  Development-time and coding-agent model choices are unrestricted by this
  production pinning rule.
- Inference must remain CPU-capable when `ml_nlp.cpu_support_required` is true.
- Missing source text follows `{{ai.fail_policy.missing_source_text}}`.
- Oversized input follows `{{ai.fail_policy.oversized_input}}`; silent truncation is prohibited when configured false.
- Outputs are {{ai.output_status}} and must not be represented as any item under `ai.prohibited_claims`.
- Human overrides are supported by `{{ai.human_corrections_module}}`.
- Accuracy claims require `{{ai.evaluation.package}}` evidence tracked in {{ai.evaluation.tracker}} against `{{ai.evaluation.baseline_doc}}`.
- Generated proposals must pass deterministic validation gates such as tests,
  linters, type checks, and security scans before they are accepted.
- Agents must not claim work is complete or correct without verifiable
  evidence, such as passing command output or a recorded analysis result.
- Human developers retain final approval authority over agent-generated plans,
  decisions, and implementations.

### Evaluation and reporting

- Every configured classification stage reports the complete metric set.
- Per-class metrics:
{{#each metrics.per_class}}
  - {{this}}
{{/each}}
- Offline overall metrics:
{{#each metrics.overall_offline}}
  - {{this}}
{{/each}}
- Downstream judge evaluation follows `metrics.downstream_judge`, including configured weighting, overall measures, and diagnostic-only variants.
- Candidate comparisons use `{{metrics.comparison_format}}` and the same metric implementation and evaluation path.
- Historical runs missing newly required metrics are handled by: {{metrics.missing_historical_metrics}}.
- Reporting policy: {{metrics.reporting_policy}}.
- Evaluation runs must emit machine-readable reports, such as JSON or JUnit
  XML, including execution time, metric deltas, and coverage where applicable.
- CI must compare current results with historical baselines. Degradation in
  required performance, coverage, or acceptance results blocks integration.

_Coding-agent conduct:_

- Read this constitution and `{{sdd.spec_file}}` before planning or editing.
- Match existing placement, naming, imports, and bootstrap conventions before introducing structure.
- Prefer the smallest complete change; avoid unrelated refactors and abstractions.
- `{{agent.instruction_file}}` must satisfy the existence, tracking, and reference rules configured under `agent` but cannot override version-controlled SDD artifacts.
- Respect `agent.destructive_history_boundary` before checkout or reset operations.
- Obtain approval for every item under `agent.scope_expansion_requires_approval`.
- Update all affected product, SDD, configuration, constitution, template,
  automation, CI, and contributor artifacts when implementation changes their
  documented state; never rename an artifact when `rename_allowed` is false.
- Never fabricate repository state or weaken checks to make a change pass.
- Agents must not weaken, disable, or delete tests, static-analysis rules, or
  SDD artifacts to obtain a passing result.

### Interfaces, data, and reliability

- Public contracts define inputs, outputs, errors, versions, compatibility, and ownership.
- Validate external inputs at trust boundaries.
- SOURCE remains read-only and RESULTS follows its configured read/write contract.
- Schema changes are migration-driven and require explicit scope approval.
- Time, ordering, retries, idempotency, and data provenance are explicit where applicable.
- Failures are observable and are never silently converted to successful predictions.
- External calls use bounded timeouts, retries, and resource limits.
- External network calls, database queries, and system processes must use
  explicit timeouts, circuit breakers, and bounded retries with exponential
  backoff. Circuit breakers are mandatory for all three categories.
- External and inter-service interfaces must use strict, versioned schemas
  such as OpenAPI, gRPC/Protobuf, or JSON Schema before implementation.
- Domain logic accesses persistence through repositories or gateways; direct
  SQL or storage calls do not belong in business or presentation layers.
- Failures must be logged with structured context, error codes, and tracing
  identifiers where available. Silent exception handling and empty catch
  blocks are prohibited.
- Retries must be bounded and use exponential backoff for all three categories.

### Executable commands

```text
{{commands.dependency_install}}     # base dependencies
{{commands.eval_install}}           # evaluation dependencies
{{commands.notebook_install}}       # notebook dependencies
{{commands.model_setup}}            # pre-download configured models
{{commands.service_start}}          # service
{{commands.pipeline_run}}           # batch pipeline
{{commands.evaluation_run}}         # full evaluation
{{commands.evaluation_ui}}          # evaluation UI
{{commands.test}}                   # full test suite
{{commands.ci_test}}                # CI tests
{{commands.lint}}                   # lint
{{commands.format_check}}           # format verification
{{commands.type_check}}             # type analysis
{{commands.pre_commit}}             # all local gates
```

- CI configuration: `{{quality.ci_file}}`; ordered gates come from `quality.ci_gate_order`.
- The separate evaluation workflow is `{{quality.evaluation_workflow.file}}`, blocking: {{quality.evaluation_workflow.blocking}}.
- Commands must use the configured package manager and locked environment.
- All canonical validation commands must run in isolated, deterministic CI
  before integration.

### Code and Git

- Commit convention: `{{quality.commit_convention}}`, enforced by {{quality.commit_hook}}.
- Commit subjects use imperative Conventional Commit syntax and include the
  full FR/WI/Task traceability suffix required above.
- Integration branch: `{{project.integration_branch}}`; direct commits are governed by `code_git.direct_commits_to_integration_branch`.
- Verify branch freshness before editing.
- Feature branches are short-lived and pull requests contain isolated,
  self-contained functional changes.
- Do not place unrelated development on an in-flight PR without following `code_git.unrelated_work_on_inflight_pr`.
- Required hooks and CI checks must pass before merge.
- Pre-commit and pre-push hooks must run the configured fast quality checks,
  including secret scanning where configured. CI must reject detected secrets.
- Secrets must not be committed; example environment files contain placeholders only.
- Leave the working tree on the pushed PR branch when configured, and include the complete PR URL in the final handoff.

### Project-specific constraints

{{#each known_constraints}}
- {{this}}
{{/each}}

### Governance

This constitution supersedes ad-hoc convention when the two conflict.

- Amendments identify the affected section, exact change, rationale, and migration impact.
- Amendments that change architecture or governance include an ADR describing
  business rationale, technical impact, trade-offs, and migration steps.
- Amendments are reviewed through the normal pull-request path before being relied upon.
- Use semantic versioning: MAJOR for removed or redefined guarantees, MINOR for new or materially expanded principles, PATCH for non-semantic corrections.
- The highest applicable impact wins: MAJOR overrides MINOR, and MINOR
  overrides PATCH. Runtime, framework, breaking API, and security-boundary
  changes are MAJOR.
- Update affected templates, SDD artifacts, architecture records, automation,
  CI workflows, and contributor documentation together.
- When an amendment is approved, update every affected artifact, including
  `docs/PRODUCT.md`, `{{sdd.spec_file}}`, `{{sdd.plan_file}}`,
  `{{sdd.tasks_file}}`, root `config.yaml`, `.sdd/constitution.md`, templates,
  automation, CI workflows, and contributor documentation.
- Reviewers cite the conflicting section when rejecting non-compliant work.
- The rendered constitution records its version, effective date, and governance
  status from the approved project configuration.

**Version**: {{governance.version}}  
**Ratified**: {{governance.ratified}}  
**Last Amended**: {{governance.last_amended}}  

**Amendment log source**: {{governance.amendment_log_source}}