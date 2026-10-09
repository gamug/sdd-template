# Technical Discovery Specification Package
## Application: SDSS Spectra Classifier & Web Analytics Platform

- **Project Name**: SDSS Spectra Classifier
- **Document Version**: `1.0.0`
- **Author**: Technical Discovery Lead

---

## 1. Executive Summary & Vision

- **Problem Statement**: Astronomical researchers and data analysts need to classify stellar spectra from SDSS FITS (Flexible Image Transport System) files and confirm the result against the spectrum itself.
- **Vision**: An AI-driven web application where users upload FITS files, the system parses the spectral data, runs deep learning inference (ResNet1D), and shows an interactive spectral flux curve with classification probabilities.
- **Success Metrics**: Flux and wavelength data extracted within 1.5 seconds of an upload (`FR-002`); every classification returned as structured JSON with category and confidence scores (`FR-003`).
- **Personas**: Astronomical Researcher and Data Analyst: upload FITS files, review classifications, and confirm spectral features visually.

---

## 2. Use Case Specifications

### Use Case `UC-001`: Upload and Classify Spectral FITS File

- **Primary Actor**: Astronomical Researcher
- **Secondary Actors**: FastAPI Backend API, PyTorch ResNet1D Model Engine
- **Brief Description**: The researcher uploads a FITS spectrum and receives its star class with confidence scores next to an interactive chart of the spectrum.
- **Preconditions**: User is logged in and on the web classification dashboard.
- **Triggers**: User selects a `.fits` file and clicks "Analyze Spectrum".

#### Basic Flow (Happy Path)
1. User drops a `.fits` dataset file (up to 50MB) into the upload zone.
2. System validates file format (`.fits` header compliance).
3. Backend extracts wavelength ($\text{\AA}$) and flux vectors using `Astropy` and `SciPy` interpolation.
4. ResNet1D model executes inference and generates Softmax class probability distribution (F, G, K star types).
5. Web interface renders the interactive spectral line chart (Chart.js) alongside classification confidence scores.

#### Exception Flow `UC-001-EX1`: Invalid File Format
1. At step 2, if file format is invalid, system logs validation failure.
2. System displays error toast: *"Invalid file type. Please upload a compliant SDSS .fits file."*
3. Upload process terminates safely without backend processing.

#### Postconditions
- **Success**: The spectrum's class probabilities and interactive chart are shown to the user.
- **Failure**: No backend processing runs, and the user sees the validation error (`UC-001-EX1`).

---

## 3. Functional Requirements & User Stories

### Functional Requirements (EARS Syntax)

| Requirement ID | EARS Pattern | Statement | MoSCoW Priority | Traceability |
| :--- | :--- | :--- | :--- | :--- |
| `FR-002` | Event-Driven | WHEN a user uploads a `.fits` file, the system shall extract flux and wavelength data within 1.5 seconds. | Must Have | `UC-001` |
| `FR-003` | Ubiquitous | The backend shall return all classification responses in structured JSON format containing category and confidence scores. | Must Have | `UC-001` |
| `FR-004` | State-Driven | WHILE deep learning inference is executing, the UI shall display a responsive spinner indicator. | Should Have | `UC-001` |
| `FR-005` | Optional | WHERE GPU acceleration is present, the inference service shall utilize CUDA tensor processing. | Could Have | `UC-001` |
| `FR-006` | Unwanted / Error | IF the file payload exceeds 50MB, THEN the system shall return an HTTP 413 error message. | Must Have | `UC-001` |

- **MVP Won't Have**: Batch processing of multiple FITS files in one request.

### User Story `US-001`: Interactive Spectral Visualization

- **Card**: As an astronomical researcher, I want to view an interactive chart of wavelength vs. flux for my uploaded dataset, so that I can visually confirm spectral line features alongside model classification results.
- **Priority**: Must Have
- **Traceability**: `FR-002`, `FR-003`, `UC-001`

#### Acceptance Criteria (Given-When-Then)
```gherkin
SCENARIO: Interactive chart rendering
  GIVEN a valid FITS file has been processed by the backend
  WHEN the classification response payload is received by the browser
  THEN the UI shall render a dynamic line chart with zoom and pan enabled
  AND display the predicted star class (F, G, or K) with confidence percentage.
```

---

## 4. Technology Stack Selection & MCDM Matrix

### Multi-Criteria Decision-Making (MCDM) Evaluation

Evaluating Backend API Framework Options:

| Evaluation Criteria | Weight (1-5) | Option A: FastAPI (Python) | Option B: Express (Node.js) | Option C: Spring Boot (Java) |
| :--- | :---: | :---: | :---: | :---: |
| **Unified AI/ML Ecosystem** | 5 | 5 (PyTorch/Astropy native) | 2 (Requires IPC calls) | 2 (Requires JNI wrapper) |
| **Async Request Performance** | 4 | 4 (ASGI / Uvicorn) | 4 (Event loop) | 4 (Netty async) |
| **Team Skill Alignment** | 4 | 5 (High Python fluency) | 3 (Moderate) | 2 (Low Java fluency) |
| **AI Coding Proficiency (LLM Support)**| 4 | 5 (Extensive LLM training data)| 5 (High) | 4 (High) |
| **Weighted Score Total** | -- | **81 / 85** | **58 / 85** | **50 / 85** |

