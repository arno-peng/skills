# skills

Personal Cursor skills repository.

## Structure

- `general/`: Reusable skills that are broadly applicable across projects and workflows.
  - `ai-sync/`: Skills for shared AI context bootstrap and synchronization.
  - `docs/`: Skills for documentation rendering and review workflows.
  - `planning/`: Skills for task decomposition and execution planning.
- `personal-custom/`: Skills tailored to personal workflows, machine setup, or project-specific processes.
  - `machine-setup/`: Skills for local shell and development environment setup.
  - `design/`: Skills for design-to-code workflows.
  - `logs/`: Skills for personal or project progress logging.

## Skill Index

| Skill | Scope | Category | Purpose | Path |
|---|---|---|---|---|
| `cross-tool-ai-sync` | General | AI Sync | Sync shared AI context across Codex, Cursor, and Claude. | `general/ai-sync/cross-tool-ai-sync/` |
| `project-ai-sync-bootstrap` | General | AI Sync | Bootstrap shared AI context and sync scaffolding in a new repository. | `general/ai-sync/project-ai-sync-bootstrap/` |
| `md-browser-preview` | General | Docs | Render Markdown to HTML and preview it in a browser. | `general/docs/md-browser-preview/` |
| `task-subagent-planner` | General | Planning | Turn task-marked requests into review-first subagent execution plans. | `general/planning/task-subagent-planner/` |
| `machine-dev-bootstrap` | Personal Custom | Machine Setup | Restore the standard development environment baseline on this Mac. | `personal-custom/machine-setup/machine-dev-bootstrap/` |
| `zsh-setup` | Personal Custom | Machine Setup | Configure and troubleshoot zsh themes, plugins, and prompt styles. | `personal-custom/machine-setup/zsh-setup/` |
| `sketch-to-android` | Personal Custom | Design | Generate Android View-based UI code from Sketch designs. | `personal-custom/design/sketch-to-android/` |
| `sketch-to-compose` | Personal Custom | Design | Generate Jetpack Compose UI code from Sketch designs. | `personal-custom/design/sketch-to-compose/` |
| `parttime-work-log` | Personal Custom | Logs | Record and summarize personal part-time work logs. | `personal-custom/logs/parttime-work-log/` |
| `work-progress-log` | Personal Custom | Logs | Track and summarize Siuper project progress notes. | `personal-custom/logs/work-progress-log/` |

## Usage

Copy the desired skill folders into a project's `.cursor/skills/` or `.codex/skills/` directory, keeping each skill folder self-contained with its `SKILL.md` and companion assets/scripts.

### Install Examples

Clone the repository locally:

```bash
git clone --branch develop git@github.com:arno-peng/skills.git
```

Install a skill into a project's Codex skills directory:

```bash
mkdir -p .codex/skills
cp -R /path/to/skills/general/docs/md-browser-preview .codex/skills/
```

Install a skill into a project's Cursor skills directory:

```bash
mkdir -p .cursor/skills
cp -R /path/to/skills/general/planning/task-subagent-planner .cursor/skills/
```

Install a personal custom skill:

```bash
mkdir -p .codex/skills
cp -R /path/to/skills/personal-custom/design/sketch-to-compose .codex/skills/
```

After copying a skill, keep the folder name unchanged and preserve any bundled `scripts/`, `assets/`, `references/`, or `agents/` subdirectories.

## Branch

- Primary working branch: `develop`.
