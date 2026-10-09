# Architecture Decision Records (ADR) Guide

## Overview

Software architecture is the composition of architectural design decisions. An Architecture Decision Record (ADR) captures a single significant decision, its context, business drivers, evaluated alternatives, and trade-offs.

---

## Why Capture Architectural Decisions?

- **Traceability**: Preserves the "why" behind decisions for future maintainers.
- **Knowledge Transfer**: Onboards new team members by documenting evaluated alternatives and rejected options.
- **Change Management**: Facilitates impact analysis when constraints or requirements evolve.

---

## ADR Lifecycle States

- **Proposed**: Under review by technical leads and stakeholders.
- **Accepted**: Approved and active design guidance for the team.
- **Deprecated**: Decision is no longer relevant due to scope or technology shifts.
- **Superseded**: Replaced by a newer ADR (must include a link to the replacing ADR ID).

---

## Anatomy of an ADR

1. **Title & Number**: Sequential identifier and clear summary (e.g., `ADR-001: Use FastAPI for Asynchronous Backend API`).
2. **Status**: Current lifecycle state (*Proposed*, *Accepted*, *Deprecated*, *Superseded*).
3. **Context**: The business problem, technical constraints, quality attribute requirements, and forces at play.
4. **Decision**: Explicit statement of the chosen solution and architectural pattern.
5. **Considered Options / Rejected Options**: Evaluated options with pros/cons analysis for each, and why the rejected ones lost.
6. **Consequences**:
   - **Positive**: Expected performance, developer speed, or maintainability gains.
   - **Trade-offs**: Introduced complexity, memory overhead, or vendor lock-in, and the mitigation that contains them.
   - **Neutral**: Structural shifts or secondary operational impacts.
7. **Traceability**: The `FR-xxx` and `UC-xxx` IDs the decision serves.
8. **External Docs**: Links to PRDs, benchmark reports, or external specifications.
