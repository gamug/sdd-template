## Project Constitution

> Project-specific values are supplied by `nlp-constitution.yaml`.
> `{{ ... }}` represents a required scalar; `{{#each ...}}` iterates a collection.
> Rendering must fail when a required value is missing.

Governing principles for **{{project.name}}** under a specification-driven development workflow. Specifications and plans precede implementation and may not silently contradict this constitution.

### Technological foundation

- **Runtime**: {{runtime.language}} {{runtime.version}}, managed by `{{runtime.package_manager}}` using `{{runtime.lockfile}}` and `{{runtime.dependency_manifest}}`.
- **Service type**: {{project.kind}}. Project exclusions are declared in `project.excluded_components`.
- **ML/NLP framework**: {{ml_nlp.framework}} {{ml_nlp.torch_version}}. All model stages must work under `{{ml_nlp.device_policy}}`.
- **Pinned models**:
{{#each ml_nlp.models}}
  - {{@key}}: `{{this.checkpoint}}` (optional: {{this.optional}})
{{/each}}
- Model selection is `{{ml_nlp.model_selection}}`; replacement requires every item under `ml_nlp.model_change_requires`.
- **Service layer**: {{service.framework}} {{service.framework_version}} with {{service.server}}, application `{{service.application}}`, default port {{service.default_port}}.
- **Storage**: {{storage.engine}} with the configured SOURCE/RESULTS topology, accessed through `{{storage.access_library}}` pinned to {{storage.access_library_version}}.
- Optional heavy dependency groups must remain isolated from normal package imports.
- New libraries, frameworks, model checkpoints, storage engines, or platform dependencies require a reviewed rationale and a constitution amendment when they alter these guarantees.

### Project structure

- Source: `{{project.source_dir}}/`; tests: `{{project.tests_dir}}/`; docs: `{{project.docs_dir}}/`; SDD artifacts: `{{project.sdd_dir}}/`.
- Source layout: {{architecture.source_layout}}. The configured local package is `{{architecture.local_package}}`.
- Entrypoints are organized by kind under `{{project.apps_dir}}/`, `{{project.cli_dir}}/`, and `{{project.scripts_dir}}/`, using `{{architecture.entrypoints.bootstrap}}`.
- Tests follow the configured mirrored layout and hermetic fixture policy under `project_structure.tests`.
- Each tool has one canonical configuration, as declared in `project_structure.config`.
- `.env` loading occurs only at `{{environment.load_location}}`; `{{environment.example_file}}` stays synchronized with configured variables.
- Naming follows `naming.mappings`; do not create a new term for an established stage or storage concept.

### Specification-driven development

- `{{sdd.spec_file}}` defines required behavior.
- `{{sdd.plan_file}}` translates requirements into architecture, risks, verification, rollout, and rollback.
- `{{sdd.tasks_file}}` contains active, traceable work with stable identifiers.
- Completed work moves to `{{sdd.changelog_file}}`, and status references are updated in the same change.
- Material ambiguity and scope changes are resolved in the SDD artifacts before implementation relies on them.

### AI behavior

- Model checkpoints are pinned, not selected dynamically.
- Inference must remain CPU-capable when `ml_nlp.cpu_support_required` is true.
- Missing source text follows `{{ai.fail_policy.missing_source_text}}`.
- Oversized input follows `{{ai.fail_policy.oversized_input}}`; silent truncation is prohibited when configured false.
- Outputs are {{ai.output_status}} and must not be represented as any item under `ai.prohibited_claims`.
- Human overrides are supported by `{{ai.human_corrections_module}}`.
- Accuracy claims require `{{ai.evaluation.package}}` evidence tracked in {{ai.evaluation.tracker}} against `{{ai.evaluation.baseline_doc}}`.

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

_Coding-agent conduct:_

- Read this constitution and `{{sdd.spec_file}}` before planning or editing.
- Match existing placement, naming, imports, and bootstrap conventions before introducing structure.
- Prefer the smallest complete change; avoid unrelated refactors and abstractions.
- `{{agent.instruction_file}}` must satisfy the existence, tracking, and reference rules configured under `agent` but cannot override version-controlled SDD artifacts.
- Respect `agent.destructive_history_boundary` before checkout or reset operations.
- Obtain approval for every item under `agent.scope_expansion_requires_approval`.
- Update all configured architecture artifacts when implementation changes their documented state; never rename an artifact when `rename_allowed` is false.
- Never fabricate repository state or weaken checks to make a change pass.

### Interfaces, data, and reliability

- Public contracts define inputs, outputs, errors, versions, compatibility, and ownership.
- Validate external inputs at trust boundaries.
- SOURCE remains read-only and RESULTS follows its configured read/write contract.
- Schema changes are migration-driven and require explicit scope approval.
- Time, ordering, retries, idempotency, and data provenance are explicit where applicable.
- Failures are observable and are never silently converted to successful predictions.
- External calls use bounded timeouts, retries, and resource limits.

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

### Code and Git

- Commit convention: `{{quality.commit_convention}}`, enforced by {{quality.commit_hook}}.
- Integration branch: `{{project.integration_branch}}`; direct commits are governed by `code_git.direct_commits_to_integration_branch`.
- Verify branch freshness before editing.
- Do not place unrelated development on an in-flight PR without following `code_git.unrelated_work_on_inflight_pr`.
- Required hooks and CI checks must pass before merge.
- Secrets must not be committed; example environment files contain placeholders only.
- Leave the working tree on the pushed PR branch when configured, and include the complete PR URL in the final handoff.

### Project-specific constraints

{{#each known_constraints}}
- {{this}}
{{/each}}

### Governance

This constitution supersedes ad-hoc convention when the two conflict.

- Amendments identify the affected section, exact change, rationale, and migration impact.
- Amendments are reviewed through the normal pull-request path before being relied upon.
- Use semantic versioning: MAJOR for removed or redefined guarantees, MINOR for new or materially expanded principles, PATCH for non-semantic corrections.
- Update affected templates, SDD artifacts, architecture records, automation, and contributor documentation together.
- Reviewers cite the conflicting section when rejecting non-compliant work.

**Version**: {{governance.version}}  
**Ratified**: {{governance.ratified}}  
**Last Amended**: {{governance.last_amended}}  

**Amendment log source**: {{governance.amendment_log_source}}