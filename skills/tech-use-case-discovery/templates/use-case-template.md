> Fragment for `## 2. Use Case Specifications` in
> [`product-template.md`](./product-template.md). Repeat this `###` block for
> each use case. The ID stays in the heading and uses three digits; flows
> extend it (`UC-001-ALT1`, `UC-001-EX1`).

### Use Case `UC-001`: [Active Verb + Noun Phrase]

- **Primary Actor**: [User role or external system that starts the use case]
- **Secondary Actors**: [Supporting systems, databases, third-party APIs]
- **Brief Description**: [2-3 sentences on the user goal and expected outcome]
- **Preconditions**:
  - [e.g., User is authenticated with a valid role]
- **Triggers**:
  - [e.g., User clicks "Upload Dataset"]

#### Basic Flow (Happy Path)
1. The [Primary Actor] initiates [action].
2. The system validates [inputs or preconditions].
3. The system processes [data or logic].
4. The system displays [output or confirmation].

#### Alternate Flow `UC-001-ALT1`: [Descriptive Title]
1. At step [X] of the basic flow, if [condition], the system [alternative step].
2. The flow rejoins the basic flow at step [Y].

#### Exception Flow `UC-001-EX1`: [Error Condition Title]
1. At step [X] of the basic flow, if [error occurs], the system logs [error details].
2. The system displays "[user-friendly error]".
3. The use case ends in a failed state without data corruption.

#### Postconditions
- **Success**: [Guaranteed system state after successful completion]
- **Failure**: [Guaranteed system state if execution fails]

#### Non-Functional Constraints
- **Performance**: [e.g., completes within 2.0 seconds]
- **Security**: [e.g., data in transit is encrypted]
