# Architecture Decision Records

> Output template for the root `ADR.md`, the live record of architecture
> decisions. Discovery Phase 4 seeds it with every `###` block of
> `docs/PRODUCT.md` § 5 (fragment [`adr-template.md`](./adr-template.md)) and
> keeps both identical until PRODUCT.md is approved; approval then sets each
> seeded ADR to `Accepted` with PRODUCT's `Approved by` and `Approved on`.
> After approval, PRODUCT.md § 5 is a frozen discovery snapshot and every new
> decision, rejection, or supersession is recorded here only.
>
> IDs use three digits, continue sequentially, and are never reused, not even
> for a rejected ADR. Status is one of `Proposed` (awaiting user validation),
> `Accepted`, `Rejected`, `Deprecated`, or `Superseded`. A change is
> implemented only after its ADR is `Accepted`. Repeat the `###` block below
> for each decision; fields that do not apply hold `N/A`.

### `ADR-001`: [Concise, descriptive title]

- **Status**: [Proposed | Accepted | Rejected | Deprecated | Superseded]
- **Approved by**: [Name or role, or N/A while Proposed or when Rejected]
- **Approved on**: [YYYY-MM-DD, or N/A while Proposed or when Rejected]
- **Rejection reason**: [The user's reason, or N/A]
- **Supersedes**: [ADR ID, or N/A]
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
- **Traceability**: `FR-002`, `FR-003`, `UC-001`
- **External Docs**: [Benchmarks, framework docs, or internal spikes]
