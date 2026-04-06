# skills

Personal skills repository for reusable Codex/Cursor workflows, plus a small set of personal custom skills.

- Chinese version: [README.zh.md](./README.zh.md)

## Overview

This repository is the canonical remote home for skills that are useful across local AI coding tools.

It is organized around two top-level scopes:

- `general/`: skills that are portable across projects and worth reusing broadly
- `personal-custom/`: skills that are intentionally opinionated for personal setup, private workflows, or project-specific habits

The repository is intended to support these use cases:

- keep a curated remote backup of local skills
- copy selected skills into `.codex/skills/` or `.cursor/skills/` for a specific project
- separate truly reusable skills from personal-only workflows
- make the catalog easy to scan both for humans and future automation

## Repository Map

```text
skills/
├── README.md
├── README.zh.md
├── scripts/
│   ├── generate_readme_sections.py
│   ├── install_skill.py
│   ├── sync_skills.py
│   └── validate_index.py
├── skills-index.json
├── general/
│   ├── ai-sync/
│   ├── docs/
│   ├── planning/
│   └── repository-maintenance/
└── personal-custom/
    ├── design/
    ├── logs/
    └── machine-setup/
```

## Structure

- `general/`: Reusable skills that are broadly applicable across projects and workflows.
  - `ai-sync/`: Skills for shared AI context bootstrap and synchronization.
  - `docs/`: Skills for documentation rendering and review workflows.
  - `planning/`: Skills for task decomposition and execution planning.
  - `repository-maintenance/`: Skills for maintaining this skills repository and its catalog.
- `personal-custom/`: Skills tailored to personal workflows, machine setup, or project-specific processes.
  - `machine-setup/`: Skills for local shell and development environment setup.
  - `design/`: Skills for design-to-code workflows.
  - `logs/`: Skills for personal or project progress logging.

## Classification Rules

Use `general/` when a skill is:

- useful across multiple repositories
- not tightly coupled to one private project
- safe to share without exposing personal-only process assumptions
- understandable without requiring private local context

Use `personal-custom/` when a skill is:

- tied to this machine or shell setup
- designed around a personal workflow
- coupled to a private project structure or naming convention
- helpful mainly as a personal toolbox rather than a general reusable asset

## Skill Index

<!-- BEGIN SKILL INDEX -->
| Skill | Scope | Category | Purpose | Path |
|---|---|---|---|---|
| `cross-tool-ai-sync` | General | AI Sync | Sync shared AI context across Codex, Cursor, and Claude. | `general/ai-sync/cross-tool-ai-sync/` |
| `project-ai-sync-bootstrap` | General | AI Sync | Bootstrap shared AI context and sync scaffolding in a new repository. | `general/ai-sync/project-ai-sync-bootstrap/` |
| `md-browser-preview` | General | Docs | Render Markdown to HTML and preview it in a browser. | `general/docs/md-browser-preview/` |
| `task-subagent-planner` | General | Planning | Turn task-marked requests into review-first subagent execution plans. | `general/planning/task-subagent-planner/` |
| `skills-repo-maintainer` | General | Repository Maintenance | Drive install, sync, validation, and README generation workflows for this skills repository. | `general/repository-maintenance/skills-repo-maintainer/` |
| `machine-dev-bootstrap` | Personal Custom | Machine Setup | Restore the standard development environment baseline on this Mac. | `personal-custom/machine-setup/machine-dev-bootstrap/` |
| `zsh-setup` | Personal Custom | Machine Setup | Configure and troubleshoot zsh themes, plugins, and prompt styles. | `personal-custom/machine-setup/zsh-setup/` |
| `sketch-to-android` | Personal Custom | Design | Generate Android View-based UI code from Sketch designs. | `personal-custom/design/sketch-to-android/` |
| `sketch-to-compose` | Personal Custom | Design | Generate Jetpack Compose UI code from Sketch designs. | `personal-custom/design/sketch-to-compose/` |
| `parttime-work-log` | Personal Custom | Logs | Record and summarize personal part-time work logs. | `personal-custom/logs/parttime-work-log/` |
| `work-progress-log` | Personal Custom | Logs | Track and summarize Siuper project progress notes. | `personal-custom/logs/work-progress-log/` |
<!-- END SKILL INDEX -->

The same catalog is also available in machine-readable form:

- `skills-index.json`

## How To Choose

- Choose `general/ai-sync/*` when you want to bootstrap or maintain cross-tool AI instructions.
- Choose `general/docs/*` when you need document rendering or review helpers.
- Choose `general/planning/*` when you want the assistant to decompose work before execution.
- Choose `general/repository-maintenance/*` when you want to maintain this repository itself, sync local skill sources, or validate the catalog.
- Choose `personal-custom/machine-setup/*` when the task is about terminal, shell, or machine bootstrap.
- Choose `personal-custom/design/*` when the task is about converting Sketch designs into Android UI code.
- Choose `personal-custom/logs/*` when the task is about personal or project progress tracking.

