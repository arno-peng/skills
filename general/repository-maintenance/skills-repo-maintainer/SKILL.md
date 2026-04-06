---
name: skills-repo-maintainer
description: Use when the user wants to maintain this skills repository, sync local skill sources into it, validate `skills-index.json`, or install indexed skills with the repository maintenance scripts.
---

# Skills Repo Maintainer

Use this skill when working inside this repository or when using it as the source of truth for skill distribution.

## Scripts

This skill orchestrates:

- `scripts/install_skill.py`
- `scripts/sync_skills.py`
- `scripts/validate_index.py`
- `scripts/generate_readme_sections.py`

## When To Use

Apply this skill when the user wants to:

- add or update a skill in this repository
- sync local skill source directories into this repository
- validate `skills-index.json`
- regenerate README skill index sections
- install indexed skills into `.codex/skills/` or `.cursor/skills/`

## Workflow

1. Decide whether the task is `install`, `sync`, `validate`, `generate-readme`, or a combined maintenance flow.
2. Treat `skills-index.json` as the machine-readable catalog.
3. If the catalog or structure changes, regenerate README skill index sections.
4. Review the diff before committing.

## Script Selection

Use `scripts/install_skill.py` for listing or installing indexed skills.

Use `scripts/sync_skills.py` for refreshing this repository from local source roots. Prefer `--dry-run` first when multiple roots may contain the same skill.

Use `scripts/validate_index.py` for structural checks, missing `SKILL.md`, and soft quality warnings.

Use `scripts/generate_readme_sections.py` to regenerate the README skill index blocks from `skills-index.json`.

## Rules

- Keep skill folder names aligned with indexed `name`.
- Keep category paths aligned with indexed `scope` and `category`.
- Do not silently change category layout without updating both the index and README.
- If multiple source roots contain the same skill, use `--prefer-root` or `--source-map`.
- Keep detailed command examples in `references/commands.md`, not in the main skill body.

## Output Expectations

When making maintenance changes, report:

- which script(s) were used
- which skills were installed or synced
- whether validation passed
- any ambiguous source-root choices or follow-up risks

For command examples, read:

- `references/commands.md`
