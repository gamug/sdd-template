# Specification

## Functional requirements

### FR-001 — Discover and initialize the project

The project must complete the ordered Work Items in [`PLAN.md`](./PLAN.md). The hierarchy is strictly:

```text
FR-001
└── Work Items
    └── Tasks
```

FR-001 does not define the project's purpose, scope, product, stack, or architecture in advance. Those decisions are discovered through WI-001 and then applied by the remaining Work Items. FR-001 is reserved for initialization: the product requirements discovered in WI-001 are numbered from `FR-002`, and `validate_discovery.py` rejects an `FR-001` row in `docs/PRODUCT.md`.

## Acceptance criteria

Each criterion uses the constitution's executable GIVEN-WHEN-THEN form. A criterion may have several scenarios under the same ID.

- **AC-FR001-01:**

  ```gherkin
  SCENARIO: Discovery package approved
    GIVEN the discovery phases are complete
    WHEN the user approves `docs/PRODUCT.md`
    THEN it contains the complete discovery package
    AND it has no unresolved decisions
    AND it records the user's approval
    AND `validate_discovery.py` passes without `--draft`
  ```

  ```gherkin
  SCENARIO: Discovery ADRs accepted
    GIVEN `docs/PRODUCT.md` is approved
    WHEN the seeded ADRs are accepted
    THEN the root `ADR.md` holds the discovery ADRs
    AND each is `Accepted` with `Approved by` and `Approved on` filled from the approver and first approval date recorded in `docs/PRODUCT.md`
  ```

- **AC-FR001-02:**

  ```gherkin
  SCENARIO: Configuration built
    GIVEN an approved `docs/PRODUCT.md`
    WHEN root `config.yaml` is built
    THEN it defines every key the constitution template requires
    AND each value's source (`PRODUCT.md § <section>` or `user, YYYY-MM-DD`) is recorded in the `Configuration Decisions` table of `docs/PRODUCT.md`
    AND `validate_config.py check` passes
  ```

- **AC-FR001-03:**

  ```gherkin
  SCENARIO: Constitution rendered
    GIVEN a `config.yaml` that passes `validate_config.py check`
    WHEN `validate_config.py render` runs
    THEN `.sdd/constitution.md` has no placeholders left
  ```

  ```gherkin
  SCENARIO: SDD objects synchronized
    GIVEN a rendered `.sdd/constitution.md`
    WHEN the other canonical `.sdd/` artifacts are created
    THEN they are synchronized with `docs/PRODUCT.md`
  ```

- **AC-FR001-04:**

  ```gherkin
  SCENARIO: Project structure created
    GIVEN the approved constitution and `docs/PRODUCT.md`
    WHEN the project structure is created
    THEN the approved project structure and non-programmatic dependencies exist
    AND no product source code has been implemented
  ```

- **AC-FR001-05:**

  ```gherkin
  SCENARIO: Environment created
    GIVEN the approved project structure exists
    WHEN the selected development environment is created
    THEN its documented baseline checks pass without committed secrets
  ```

- **AC-FR001-06:**

  ```gherkin
  SCENARIO: Environment reproduced
    GIVEN a clean checkout and every documented prerequisite
    WHEN the environment initialization is run
    THEN it reproduces the documented setup
  ```

  ```gherkin
  SCENARIO: Missing prerequisite reported
    GIVEN a clean checkout missing a documented prerequisite
    WHEN the environment initialization is run
    THEN it reports an actionable error
  ```

## Traceability

- FR-001 contains WI-001 through WI-006.
- WI-001 through WI-006 implement `AC-FR001-01` through `AC-FR001-06`, respectively.
- Each WI contains its own implementation tasks in [`TASKS.md`](./TASKS.md).
- Every task must identify exactly one parent WI.
- Every task must reference the acceptance-criteria ID it implements.
- No task may exist without a WI, and no WI may exist without FR-001.
