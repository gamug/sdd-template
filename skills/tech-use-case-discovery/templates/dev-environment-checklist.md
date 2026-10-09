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

- [ ] Local services (if any) start with the documented command.
- [ ] Data migrations (if any) apply, and the documented health or smoke check passes.
- [ ] Test suite verified: local tests pass without errors.

---

## 6. Governance & Workflow

These answers feed the project constitution through root `config.yaml`.

- [ ] **Version control**: integration branch, whether direct commits to it are
  allowed, and the policy for unrelated work on an in-flight pull request.
- [ ] **Commits**: the hook that enforces the template's commit convention
  (Conventional Commits with the `[FR][WI][TASK]` suffix), and the secret
  scanner that hooks and CI run.
- [ ] **CI**: the ordered quality gates. They run in the inherited
  `.github/workflows/validators.yml`, which is the project's CI file.
- [ ] **Tool configuration**: the canonical configuration file per tool and the
  test layout / fixture policy.
- [ ] **Coding agent**: framework, instruction file (e.g. `CLAUDE.md`,
  `AGENTS.md`, `.github/copilot-instructions.md`), its init command, whether it
  is tracked in Git, and the files it must reference.
- [ ] **Agent limits**: changes that require approval before scope expansion,
  the destructive-history boundary, and whether agents leave the working tree
  on the pushed PR branch.
- [ ] **Naming**: established terms that must not be renamed.
- [ ] **Governance**: initial constitution version, ratification date, and
  amendment log location.
