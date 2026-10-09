# Specification

## Functional requirements

### FR-001 — Discover and initialize the project

The project must complete the ordered Work Items in
[`PLAN.md`](./PLAN.md). The hierarchy is strictly:

```text
FR-001
└── Work Items
    └── Tasks
```

FR-001 does not define the project's purpose, scope, product, stack, or
architecture in advance. Those decisions are discovered through WI-001 and
then applied by the remaining Work Items.

## Acceptance criteria

- **AC-FR001-01:** `docs/PRODUCT.md` contains the complete discovery package,
  has no unresolved decisions, and records the user's approval; it passes
  `validate_discovery.py` without `--draft`.
- **AC-FR001-02:** Root `config.yaml` defines every key the constitution
  template requires, and each value's source (`PRODUCT.md § <section>` or
  `user, YYYY-MM-DD`) is recorded in the `Configuration Decisions` table of
  `docs/PRODUCT.md`; `uv run --with pyyaml python validate_config.py check` passes.
- **AC-FR001-03:** `.sdd/constitution.md` is rendered by
  `uv run --with pyyaml python validate_config.py render` with no placeholders left, and the other canonical `.sdd/`
  artifacts are synchronized with `docs/PRODUCT.md`.
- **AC-FR001-04:** The approved project structure and non-programmatic
  dependencies exist without implementing product source code.
- **AC-FR001-05:** The selected development environment can be created and
  its documented baseline checks pass without committed secrets.
- **AC-FR001-06:** Environment initialization can reproduce the documented
  setup from a clean checkout or reports actionable errors.

## Traceability

- FR-001 contains WI-001 through WI-006.
- WI-001 through WI-006 implement `AC-FR001-01` through `AC-FR001-06`,
  respectively.
- Each WI contains its own implementation tasks in
  [`TASKS.md`](./TASKS.md).
- Every task must identify exactly one parent WI.
- Every task must reference the acceptance-criteria ID it implements.
- No task may exist without a WI, and no WI may exist without FR-001.
