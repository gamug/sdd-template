---
name: tech-use-case-discovery
description: Guides users through the software development discovery phase. Assists in defining use cases, functional requirements, technology stack selection, Architecture Decision Records (ADRs), development environment setup, and risk/roadmap planning. Use when taking a project idea from concept to a complete technical specification.
---

# Tech Use Case Discovery Skill

This Skill provides a structured, interactive workflow to guide users through the entire software discovery phase. It transforms an initial application idea into a build-ready technical specification package, preventing scope creep, technical debt, and architectural misalignment.

---

## Required Project Inputs

Before initiating the discovery workflow, gather the following initial inputs from the user (or prompt for them iteratively during Phase 1):

| Input Domain | Key Questions / Context Needed |
| :--- | :--- |
| **Problem & Vision** | What core problem does the application solve? What is the vision and business goal? |
| **Target Users & Actors** | Who will use or interact with the system (end-users, admins, external APIs)? |
| **Core Capabilities** | What are the primary high-level features or operations expected? |
| **Quality Attributes** | What are key non-functional constraints (performance, security, concurrency, compliance)? |
| **Organizational Context** | What is the team's experience, budget horizon, and timeline? |
| **Ecosystem & AI Scope** | Will the app integrate AI/ML models, external LLMs, or legacy systems? |

---

## Step-by-Step Discovery Workflow

The discovery process is executed in six sequential phases and produces one document, `docs/PRODUCT.md`, built from [`templates/product-template.md`](templates/product-template.md). For each phase, consult the referenced guide in `./references/` and fill the matching numbered section of the product template using the phase's fragment in `./templates/`. Every ID uses three digits (`UC-001`, `FR-002`, `US-001`, `ADR-001`, `RSK-001`), sits in the item's heading or the first table column, and is defined once.

```
  ┌───────────────────────────────┐
  │  Phase 1: Use Case Definition │ ──> See references/01-use-case-definition.md
  └──────────────┬────────────────┘
                 │
                 ▼
  ┌───────────────────────────────┐
  │ Phase 2: Requirements & Stories│ ──> See references/02-functional-requirements.md
  └──────────────┬────────────────┘
                 │
                 ▼
  ┌───────────────────────────────┐
  │ Phase 3: Tech Stack Selection │ ──> See references/03-tech-stack-selection.md
  └──────────────┬────────────────┘
                 │
                 ▼
  ┌───────────────────────────────┐
  │  Phase 4: Architectural ADRs  │ ──> See references/04-architecture-decision-records.md
  └──────────────┬────────────────┘
                 │
                 ▼
  ┌───────────────────────────────┐
  │ Phase 5: Dev Environment Setup│ ──> See references/05-dev-environment-setup.md
  └──────────────┬────────────────┘
                 │
                 ▼
  ┌───────────────────────────────┐
  │ Phase 6: Risk & MVP Roadmap   │ ──> See references/06-risk-and-roadmap.md
  └───────────────────────────────┘
```

### Phase 1: Use Case Definition & Scoping
1. Conduct user/actor discovery to identify all primary, secondary, and system actors.
2. Draft structured use cases covering Preconditions, Basic Flow, Alternate/Exception Flows, and Postconditions.
3. Establish clear boundaries to eliminate out-of-scope feature bloat.
4. **Output format**: Section 2 of the product template, one block per use case from `templates/use-case-template.md`.

### Phase 2: Functional Requirements & User Stories
1. Convert high-level goals into precise functional requirements using EARS (Easy Approach to Requirements Syntax) rules (*Event-Driven*, *State-Driven*, *Ubiquitous*, *Optional*, *Unwanted*).
   `FR-001` is reserved for the SDD initialization requirement: number product
   requirements from `FR-002`.