**Decision**: Selected **FastAPI + PyTorch + Astropy** in Python due to complete ecosystem alignment, high performance, and minimal cross-language data conversion overhead.

---

## 5. Architecture Decision Records (ADRs)

### `ADR-001`: Use FastAPI and PyTorch in a Unified Python Runtime

- **Status**: Accepted
- **Context**: The application requires scientific data extraction from FITS files (`Astropy`, `SciPy`), deep learning inference (`PyTorch ResNet1D`), and real-time REST API serving. Cross-language IPC (e.g. Node.js calling Python scripts) introduces serialization overhead and deployment complexity.
- **Decision**: Adopt FastAPI (Python 3.12) as the unified backend framework, running model inference and data preprocessing in the same Python process.
- **Consequences (Positive)**: Zero IPC serialization overhead, unified data structures (`NumPy` arrays to `PyTorch` Tensors), rapid development cycle.
- **Consequences (Trade-offs)**: Python GIL requires process-based worker scaling (`Uvicorn` worker processes) for high-concurrency CPU tasks.
- **Traceability**: `FR-002`, `FR-003`, `UC-001`

---

## 6. Development Environment Setup

- **Target platforms**: Linux and macOS.
- **Source hosting**: Git hosted on GitHub; contributors authenticate over SSH.
- **Runtimes and version managers**: `pyenv` (Python 3.12.2), `nvm` (Node 20 LTS for frontend tools).
- **Environment isolation**: Docker Compose running the local FastAPI server and a PostgreSQL test instance.
- **Local services**: PostgreSQL test instance, started with `docker compose up -d`.
- **Editor configuration**: Shared `.vscode/settings.json` and recommended extensions for Python, Ruff, and Docker.
- **Configuration variables**: `.env.example` lists every required key; local values live in `.env`, which stays out of Git.
- **Code quality**: `ruff` for linting and formatting, `mypy` for static type enforcement.
- **Verification command**:
  ```bash
  docker compose up -d
  pytest tests/
  ```

---

## 7. Risk Assessment & MVP Roadmap

### Risk Matrix

Impact and Probability use 1 (Low) to 3 (High); Score = Impact × Probability.
A score of 6 or more requires a mitigation plan.

| Risk ID | Description | Impact | Probability | Score | Mitigation Plan |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `RSK-001` | Non-uniform FITS spectral sequence lengths cause tensor shape errors. | High (3) | High (3) | **9** | Implement SciPy 1D interpolation (`interp1d`) to resample all spectra to a fixed 3,500-point sequence during preprocessing. |
| `RSK-002` | Large FITS files cause memory spikes during concurrent uploads. | Medium (2) | Medium (2) | **4** | Stream file uploads to disk scratch space and enforce 50MB file size limits. |

### Phased Roadmap

- **MVP**: the three sprints below.
  - **Sprint 1 (Weeks 1-2)**: Core API routes, Astropy parser, ResNet1D model integration.
  - **Sprint 2 (Weeks 3-4)**: Vanilla JS / Chart.js frontend, interactive curve visualization, end-to-end integration.
  - **Sprint 3 (Weeks 5-6)**: Dockerization, CI pipeline integration, automated benchmark testing.
- **Next phases**: Batch processing of multiple FITS files (MVP Won't Have).

---

## 8. Governance & Workflow

- **Version control**: integration branch `main`; no direct commits to it. Unrelated work on an in-flight pull request goes to a new branch after asking the user.
- **Commits**: Conventional Commits, enforced by `commitizen`; hooks and CI scan for secrets with `gitleaks`.
- **CI**: `.github/workflows/validators.yml` (inherited from the template) also runs `ruff check`, `ruff format --check`, `mypy`, and `pytest -q`, in that order.
- **Tool configuration**: `pyproject.toml` is the single configuration for `ruff`, `mypy`, and `pytest`; tests mirror `src/` under `tests/` and stay hermetic.
- **Coding agent**: Claude Code, instruction file `CLAUDE.md` (created with `/init`, tracked in Git), which must reference `.sdd/constitution.md` and `.sdd/SPEC.md`.
- **Agent limits**: new external services, new heavy dependencies, and storage schema changes require approval; never rewrite history already pushed to `main`. Agents leave the working tree on the pushed PR branch.
- **Naming**: "spectrum" for an uploaded FITS observation; "classification" for a model prediction.
- **Governance**: constitution version `1.0.0`, ratified on approval; amendments are logged in `.sdd/CHANGELOG.md`.

---

## 9. Approval

- **Approved by**: Product Owner (example)
- **First approved on**: 2026-01-15
- **Approved on**: 2026-01-15
- **Approved content**: `sha256:7d9c6c655596f4f57a6f8d6e80667557620feb4e8f4c187067247e3147096b26`
