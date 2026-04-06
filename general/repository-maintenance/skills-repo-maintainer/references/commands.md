# Skills Repo Maintainer Commands

## Install

```bash
python3 scripts/install_skill.py --list
python3 scripts/install_skill.py md-browser-preview --tool codex --project-root .
python3 scripts/install_skill.py cross-tool-ai-sync task-subagent-planner --tool cursor --project-root .
```

## Sync

```bash
python3 scripts/sync_skills.py --all \
  --source-root ~/.codex/skills \
  --source-root ~/project/Siuper/siuper-sdk-android/.codex/skills \
  --source-root ~/project/Siuper/.codex/skills
```

Preview first:

```bash
python3 scripts/sync_skills.py --all \
  --source-root ~/.codex/skills \
  --source-root ~/project/Siuper/siuper-sdk-android/.codex/skills \
  --source-root ~/project/Siuper/.codex/skills \
  --dry-run
```

Prefer one source root when duplicates exist:

```bash
python3 scripts/sync_skills.py cross-tool-ai-sync \
  --source-root ~/.codex/skills \
  --source-root ~/project/Siuper/.codex/skills \
  --prefer-root ~/.codex/skills
```

Pin one skill to one exact source:

```bash
python3 scripts/sync_skills.py cross-tool-ai-sync \
  --source-map cross-tool-ai-sync=~/.codex/skills/cross-tool-ai-sync
```

## Validate And Regenerate

```bash
python3 scripts/validate_index.py
python3 scripts/generate_readme_sections.py
```
