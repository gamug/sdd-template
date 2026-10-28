# Architecture Decision Records (ADRs)

> Output template for the root `ADR.md`, the live record of architecture
> decisions. Standalone file: unlike the other templates it is not a fragment
> of `product-template.md`. Remove this guidance block from `ADR.md`; the
> rules for proposing, validating, and superseding ADRs are in the
> constitution's "Architecture decisions" section.
>
> Discovery Phase 4 seeds `ADR.md` with every `###` block written in
> `docs/PRODUCT.md` § 5 (fragment `adr-template.md`) and keeps both in sync
> (same ID, title, and decision content) until PRODUCT.md is approved. Add
> the fields below that § 5 lacks (`Proposed on`, `Approved by`, `Approved on`,
> `Rejected by`, `Rejected on`, `Rejection reason`, `Deprecation reason`,
> `Supersedes`) to each seeded block as `N/A`. Approval then sets every seeded
> `Proposed` ADR to `Accepted` and copies PRODUCT's `Approved by` and
> `Approved on`; ADRs already `Deprecated` or `Superseded` keep their status.
> `Proposed on` is the PRODUCT approval date. If PRODUCT.md is approved but a
> seeded ADR is still `Proposed`, apply the approval to it before continuing.
> IDs use three digits. Repeat the `###` block for each decision; fields that
> do not apply hold `N/A`.

### `ADR-001`: [Concise, descriptive title]

- **Status**: [Proposed | Accepted | Rejected | Deprecated | Superseded]
- **Proposed on**: [YYYY-MM-DD]
- **Approved by**: [Name or role of the user who accepted it, or N/A]
- **Approved on**: [YYYY-MM-DD, or N/A]
- **Rejected by**: [Name or role of the user who rejected it, or N/A]
- **Rejected on**: [YYYY-MM-DD, or N/A]
- **Rejection reason**: [The user's reason, or N/A]
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
- **Rejected Options**: [Option 2 and 3: key benefits and drawbacks]
- **Traceability**: [`FR-002`, `UC-001`: only the IDs this decision serves]
- **External Docs**: [Benchmarks, framework docs, or internal spikes]
