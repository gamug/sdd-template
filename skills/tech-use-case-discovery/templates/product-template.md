# Technical Discovery Specification Package

> Output template for `docs/PRODUCT.md`. Keep the numbered `##` sections and
> fill each one from the phase fragment it names. IDs go in the item heading or
> the first table column and use three digits (`UC-001`, `FR-002`, `US-001`,
> `ADR-001`, `RSK-001`); `FR-001` is reserved for SDD initialization, and each
> ID is defined once. Mark every open decision with a line containing
> `UNRESOLVED:` and the question to ask. Validate the draft with
> `python skills/tech-use-case-discovery/scripts/validate_discovery.py --draft docs/PRODUCT.md`.

## Application: [Project Name]

- **Project Name**: [Project Name]
- **Document Version**: `1.0.0`
- **Author**: [Name or role]

---

## 1. Executive Summary & Vision

- **Problem Statement**: [Current pain point or opportunity]
- **Vision**: [Solution overview and value proposition]
- **Success Metrics**: [Measurable KPIs]
- **Personas**: [Persona: role, key goals, main pain points]

---

## 2. Use Case Specifications

> Fragment: [`use-case-template.md`](./use-case-template.md), one `###` block per use case.

### Use Case `UC-001`: [Active Verb + Noun Phrase]

- **Primary Actor**: [Role or external system that starts the use case]
- **Preconditions**: [State required before the use case starts]
- **Triggers**: [Event that starts the use case]

#### Basic Flow (Happy Path)
1. The [Primary Actor] [action].
2. The system [response].

#### Exception Flow `UC-001-EX1`: [Error Condition]
1. At step [X], if [error], the system [handling].

---

## 3. Functional Requirements & User Stories

> Fragment: [`prd-user-stories-template.md`](./prd-user-stories-template.md).

### Functional Requirements (EARS Syntax)

| Requirement ID | EARS Pattern | Statement | MoSCoW Priority | Traceability |
| :--- | :--- | :--- | :--- | :--- |
| `FR-002` | Ubiquitous | The system shall [action]. | Must Have | `UC-001` |
| `FR-003` | Event-Driven | WHEN [event], the system shall [action]. | Should Have | `UC-001` |
| `FR-004` | Optional | WHERE [feature is present], the system shall [action]. | Could Have | `UC-001` |

- **MVP Won't Have**: [Capabilities explicitly out of scope for this release]

### User Story `US-001`: [Story Title]

- **Card**: As a [persona], I want [goal], so that [benefit].
- **Priority**: Must Have
- **Traceability**: `FR-002`

#### Acceptance Criteria (Given-When-Then)
```gherkin
SCENARIO: [Scenario name]
  GIVEN [precondition]
  WHEN [action]
  THEN [expected result]
```

---

## 4. Technology Stack Selection & MCDM Matrix

> Fragment: [`tech-stack-evaluation-matrix.md`](./tech-stack-evaluation-matrix.md).

### Multi-Criteria Decision-Making (MCDM) Evaluation

| Evaluation Criteria | Weight (1-5) | Option A: [Name] | Option B: [Name] |
| :--- | :---: | :---: | :---: |
| **[Criterion]** | [1-5] | [1-5] | [1-5] |
| **Weighted Score Total** | -- | **[Total A]** | **[Total B]** |

**Decision**: [Selected option and rationale]

---

## 5. Architecture Decision Records (ADRs)

> Fragment: [`adr-template.md`](./adr-template.md), one `###` block per decision.

### `ADR-001`: [Decision Title]

- **Status**: [Proposed | Accepted | Deprecated | Superseded]
- **Context**: [Forces and constraints that require a decision now]
- **Decision**: [The chosen option]
- **Consequences (Positive)**: [Benefits]
- **Consequences (Trade-offs)**: [Costs and how they are mitigated]
- **Traceability**: `FR-002`, `UC-001`

---

## 6. Development Environment Setup

> Fragment: [`dev-environment-checklist.md`](./dev-environment-checklist.md), "Development Environment Setup".

- **Target platforms**: [e.g., Linux, macOS, Windows (WSL2)]
- **Source hosting**: [Git hosting and access, e.g., SSH keys]
- **Runtimes and version managers**: [Language runtimes and how their versions are pinned]
- **Environment isolation**: [Devcontainer, Docker, host-only, or no-container, and why]
- **Local services**: [Services the project needs locally and the command that starts them, or none]
- **Editor configuration**: [Shared workspace settings and recommended extensions]
- **Code quality**: [Linters, formatters, type checkers]
- **Configuration variables**: [Environment example file and where local values live]
- **Verification command**: [Command that proves the environment works]

---

## 7. Risk Assessment & MVP Roadmap

### Risk Matrix

Impact and Probability use 1 (Low) to 3 (High); Score = Impact × Probability.
A score of 6 or more requires a mitigation plan.

| Risk ID | Description | Impact | Probability | Score | Mitigation Plan |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `RSK-001` | [Risk description] | High (3) | Medium (2) | **6** | [Mitigation plan] |

### Phased Roadmap

- **MVP**: [Scope of the first release]
- **Next phases**: [Later increments]

---

## 8. Governance & Workflow

> Fragment: [`dev-environment-checklist.md`](./dev-environment-checklist.md), "Governance & Workflow".

- **Version control**: [Integration branch, direct-commit policy, unrelated work on an in-flight PR]
- **Commits**: [Hook enforcing the template's commit convention; secret scanner run by hooks and CI]
- **CI**: [Ordered quality gates added to `.github/workflows/validators.yml`]
- **Tool configuration**: [Canonical configuration per tool; test layout and fixture policy]
- **Coding agent**: [Framework, instruction file, init command, tracked in Git, files it must reference]
- **Agent limits**: [Changes needing approval, destructive-history boundary, whether agents leave the tree on the pushed PR branch]
- **Naming**: [Established terms that must not be renamed]
- **Governance**: [Initial constitution version, ratification date, amendment log location]

---

## 9. Approval

- **Approved by**: [Name or role]
- **First approved on**: [YYYY-MM-DD]
- **Approved on**: [YYYY-MM-DD]
- **Approved content**: [Output of `validate_discovery.py --hash docs/PRODUCT.md` for the approved version]
