> Fragment for `## 5. Architecture Decision Records (ADRs)` in
> [`product-template.md`](./product-template.md). Repeat this `###` block for
> each decision. The ID stays in the heading and uses three digits; the
> validator requires Context, Decision, Consequences, and Trade-offs.
>
> In Phase 4 each block is also seeded into the root `ADR.md`, which adds the
> status, approval, and lifecycle fields only it holds (see
> `adr-log-template.md`); a section 5 block has no `Status`. Keep the ID,
> title, and decision content identical until PRODUCT.md is approved. `SKILL.md`
> Phases 4 and 6 describe the procedure.

### `ADR-001`: [Concise, descriptive title]

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
