# Architecture Decision Records (ADRs)

> Output template for the root `ADR.md`, the live record of architecture
> decisions. Standalone file: unlike the other templates it is not a fragment
> of `product-template.md`. In `ADR.md`, replace this guidance block with one
> line: "Live ADR log. Rules: the constitution's Architecture decisions
> section. Discovery snapshot: `docs/PRODUCT.md` § 5." That constitution
> section holds the rules for proposing, validating, and superseding ADRs.
>
> Discovery Phase 4 seeds `ADR.md` with every `###` block written in
> `docs/PRODUCT.md` § 5 (fragment `adr-template.md`) and keeps both in sync
> (same ID, title, and decision content) until PRODUCT.md is approved. Add
> the fields below that § 5 lacks (`Approved by`, `Approved on`, `Rejected by`,
> `Rejected on`, `Rejection reason`, `Deprecated by`, `Deprecated on`,
> `Deprecation reason`, `Supersedes`) to each seeded block as `N/A`, and set
> `Proposed on` to the date the block is written to `ADR.md`. Approval then
> sets every seeded `Proposed` ADR to `Accepted` and copies PRODUCT's
> `Approved by` and `First approved on` (as `Approved on`) to every seeded
> ADR; ADRs already `Deprecated` or `Superseded` keep their status. A later
> PRODUCT.md re-approval does not rewrite `ADR.md`. If PRODUCT.md is approved
> but a seeded ADR is still `Proposed`, apply the approval to it before
> continuing. IDs use three digits.
>
> Fields set per status; every other status-dependent field holds `N/A`:
>
> | Status | Fields set |
> | :--- | :--- |
> | Proposed | `Proposed on` |
> | Accepted | `Proposed on`, `Approved by`, `Approved on` |
> | Rejected | `Proposed on`, `Rejected by`, `Rejected on`, `Rejection reason` |
> | Deprecated | `Approved by`, `Approved on` kept, plus `Deprecated by`, `Deprecated on`, `Deprecation reason` |
> | Superseded | `Approved by`, `Approved on` kept, plus `Superseded By` (its date is the successor's `Approved on`) |
>
> Repeat the `###` block for each decision.

### `ADR-001`: [Concise, descriptive title]

- **Status**: [Proposed | Accepted | Rejected | Deprecated | Superseded]
- **Proposed on**: [YYYY-MM-DD the block was written to `ADR.md`]
- **Approved by**: [Name or role of the user who accepted it, or N/A]
- **Approved on**: [YYYY-MM-DD, or N/A]
- **Rejected by**: [Name or role of the user who rejected it, or N/A]
- **Rejected on**: [YYYY-MM-DD, or N/A]
- **Rejection reason**: [The user's reason, or N/A]
- **Deprecated by**: [Name or role of the user who deprecated it, or N/A]
- **Deprecated on**: [YYYY-MM-DD, or N/A]
- **Deprecation reason**: [Why it is no longer relevant, or N/A]
- **Supersedes**: [ADR ID, or N/A. When set, mark that ADR `Superseded` and
  put this ID in its `Superseded By`]
- **Superseded By**: [ADR ID, or N/A]
- **Context**: [Technical context, business drivers, quality attributes, and
  forces at play. Explain why a decision is needed now.]
- **Decision Drivers**:
  - **Business goal**: [e.g., minimize deployment complexity]
  - **Technical constraint**: [e.g., ecosystem compatibility]
  - **Quality attribute**: [e.g., low latency]
- **Considered Options**:
  1. [Option 1: primary choice]
  2. [Option 2: alternative]
  3. [Option 3: alternative]
- **Decision**: [Chosen option and why it beats the alternatives: benchmark
  data, team skills, or ecosystem fit]
- **Consequences (Positive)**: [Benefits of the chosen option]
- **Consequences (Trade-offs)**: [Costs of the chosen option]
- **Mitigation**: [How the trade-offs are contained]
- **Rejected Options**: [Alternatives considered and not chosen, with key
  benefits and drawbacks. Not this ADR's own rejection: see `Rejected by`]
- **Traceability**: [`FR-002`, `UC-001`: only the IDs this decision serves]
- **External Docs**: [Benchmarks, framework docs, or internal spikes]
