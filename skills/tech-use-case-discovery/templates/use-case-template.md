# Use Case Specification Template

## Document Metadata
- **Project Name**: [Project Title]
- **Use Case ID**: `UC-[Number]`
- **Use Case Title**: [Active Verb + Noun Phrase]
- **Author**: [Name / Role]
- **Status**: [Draft / In Review / Approved]
- **Last Updated**: [YYYY-MM-DD]

---

## 1. Overview
- **Primary Actor**: [User Role / External System initiating the action]
- **Secondary Actors**: [Supporting systems, databases, third-party APIs]
- **Brief Description**: [2-3 sentences explaining the user goal and expected outcome]

---

## 2. Conditions & Triggers
- **Preconditions**:
  - [Precondition 1: e.g., User must be authenticated with valid role]
  - [Precondition 2: e.g., System has active database connection]
- **Triggers**:
  - [Event initiating the use case: e.g., User clicks 'Upload Dataset']

---

## 3. Flow of Events

### Basic Flow (Happy Path)
1. The [Primary Actor] initiates [Action].
2. The System validates [Inputs/Preconditions].
3. The System processes [Data/Logic].
4. The System displays [Output/Confirmation].
5. The Primary Actor confirms [Completion].

### Alternate Flows
- **Alt-1: [Descriptive Title]**
  - At step [X] of Basic Flow, if [Condition]:
  - 1. The System executes [Alternative Step].
  - 2. Rejoins Basic Flow at step [Y].

### Exception Flows
- **Ex-1: [Error Condition Title]**
  - At step [X] of Basic Flow, if [Error occurs]:
  - 1. The System logs [Error Details].
  - 2. The System displays error message: "[User-friendly error]".
  - 3. Use case ends in failed state without data corruption.

---

## 4. Postconditions
- **Success Postconditions**: [Guaranteed system state upon successful completion]
- **Failure Postconditions**: [Guaranteed system state if execution fails]

---

## 5. Non-Functional Constraints
- **Performance**: [e.g., Execution must complete within 2.0 seconds]
- **Security**: [e.g., Data in transit must be TLS 1.3 encrypted]