2. Create User Stories following the 3 C's framework (*Card, Conversation, Confirmation*): `As a [persona], I want [goal], so that [benefit]`.
3. Define testable Acceptance Criteria for every user story.
4. Apply MoSCoW prioritization (*Must have*, *Should have*, *Could have*, *Won't have*).
5. **Output format**: Section 3 of the product template, from `templates/prd-user-stories-template.md`.

### Phase 3: Tech Stack Selection & Multi-Criteria Decision-Making (MCDM)
1. Evaluate candidate technologies across four key dimensions:
   - **Technical**: Performance, scalability, modularity, and system adaptability.
   - **Organizational**: Team skill alignment, maintainability, and knowledge sharing.
   - **Strategic**: Cost structure, license constraints, open-source activity, and vendor lock-in.
   - **AI Ecological Adaptability**: Compatibility with ML frameworks and LLM coding proficiency.
2. Build a Multi-Criteria Decision-Making (MCDM) matrix to score options objectively.
3. **Output format**: Section 4 of the product template, from `templates/tech-stack-evaluation-matrix.md`.

### Phase 4: Architecture Decision Recording (ADR)
1. Document every significant technical choice as an Architecture Decision Record (ADR).
2. Detail the context, decision rationale, trade-offs, and positive/negative consequences.
3. Ensure bidirectional traceability between requirements and decisions.
4. **Output format**: Section 5 of the product template, one block per decision from `templates/adr-template.md`.

### Phase 5: Development Environment Setup
1. Define local and team developer environment standards: IDE setup, version control, language runtimes, version managers, package managers, and container isolation (e.g., Docker).
2. Set up linters, formatters, environment variable configurations (`.env.example`), and CI/CD pipelines.
3. Record the repository governance and workflow decisions the project
   constitution needs: integration branch and commit policy, the commit hook and
   secret scanner, CI gate order (run in the inherited `validators.yml`),
   canonical tool configuration, the coding-agent framework and its instruction
   file, scope-expansion approvals, whether agents leave the working tree on the
   pushed PR branch, and the initial governance version.
4. **Output format**: Sections 6 and 8 of the product template, from `templates/dev-environment-checklist.md`.

### Phase 6: Feasibility, Risk Assessment & MVP Roadmap
1. Assess technical, delivery, and organizational risks in the risk matrix
   (`RSK-001`, …): Score = Impact × Probability on 1-3 scales, and every score
   of 6 or more needs a mitigation plan.
2. Define the Minimum Viable Product (MVP) boundary and establish a phased project roadmap.
3. **Output format**: Section 7 of the product template. `docs/PRODUCT.md`
   now holds every phase's decisions, including `## 8. Governance & Workflow`
   from Phase 5. Mark every open decision with a line containing
   `UNRESOLVED:` and the question to ask.
4. **Approval**: Resolve every `UNRESOLVED:` item with the user, then close
   the approved content of `docs/PRODUCT.md` with an `## Approval` section
   (`validate_config.py scaffold` later appends `## Configuration Decisions`
   after it) containing `Approved by: <name or role>`,
   `First approved on: YYYY-MM-DD`, `Approved on: YYYY-MM-DD`, and
   `Approved content: <hash>`, where `<hash>`
   is the output of `validate_discovery.py --hash docs/PRODUCT.md` for the
   version the user approved. Any later edit outside the Approval and
   Configuration Decisions sections fails validation until the user approves
   again; a re-approval updates `Approved on` and the hash and keeps
   `First approved on`. Configuration
   (WI-002) cannot start until this validates.

---

## Validation Protocol

To ensure all discovery deliverables meet quality standards and completeness rules, run the bundled validation script:

```bash
# While writing PRODUCT.md (approval not required yet)
python skills/tech-use-case-discovery/scripts/validate_discovery.py --draft docs/PRODUCT.md
# After user approval: print the hash to record as "Approved content"
python skills/tech-use-case-discovery/scripts/validate_discovery.py --hash docs/PRODUCT.md
# Then validate the approved document (required before WI-002)
python skills/tech-use-case-discovery/scripts/validate_discovery.py docs/PRODUCT.md
```

The script verifies:
- Presence of required sections in `docs/PRODUCT.md` (Use Cases, Functional
  Requirements, User Stories, Tech Stack, ADRs, Dev Environment, Risks,
  Governance & Workflow).
- EARS syntax compliance, product requirements numbered from `FR-002`
  (`FR-001` is reserved for initialization), and three-digit FR, UC, US, ADR,
  and RSK IDs that are each defined once. FR rows define requirements only in
  the Functional Requirements section and RSK rows only in the Risk section;
  elsewhere (e.g. a traceability matrix) they are references.
- ADR completeness (Context, Decision, Trade-offs, Consequences).
- The risk matrix: at least one `RSK-xxx` row, Score = Impact × Probability on
  1-3 scales, and a mitigation plan for every score of 6 or more.
- MoSCoW: every FR and user story has exactly one valid priority, at least
  one is Must Have, and Won't Have is stated (as a priority or a
  `Won't Have:` line).
- Each FR's EARS pattern column matches its statement (WHEN, WHILE, WHERE,
  IF … THEN, or none for Ubiquitous), and every referenced ID is defined.
- No template `[...]` placeholders are left outside code (a warning with
  `--draft`). Links, task boxes, numeric citations (`[1]`, `[1, 2]`,
  `[1-3]`), and footnotes (`[^1]`) are not placeholders.
- User approval: an `Approval` section with an approver that is not a
  template placeholder, real `First approved on` and `Approved on` dates (the
  first no later than the second), and a content hash on their own lines that
  matches the current document, and no remaining `UNRESOLVED:` markers
  (skipped with `--draft`).

Lines starting with `>` are template guidance: every content check skips
them, but the approval hash covers them.

When validating from a directory, pass the project root or a directory that
contains exactly one generated `PRODUCT.md`; bundled templates, references,
and examples are not discovery output and are not aggregated.

---

## Reference & Template Index

### Reference Documentation
- [01-use-case-definition.md](references/01-use-case-definition.md): Use case scoping, actor identification, and boundary setting.
- [02-functional-requirements.md](references/02-functional-requirements.md): EARS syntax, User Stories (3 C's), acceptance criteria, and MoSCoW prioritization.
- [03-tech-stack-selection.md](references/03-tech-stack-selection.md): Multi-Criteria Decision-Making (MCDM) framework across technical, organizational, strategic, and AI dimensions.
- [04-architecture-decision-records.md](references/04-architecture-decision-records.md): ADR lifecycle, structure, and traceability management.
- [05-dev-environment-setup.md](references/05-dev-environment-setup.md): Local dev environment, runtimes, containers, code quality tools, and CI/CD.
- [06-risk-and-roadmap.md](references/06-risk-and-roadmap.md): Feasibility analysis, risk matrices, and MVP roadmap planning.

### Templates
- [product-template.md](templates/product-template.md): The `docs/PRODUCT.md` structure; it passes `validate_discovery.py --draft`.
- [use-case-template.md](templates/use-case-template.md): Fragment for section 2, one block per use case.
- [prd-user-stories-template.md](templates/prd-user-stories-template.md): Fragment for section 3, requirements and user stories.
- [tech-stack-evaluation-matrix.md](templates/tech-stack-evaluation-matrix.md): Fragment for section 4, the MCDM matrix.
- [adr-template.md](templates/adr-template.md): Fragment for section 5, one block per ADR.
- [dev-environment-checklist.md](templates/dev-environment-checklist.md): Fragments for sections 6 and 8, environment and governance decisions.

### Examples
- [sample-discovery-output.md](examples/sample-discovery-output.md): Full end-to-end example of a completed discovery package for an AI-powered web platform.
