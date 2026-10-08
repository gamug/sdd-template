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

## Traceability

- FR-001 contains WI-001 through WI-006.
- Each WI contains its own implementation tasks in
  [`TASKS.md`](./TASKS.md).
- Every task must identify exactly one parent WI.
- No task may exist without a WI, and no WI may exist without FR-001.
