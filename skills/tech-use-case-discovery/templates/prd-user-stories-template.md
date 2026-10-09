> Fragment for `## 3. Functional Requirements & User Stories` in
> [`product-template.md`](./product-template.md). The problem statement,
> vision, success metrics, and personas go in `## 1. Executive Summary & Vision`.
> `FR-001` is reserved for the SDD initialization requirement: number product
> requirements from `FR-002`. IDs use three digits and are each defined once.

### Functional Requirements (EARS Syntax)

| Requirement ID | EARS Pattern | Statement | MoSCoW Priority | Traceability |
| :--- | :--- | :--- | :--- | :--- |
| `FR-002` | Ubiquitous | The system shall encrypt all stored user data at rest using AES-256. | Must Have | `UC-001` |
| `FR-003` | Event-Driven | WHEN a user uploads a CSV file, the system shall validate columns within 1s. | Must Have | `UC-001` |
| `FR-004` | State-Driven | WHILE processing data, the system shall display a real-time progress bar. | Should Have | `UC-002` |
| `FR-005` | Optional | WHERE GPU execution is available, the system shall accelerate ML inference. | Could Have | `UC-003` |
| `FR-006` | Unwanted / Error | IF an invalid payload is received, THEN the system shall return HTTP 400 with details. | Must Have | `UC-001` |

- **MVP Won't Have**: [Capabilities explicitly out of scope for this release]

### Non-Functional Requirements (NFRs)

- **Performance**: [e.g., response time < 500ms for 95th percentile requests]
- **Reliability & Availability**: [e.g., 99.9% availability]
- **Security**: [e.g., token-based authentication with role-based access]
- **Maintainability**: [e.g., automated test coverage above 80%]

### User Story `US-001`: [Story Title]

Repeat this `###` block for each user story.

- **Card**: As a [persona], I want [goal], so that [benefit].
- **Epic**: [Epic title]
- **Priority**: [Must Have / Should Have / Could Have / Won't Have]
- **Traceability**: `FR-002`

#### Acceptance Criteria (Given-When-Then)
```gherkin
SCENARIO 1: Successful execution
  GIVEN [precondition]
  WHEN [user action]
  THEN [system response]
  AND [additional verification]

SCENARIO 2: Error handling
  GIVEN [precondition]
  WHEN [invalid action]
  THEN [system error response]
```
