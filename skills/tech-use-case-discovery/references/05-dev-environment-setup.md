# Development Environment Setup Guide

## Overview

A well-configured development environment ensures developer productivity, eliminates "it works on my machine" inconsistencies, and accelerates onboarding.

---

## Core Components of a Modern Dev Environment

### 1. Code Editor / IDE Configuration
- **IDE Choice**: VS Code, Cursor, JetBrains (IntelliJ / PyCharm).
- **Core Extensions**: Language servers, linters, formatters, and Git integration plugins.
- **Shared Settings**: Version-controlled workspace configurations (`.vscode/settings.json`).

### 2. Version Control & Repository Setup
- **Git Protocol**: SSH key authentication, signed commits (`gpg` / `ssh`).
- **Branching Strategy**: Trunk-based development or GitFlow (`main`, `feature/*`, `release/*`).
- **Hooks**: Pre-commit hooks (`pre-commit`, `husky`) for code formatting and linting before commits.

### 3. Runtime & Tool Version Management
- Use version managers to isolate language runtimes across projects:
  - **Python**: `pyenv` or `conda`
  - **Node.js**: `nvm` or `fnm`
  - **Ruby / Go / Java**: `asdf` or `mise`
- Specify runtime versions in root dotfiles (`.python-version`, `.nvmrc`).

### 4. Container Isolation & Local Dependencies
- When the project needs local services (databases, caches, microservices), isolate them, for example with **Docker Compose**; a devcontainer, host-only, or no-container setup is equally valid when the project calls for it.
- When containers are used, keep the local service topology close to production (e.g., PostgreSQL, Redis, local S3 mock).

### 5. Environment Variables & Secret Safety
- Maintain a version-controlled `.env.example` file documenting all required configuration keys.
- **NEVER** commit secrets or real `.env` files to git repositories. Use secret management tools (`dotenv-cli`, `1Password CLI`, `Vault`) for local secret injection.

### 6. Linting, Formatting, and Static Analysis
- **Python**: `ruff`, `black`, `mypy`.
- **JavaScript/TypeScript**: `eslint`, `prettier`, `tsc`.
- Ensure automated execution via pre-commit hooks and CI pipelines.
