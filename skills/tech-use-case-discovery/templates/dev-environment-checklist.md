# Local Development Environment Setup Checklist

## Project Metadata
- **Project Title**: [Project Name]
- **Target Platforms**: Linux / macOS / Windows (WSL2)

---

## 1. Prerequisites and Tools

- [ ] **Git Configuration**:
  - Version control installed and configured with SSH keys.
- [ ] **Runtime Managers**:
  - Python version manager (`pyenv` with Python 3.12).
  - Node.js version manager (`nvm` with Node 20 LTS).
- [ ] **Container Engine**:
  - Docker and Docker Compose installed for local services.

---

## 2. Editor Configuration

- [ ] **Workspace Settings**:
  - Project configuration saved in workspace settings.
- [ ] **Extensions**:
  - Linters, formatters, and language support tools enabled.

---

## 3. Configuration Variables

- [ ] `.env.example` created with required variable keys.
- [ ] Local `.env` file populated and added to `.gitignore`.

---

## 4. Code Quality & Pre-commit Tools

- [ ] Code linters and formatters installed.
- [ ] Pre-commit validation active.

---

## 5. Local Services & Verification

- [ ] Local services started: `docker compose up -d`
- [ ] Database migration and health check validated: `GET /health` returns success.
- [ ] Test suite verified: local tests pass without errors.

---

## 6. Governance & Workflow

These answers feed the project constitution through root `config.yaml`.

- [ ] **Version control**: integration branch, whether direct commits to it are
  allowed, and the policy for unrelated work on an in-flight pull request.
- [ ] **Commits**: commit convention (e.g. Conventional Commits) and the hook
  that enforces it.
- [ ] **CI**: workflow file and the ordered quality gates it runs.
- [ ] **Tool configuration**: the canonical configuration file per tool and the
  test layout / fixture policy.
- [ ] **Coding agent**: framework, instruction file (e.g. `CLAUDE.md`,
  `AGENTS.md`, `.github/copilot-instructions.md`), its init command, whether it
  is tracked in Git, and the files it must reference.
- [ ] **Agent limits**: changes that require approval before scope expansion,
  and the destructive-history boundary.
- [ ] **Naming**: established terms that must not be renamed.
- [ ] **Governance**: initial constitution version, ratification date, and
  amendment log location.
