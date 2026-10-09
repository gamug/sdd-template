# Risk Assessment & MVP Roadmap Planning Guide

## Overview

Technical discovery de-risks software development by identifying technical, operational, and delivery bottlenecks before writing code. This phase establishes a phased delivery roadmap with realistic MVP boundaries.

---

## 1. Risk Assessment Framework

Risks are categorized into three domains:

| Risk Category | Description | Typical Examples | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Technical Risk** | Feasibility, legacy integration, or performance bottlenecks. | *Legacy database cannot support concurrent real-time query load.* | *Implement Redis caching layer and read-replicas.* |
| **Delivery Risk** | Dependencies on third-party APIs, vendor stability, or licensing. | *Third-party AI API has strict rate limits and variable latency.* | *Build async queue worker architecture with local fallback models.* |
| **Organizational Risk** | Team capacity, skill gaps, or domain compliance requirements. | *Team lacks deep PyTorch/GPU optimization experience.* | *Conduct technical spikes in Sprint 0 and use pre-trained model APIs.* |

### Risk Matrix Scoring
Give each risk a three-digit ID (`RSK-001`, `RSK-002`, …) and a row in the
risk matrix with the columns
`| Risk ID | Description | Impact | Probability | Score | Mitigation Plan |`:
- **Impact**: Low (1), Medium (2), High (3)
- **Probability**: Low (1), Medium (2), High (3)
- **Score**: Impact × Probability. A score of 6 or more requires a mitigation
  plan before Sprint 1.

`validate_discovery.py` enforces the ID format, the score arithmetic, and the
mitigation plan for scores of 6 or more.

---

## 2. MVP Scope Definition & Phased Roadmap

### MVP Definition Guidelines
- Include **ONLY** items classified as **Must Have** in the MoSCoW prioritization.
- Focus on end-to-end core user value rather than exhaustive feature coverage.
- Establish clear success metrics and feedback loops for the MVP release.

### Phased Roadmap Structure
1. **Phase 0: Discovery & Technical Spikes (Weeks 1–3)**: Finalize architecture, setup dev environments, conduct POC spikes on high-risk components.
2. **Phase 1: MVP Core Build (Weeks 4–10)**: Implement core use cases, primary API endpoints, and essential UI flows.
3. **Phase 2: Enhanced Capabilities (Weeks 11–16)**: Add secondary features, automated analytics, and advanced UI visualizations.
4. **Phase 3: Scale & Optimization (Ongoing)**: Performance tuning, horizontal scaling, and enterprise compliance integrations.
