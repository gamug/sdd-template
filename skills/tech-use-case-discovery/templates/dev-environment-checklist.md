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
