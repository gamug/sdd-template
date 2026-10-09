# Technical Discovery Specification Package
## Application: SDSS Spectra Classifier & Web Analytics Platform

- **Project Name**: SDSS Spectra Classifier
- **Document Version**: `1.0.0`
- **Date**: 2026-10-08
- **Author**: Technical Discovery Lead
- **Status**: Approved for Build

---

## 1. Executive Summary & Vision

The SDSS Spectra Classifier is an AI-driven web application designed for astronomical researchers and data analysts to upload scientific FITS (Flexible Image Transport System) dataset files, parse spectral data, execute deep learning model inference (ResNet1D), and visualize interactive spectral flux curves with classification probabilities.

---

## 2. Use Case Specifications

### Use Case `UC-001`: Upload and Classify Spectral FITS File

- **Primary Actor**: Astronomical Researcher
- **Secondary Actor**: FastAPI Backend API, PyTorch ResNet1D Model Engine
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

**MVP Won't Have**: Batch processing of multiple FITS files in one request.

---

### User Story `US-001`: Interactive Spectral Visualization
- **As an**: Astronomical Researcher
- **I want to**: View an interactive chart of wavelength vs. flux for my uploaded dataset
- **So that**: I can visually confirm spectral line features alongside model classification results
- **Priority**: Must Have

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
| **Weighted Score Total** | -- | **81 / 85** | **59 / 85** | **49 / 85** |

**Decision**: Selected **FastAPI + PyTorch + Astropy** in Python due to complete ecosystem alignment, high performance, and minimal cross-language data conversion overhead.

---

## 5. Architecture Decision Records (ADRs)

### `ADR-001`: Use FastAPI and PyTorch in a Unified Python Runtime

- **Status**: Accepted
- **Context**: The application requires scientific data extraction from FITS files (`Astropy`, `SciPy`), deep learning inference (`PyTorch ResNet1D`), and real-time REST API serving. Cross-language IPC (e.g. Node.js calling Python scripts) introduces serialization overhead and deployment complexity.
- **Decision**: Adopt FastAPI (Python 3.12) as the unified backend framework, running model inference and data preprocessing in the same Python process.
- **Consequences (Positive)**: Zero IPC serialization overhead, unified data structures (`NumPy` arrays to `PyTorch` Tensors), rapid development cycle.
- **Consequences (Trade-offs)**: Python GIL requires process-based worker scaling (`Uvicorn` worker processes) for high-concurrency CPU tasks.

---

## 6. Development Environment Setup

- **Version Managers**: `pyenv` (Python 3.12.2), `nvm` (Node 20 LTS for frontend tools).
- **Container Isolation**: Docker Compose running local FastAPI server and PostgreSQL test instance.
- **Code Quality**: `ruff` for linting and formatting, `mypy` for static type enforcement.
- **Verification Command**:
  ```bash
  docker compose up -d
  pytest tests/
  ```

---

## 7. Risk Assessment & MVP Roadmap

### Risk Matrix

| Risk ID | Description | Impact | Probability | Score | Mitigation Plan |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `RSK-001` | Non-uniform FITS spectral sequence lengths cause tensor shape errors. | High (3) | High (3) | **9** | Implement SciPy 1D interpolation (`interp1d`) to resample all spectra to a fixed 3,500-point sequence during preprocessing. |
| `RSK-002` | Large FITS files cause memory spikes during concurrent uploads. | Medium (2) | Medium (2) | **4** | Stream file uploads to disk scratch space and enforce 50MB file size limits. |

### Phased Roadmap
- **Sprint 1 (Weeks 1-2)**: Core API routes, Astropy parser, ResNet1D model integration.
- **Sprint 2 (Weeks 3-4)**: Vanilla JS / Chart.js frontend, interactive curve visualization, end-to-end integration.
- **Sprint 3 (Weeks 5-6)**: Dockerization, CI pipeline integration, automated benchmark testing.

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
- **Approved on**: 2026-01-15
- **Approved content**: `sha256:c7397e09bb002d12d65aba4529e8cbea21512ba6b3ee78c914fe77c16e0b74ef`
