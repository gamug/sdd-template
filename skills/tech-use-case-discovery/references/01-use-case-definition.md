# Use Case Definition & Scoping Guide

## Overview

A use case describes how an actor interacts with a system to achieve a specific goal. In the discovery phase, use cases establish functional boundaries, align business stakeholders with technical teams, and prevent scope creep.

---

## Key Components of a Use Case

1. **Title & Unique ID**: Short, verb-noun phrase representing the goal (e.g., `UC-01: Upload and Classify Spectral Data`).
2. **Primary Actor**: The user role or external system initiating the interaction.
3. **Secondary Actors**: Supporting systems, databases, or third-party services involved in fulfilling the request.
4. **Preconditions**: States or system conditions that must be true before the use case can start.
5. **Triggers**: The specific event or user action that initiates the use case.
6. **Basic Flow (Happy Path)**: The main, error-free step-by-step sequence of interactions.
7. **Alternate Flows**: Secondary paths that result in successful completion under non-standard conditions.
8. **Exception Flows**: Error paths or failure conditions, describing how the system handles errors gracefully.
9. **Postconditions**: Guaranteed state of the system after execution (both successful and failed states).

---

## Defining System Boundaries & Preventing Scope Creep

To keep discovery focused and manageable:

- **Identify System Boundaries**: Explicitly state what is inside the system boundary versus external services.
- **Differentiate In-Scope vs. Out-of-Scope**: Maintain an explicit "Out of Scope" list for Phase 1 to prevent feature bloat.
- **Validate with Stakeholders**: Ensure operations, business leads, and end-users agree on the basic flow before engineering begins.

---

## Checklist for Effective Use Cases

- [ ] Does the title use an active verb-noun format?
- [ ] Is there exactly one primary actor per use case?
- [ ] Are preconditions verifiable system states?
- [ ] Does the basic flow focus on *what* the system does rather than *how* the UI looks?
- [ ] Are exception flows specified for network, validation, and authorization failures?
- [ ] Do postconditions define the exact data state changes?
