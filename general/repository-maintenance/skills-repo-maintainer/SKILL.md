---
name: skills-repo-maintainer
description: Use when the user wants to maintain this skills repository, sync local skill source folders into it, validate `skills-index.json`, or install indexed skills into `.codex/skills/` or `.cursor/skills/` using the repository's maintenance scripts.
---

# Skills Repo Maintainer

Use this skill when working inside this repository or when using this repository as the source of truth for skill distribution.

## What this skill covers

This skill orchestrates these repository scripts:

- `scripts/install_skill.py`
- `scripts/sync_skills.py`
- `scripts/validate_index.py`

## When to use

Apply this skill when the user wants to:

- add or update a skill in this repository
- sync local skill source directories into this repository
- validate that `skills-index.json` matches the repository contents
- install one or more indexed skills into a project's `.codex/skills/` or `.cursor/skills/`
- review or maintain the repository catalog and structure

## Workflow

1. Identify whether the task is `install`, `sync`, `validate`, or a combined maintenance flow.
2. If the repository catalog changes, update both:
   - `skills-index.json`
   - `README.md` when the public index or structure changed
3. Use `scripts/sync_skills.py` when local source folders are the canonical source and this repository should be refreshed from them.
4. Use `scripts/validate_index.py` after structural changes or catalog edits.
5. Review the resulting diff before committing.

## Script Selection

Use `scripts/install_skill.py` for:

- listing available skills
- installing skills into `.codex/skills/`
- installing skills into `.cursor/skills/`
- overwriting an existing local installation with `--force`

Use `scripts/sync_skills.py` for:

- copying local skill source directories into this repository
- refreshing many indexed skills from known source roots
- previewing maintenance actions with `--dry-run`

Use `scripts/validate_index.py` for:

- checking `skills-index.json`
- detecting missing `SKILL.md`
- detecting path, scope, or category mismatches
- detecting unindexed skill directories

## Common Commands

List indexed skills:

```bash
python3 scripts/install_skill.py --list
```

Sync indexed skills from local roots:

```bash
python3 scripts/sync_skills.py --all \
  --source-root ~/.codex/skills \
  --source-root ~/project/Siuper/siuper-sdk-android/.codex/skills \
  --source-root ~/project/Siuper/.codex/skills
```

Preview a sync:

```bash
python3 scripts/sync_skills.py --all \
  --source-root ~/.codex/skills \
  --source-root ~/project/Siuper/siuper-sdk-android/.codex/skills \
  --source-root ~/project/Siuper/.codex/skills \
  --dry-run
```

Validate the catalog:

```bash
python3 scripts/validate_index.py
```

Install one skill into the current project's Codex skills directory:

```bash
python3 scripts/install_skill.py md-browser-preview --tool codex --project-root .
```

## Rules

- Treat `skills-index.json` as the machine-readable catalog.
- Keep skill folder names aligned with the indexed `name`.
- Keep category paths aligned with indexed `scope` and `category`.
- Do not silently change category layout without updating both the index and README.
- Prefer `--dry-run` before broad sync operations when the source roots may be ambiguous.
- If multiple source roots contain the same skill, inspect the warning and make sure the chosen source is the intended one.

## Output Expectations

When making maintenance changes, report:

- which script(s) were used
- which skills were installed or synced
- whether validation passed
- any ambiguous source-root choices or follow-up risks
