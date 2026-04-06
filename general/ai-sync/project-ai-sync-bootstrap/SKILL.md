---
name: project-ai-sync-bootstrap
description: Use when starting a new project or when the user wants any repository to automatically support synchronized AI context and skills across Codex, Cursor, Claude, or similar local coding tools. This skill bootstraps the per-project shared AI source and native adapter files.
---

# Project AI Sync Bootstrap

Use this skill to initialize any repository with a shared AI context source and cross-tool adapter files.

## When To Use

Trigger this skill when the user asks to:

- start a new project with shared AI context
- make any repository support synchronized Codex/Cursor/Claude instructions
- initialize project-level AI skills/context
- install the cross-tool AI sync system in a repo

## What This Creates

Run the initializer script to create the shared AI context source, local sync skill, and managed adapter files.

Key outputs include:

- `.ai/shared/*`
- `.codex/skills/cross-tool-ai-sync/*`
- managed Cursor and Claude adapters
- `AGENTS.md` and `CLAUDE.md` pointers

## Command

From the target project root, run:

```bash
python3 ~/.codex/skills/project-ai-sync-bootstrap/scripts/init_project_ai_sync.py .
```

Or pass an explicit path:

```bash
python3 ~/.codex/skills/project-ai-sync-bootstrap/scripts/init_project_ai_sync.py /abs/path/to/repo
```

## Workflow

1. Identify the project root.
2. Run the initializer script.
3. Review `AGENTS.md` and `CLAUDE.md` pointers if the repo already had custom rules.
4. For later updates, use the local project skill:
   `.codex/skills/cross-tool-ai-sync/SKILL.md`

## Guardrails

- Keep canonical shared context in `.ai/shared/*`.
- Keep reusable project-local behavior in `.codex/skills/*`.
- Do not maintain generated Cursor/Claude adapter files by hand.
- If `AGENTS.md` or `CLAUDE.md` already exist, preserve existing content and append the sync section if missing.