## Usage

Copy the desired skill folders into a project's `.cursor/skills/` or `.codex/skills/` directory, keeping each skill folder self-contained with its `SKILL.md` and companion assets/scripts.

For repeatable installs, prefer the included installer script instead of manual copying.

### Installer Script

List all indexed skills:

```bash
python3 scripts/install_skill.py --list
```

List only general skills:

```bash
python3 scripts/install_skill.py --list --scope general
```

Install one skill into the current project's Codex skills directory:

```bash
python3 scripts/install_skill.py md-browser-preview --tool codex --project-root .
```

Install multiple skills into the current project's Cursor skills directory:

```bash
python3 scripts/install_skill.py cross-tool-ai-sync task-subagent-planner --tool cursor --project-root .
```

Overwrite an existing installation:

```bash
python3 scripts/install_skill.py md-browser-preview --tool codex --project-root . --force
```

Install directly into a custom target directory:

```bash
python3 scripts/install_skill.py sketch-to-compose --target-dir /absolute/path/to/.codex/skills
```

### Validation Script

Validate that `skills-index.json` matches the repository contents:

```bash
python3 scripts/validate_index.py
```

Regenerate the README skill index sections from `skills-index.json`:

```bash
python3 scripts/generate_readme_sections.py
```

### Sync Script

Sync selected skills from local source roots into this repository:

```bash
python3 scripts/sync_skills.py md-browser-preview task-subagent-planner \
  --source-root ~/.codex/skills \
  --source-root ~/project/Siuper/siuper-sdk-android/.codex/skills
```

Sync all indexed skills from a set of local roots:

```bash
python3 scripts/sync_skills.py --all \
  --source-root ~/.codex/skills \
  --source-root ~/project/Siuper/siuper-sdk-android/.codex/skills \
  --source-root ~/project/Siuper/.codex/skills
```

Preview what would be synced without writing changes:

```bash
python3 scripts/sync_skills.py --all \
  --source-root ~/.codex/skills \
  --source-root ~/project/Siuper/siuper-sdk-android/.codex/skills \
  --source-root ~/project/Siuper/.codex/skills \
  --dry-run
```

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

## Update Existing Installations

Refresh one installed skill from this repository:

```bash
rm -rf .codex/skills/md-browser-preview
cp -R /path/to/skills/general/docs/md-browser-preview .codex/skills/
```

Refresh multiple skills:

```bash
cp -R /path/to/skills/general/ai-sync/cross-tool-ai-sync .codex/skills/
cp -R /path/to/skills/general/planning/task-subagent-planner .codex/skills/
```

If a skill affects shared AI context or tool adapters inside a target project, run that project's sync command after installation when applicable.

## Maintenance Workflow

For day-to-day maintenance of this repository:

1. Update or create a skill in its real working source location.
2. Ensure `skills-index.json` is correct.
3. Use `general/repository-maintenance/skills-repo-maintainer/` when you want the assistant to drive this workflow consistently.
4. Run `scripts/sync_skills.py` to pull the latest local skill contents into this repository.
5. Run `scripts/validate_index.py`.
6. Run `scripts/generate_readme_sections.py` if the catalog changed.
7. Review the git diff.
8. Commit and push to `develop`.

## Contribution Workflow

For a new or updated skill:

1. Edit the skill in its source location.
2. Keep the skill self-contained with `SKILL.md` plus only the resources it actually needs.
3. Place it under the correct category in this repository.
4. Update `skills-index.json`.
5. Ensure `scripts/install_skill.py --list` still reflects the new catalog correctly.
6. Run `scripts/validate_index.py`.
7. Run `scripts/generate_readme_sections.py` if the catalog changed.
8. Commit to `develop`.

## Quality Bar

Each skill should:

- have a clear `name` and `description` in `SKILL.md`
- stay focused on one job or one tightly related workflow
- keep instructions concise and avoid duplicating long reference material in the main body
- preserve required companion files such as `scripts/`, `assets/`, `references/`, or `agents/`
- avoid embedding project-specific assumptions unless it is intentionally under `personal-custom/`

## Naming Conventions

- Skill folder names use lowercase hyphen-case.
- Category folders describe the workflow domain, not the implementation detail.
- Prefer short action-oriented names such as `md-browser-preview` or `task-subagent-planner`.
- Put machine-specific or personal logging skills under `personal-custom/`, not `general/`.

## Branch

- Primary working branch: `develop`.
