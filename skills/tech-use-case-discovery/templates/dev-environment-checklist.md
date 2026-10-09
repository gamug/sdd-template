> Fragments for two sections of [`product-template.md`](./product-template.md):
> `## 6. Development Environment Setup` and `## 8. Governance & Workflow`.
> Replace each bracket with the decision the user made, or a line containing
> `UNRESOLVED:` and the question to ask. Setting the environment up happens
> later, in WI-005.

## Development Environment Setup

- **Target platforms**: [e.g., Linux, macOS, Windows (WSL2)]
- **Version control**: [Git hosting and access, e.g., SSH keys]
- **Runtimes and version managers**: [Language runtimes, their versions, and how
  they are pinned]
- **Environment isolation**: [Devcontainer, Docker, host-only, or
  no-container, and why]
- **Local services**: [Services the project needs locally and the command that
  starts them, or none]
- **Editor configuration**: [Shared workspace settings and recommended
  extensions]
- **Configuration variables**: [Environment example file with every required
  key; where local values live and that they stay out of Git]
- **Code quality**: [Linters, formatters, and type checkers, run by the
  pre-commit hook]
- **Verification command**: [Command that proves the environment works: tests,
  migrations if any, and the health or smoke check]

## Governance & Workflow

These answers feed the project constitution through root `config.yaml`.

- **Version control**: [Integration branch, whether direct commits to it are
  allowed, and the policy for unrelated work on an in-flight pull request]
- **Commits**: [The hook that enforces the template's commit convention
  (Conventional Commits with the `[FR][WI][TASK]` suffix), and the secret
  scanner that hooks and CI run]
- **CI**: [The ordered quality gates. They run in the inherited
  `.github/workflows/validators.yml`, which is the project's CI file]
- **Tool configuration**: [The canonical configuration file per tool and the
  test layout / fixture policy]
- **Coding agent**: [Framework, instruction file (e.g. `CLAUDE.md`,
  `AGENTS.md`, `.github/copilot-instructions.md`), its init command, whether it
  is tracked in Git, and the files it must reference]
- **Agent limits**: [Changes that require approval before scope expansion, the
  destructive-history boundary, and whether agents leave the working tree on
  the pushed PR branch]
- **Naming**: [Established terms that must not be renamed]
- **Governance**: [Initial constitution version, ratification date, and
  amendment log location]
