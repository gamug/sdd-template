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

The discovery process is executed in six sequential phases. For each phase, consult the referenced guide in `./references/` and generate outputs using the corresponding template in `./templates/`.

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
4. **Output format**: Use `templates/use-case-template.md`.

### Phase 2: Functional Requirements & User Stories
1. Convert high-level goals into precise functional requirements using EARS (Easy Approach to Requirements Syntax) rules (*Event-Driven*, *State-Driven*, *Ubiquitous*, *Optional*, *Unwanted*).
2. Create User Stories following the 3 C's framework (*Card, Conversation, Confirmation*): `As a [persona], I want [goal], so that [benefit]`.
3. Define testable Acceptance Criteria for every user story.
4. Apply MoSCoW prioritization (*Must have*, *Should have*, *Could have*, *Won't have*).
5. **Output format**: Use `templates/prd-user-stories-template.md`.

### Phase 3: Tech Stack Selection & Multi-Criteria Decision-Making (MCDM)
1. Evaluate candidate technologies across four key dimensions:
   - **Technical**: Performance, scalability, modularity, and system adaptability.
   - **Organizational**: Team skill alignment, maintainability, and knowledge sharing.
   - **Strategic**: Cost structure, license constraints, open-source activity, and vendor lock-in.
   - **AI Ecological Adaptability**: Compatibility with ML frameworks and LLM coding proficiency.
2. Build a Multi-Criteria Decision-Making (MCDM) matrix to score options objectively.
3. **Output format**: Use `templates/tech-stack-evaluation-matrix.md`.

### Phase 4: Architecture Decision Recording (ADR)
1. Document every significant technical choice as an Architecture Decision Record (ADR).
2. Detail the context, decision rationale, trade-offs, and positive/negative consequences.
3. Ensure bidirectional traceability between requirements and decisions.
4. **Output format**: Use `templates/adr-template.md`.

### Phase 5: Development Environment Setup
1. Define local and team developer environment standards: IDE setup, version control, language runtimes, version managers, package managers, and container isolation (e.g., Docker).
2. Set up linters, formatters, environment variable configurations (`.env.example`), and CI/CD pipelines.
3. **Output format**: Use `templates/dev-environment-checklist.md`.

### Phase 6: Feasibility, Risk Assessment & MVP Roadmap
1. Assess technical, delivery, and organizational risks; define explicit mitigation strategies.
2. Define the Minimum Viable Product (MVP) boundary and establish a phased project roadmap.
3. **Output format**: Consolidate all approved discovery decisions into
   `docs/PRODUCT.md`. Keep unresolved decisions clearly marked for user
   approval.

---

## Validation Protocol

To ensure all discovery deliverables meet quality standards and completeness rules, run the bundled validation script:

```bash
python skills/tech-use-case-discovery/scripts/validate_discovery.py docs/PRODUCT.md
```

The script verifies:
- Presence of required sections in `docs/PRODUCT.md` (Use Cases, Functional
  Requirements, Tech Stack, ADRs, Dev Environment, Risks).
- EARS syntax syntax compliance and unique Requirement IDs.
- ADR completeness (Context, Decision, Trade-offs, Consequences).
- MoSCoW priority distribution for the MVP.

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
- [use-case-template.md](templates/use-case-template.md): Template for use case specifications.
- [prd-user-stories-template.md](templates/prd-user-stories-template.md): PRD and User Stories template.
- [tech-stack-evaluation-matrix.md](templates/tech-stack-evaluation-matrix.md): Tech stack multi-criteria scoring matrix.
- [adr-template.md](templates/adr-template.md): Architecture Decision Record template.
- [dev-environment-checklist.md](templates/dev-environment-checklist.md): Dev environment setup checklist.

### Examples
- [sample-discovery-output.md](examples/sample-discovery-output.md): Full end-to-end example of a completed discovery package for an AI-powered web platform.
