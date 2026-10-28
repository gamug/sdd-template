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

This is a conceptual outline; the templates (`templates/adr-log-template.md` for `ADR.md`, `templates/adr-template.md` for section 5) list the exact fields, including `Decision Drivers` and `Mitigation`.

1. **Title & Number**: Sequential identifier and clear summary (e.g., `ADR-001: Use FastAPI for Asynchronous Backend API`).
2. **Status and dates** (in `ADR.md`; a section 5 block carries only the content fields below): Current lifecycle state (*Proposed*, *Accepted*, *Rejected*, *Deprecated*, *Superseded*), `Proposed on`, and the fields of the state it reached: `Approved by` and `Approved on`; `Rejected by`, `Rejected on` and `Rejection reason`; `Deprecated by`, `Deprecated on` and `Deprecation reason`. `Supersedes` on the new ADR names the ADR(s) it replaces; `Superseded By` on the replaced ADR names the new one. Fields that do not apply hold `N/A`.
3. **Context**: The business problem, technical constraints, quality attribute requirements, and forces at play.
4. **Decision**: Explicit statement of the chosen solution and architectural pattern.
5. **Considered Options / Rejected Options**: Alternatives the decision weighed and did not choose, with pros/cons for each and why they lost. This is not the ADR's own rejection (see *Rejected* above).
6. **Consequences**:
   - **Positive**: Expected performance, developer speed, or maintainability gains.
   - **Trade-offs**: Introduced complexity, memory overhead, or vendor lock-in, and the mitigation that contains them.
   - **Neutral**: Structural shifts or secondary operational impacts.
7. **Traceability**: The `FR-xxx` and `UC-xxx` IDs the decision serves.
8. **External Docs**: Links to PRDs, benchmark reports, or external specifications.

---

## Where ADRs Live

- **`docs/PRODUCT.md` section 5** holds the ADRs written during discovery. It is covered by the approval hash and is a frozen snapshot after approval.
- **`ADR.md` in the project root** is the live record. Discovery Phase 4 seeds it from section 5 (every ADR as `Proposed`, built from `templates/adr-log-template.md`), and the approval of `docs/PRODUCT.md` accepts the seeded ADRs. After that, every new, rejected, deprecated, or superseded decision is recorded in `ADR.md` only, and a changed decision is recorded as a new ADR that supersedes the old one (an accepted ADR is not rewritten); section 5 is not edited and `docs/PRODUCT.md` is not re-approved for it.
- The scripts check section 5 (Context, Decision, Consequences, Trade-offs) but not `ADR.md`; Phase 6 step 5 of `SKILL.md` (reconcile with section 5, accept, re-read) is its check.

---

## User Validation of a New ADR

After initialization, the constitution's "Architecture decisions" section governs every architecture change; if this guide and that section differ, the constitution governs. In outline: the agent adds a new ADR to `ADR.md` as `Proposed`, presents it, and stops; the user's explicit decision accepts or rejects it; and only an accepted ADR is implemented.

The decision belongs to the user because an architecture change is costly to reverse and an agent must not approve its own proposal. That is also why `Approved by` and `Rejected by` record the name or role the user gave, never the agent.

---

## Keeping the Field Lists in Step

The ADR fields are listed in several places: `templates/adr-log-template.md`, the seeding step in `SKILL.md` (Phase 4 step 5), the constitution's "Architecture decisions" section, and the Anatomy above. The content fields shared with section 5 (`Context`, `Decision`, `Consequences`, `Traceability`, and so on) also appear in `templates/adr-template.md` and the ADR block of `templates/product-template.md`. When a field is added, renamed, or removed, change every list that names it together.
