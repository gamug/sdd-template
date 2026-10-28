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

- **Proposed**: Under review by the user. Nothing that depends on it is implemented.
- **Accepted**: Approved by the user and active design guidance for the team.
- **Rejected**: Declined by the user. It stays in `ADR.md` with who rejected it, when, and why; the change is not implemented. A rejected ADR is never reopened: revisiting the idea needs a new ADR with a new ID.
- **Deprecated**: Decision is no longer relevant due to scope or technology shifts. Needs an explicit user decision, with who, when, and why recorded.
- **Superseded**: Replaced by a newer ADR (must include a link to the replacing ADR ID).

Allowed moves: `Proposed` to `Accepted` or `Rejected`, and `Accepted` to `Deprecated` or `Superseded`.

---

## Anatomy of an ADR

1. **Title & Number**: Sequential identifier and clear summary (e.g., `ADR-001: Use FastAPI for Asynchronous Backend API`).
2. **Status and dates**: Current lifecycle state (*Proposed*, *Accepted*, *Rejected*, *Deprecated*, *Superseded*), `Proposed on`, and the fields of the state it reached: `Approved by` and `Approved on`; `Rejected by`, `Rejected on` and `Rejection reason`; `Deprecated by`, `Deprecated on` and `Deprecation reason`. `Supersedes` and `Superseded By` link a replacement to the ADR it replaces. Fields that do not apply hold `N/A`.
3. **Context**: The business problem, technical constraints, quality attribute requirements, and forces at play.
4. **Decision**: Explicit statement of the chosen solution and architectural pattern.
5. **Considered Options / Rejected Options**: Evaluated options with pros/cons analysis for each, and why the rejected ones lost.
6. **Consequences**:
   - **Positive**: Expected performance, developer speed, or maintainability gains.
   - **Trade-offs**: Introduced complexity, memory overhead, or vendor lock-in, and the mitigation that contains them.
   - **Neutral**: Structural shifts or secondary operational impacts.
7. **Traceability**: The `FR-xxx` and `UC-xxx` IDs the decision serves.
8. **External Docs**: Links to PRDs, benchmark reports, or external specifications.

---

## Where ADRs Live

- **`docs/PRODUCT.md` section 5** holds the ADRs written during discovery. It is covered by the approval hash and is a frozen snapshot after approval.
- **`ADR.md` in the project root** is the live record. Discovery Phase 4 seeds it from section 5 (every ADR as `Proposed`, built from `templates/adr-log-template.md`), and the approval of `docs/PRODUCT.md` accepts the seeded ADRs. After that, every new, changed, rejected, deprecated, or superseded decision is recorded in `ADR.md` only; section 5 is not edited and `docs/PRODUCT.md` is not re-approved for it.
- The scripts check section 5 (Context, Decision, Consequences, Trade-offs) but not `ADR.md`; Phase 6 step 5 of `SKILL.md` (reconcile with section 5, accept, re-read) is its check.

---

## User Validation of a New ADR

After initialization, the constitution's "Architecture decisions" rule governs every architecture change:

1. Add a new ADR to `ADR.md` as `Proposed` and present it to the user. Do not implement the change, or work that depends on it, until the user decides.
2. The decision is an explicit user instruction. If the user approves, set `Accepted` and record the name or role the user gave in `Approved by` and the date in `Approved on`, then implement. If the user rejects, set `Rejected` and record `Rejected by`, `Rejected on`, and `Rejection reason`; do not implement.
3. If the ADR replaces an earlier one, name it in `Supersedes`; once the new ADR is `Accepted`, mark the earlier ADR `Superseded` and record the new ID in its `Superseded By`, in the same change.
4. IDs have three digits, continue after the highest existing ID, and are never reused.

---

## Keeping the Field Lists in Step

The ADR fields are listed in three places: `templates/adr-log-template.md`, the seeding step in `SKILL.md` (Phase 4 step 5), and the constitution's "Architecture decisions" section. When a field is added, renamed, or removed, change all three together.
