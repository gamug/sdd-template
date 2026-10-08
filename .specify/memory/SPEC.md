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

- **AC-FR001-01:** `docs/PRODUCT.md` contains the approved discovery package
  and clearly identifies unresolved decisions.
- **AC-FR001-02:** Root `config.yaml` contains only approved project values
  traceable to `docs/PRODUCT.md` or an explicit user decision.
- **AC-FR001-03:** Canonical `.sdd/` artifacts are created from the approved
  configuration and synchronized with `docs/PRODUCT.md`.
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
