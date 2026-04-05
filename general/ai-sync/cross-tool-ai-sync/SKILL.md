---
name: cross-tool-ai-sync
description: Use when the user asks to synchronize skills, global AI context, or project-level AI context across Codex, Cursor, Claude, or similar local coding tools in this repository, or when adding new shared AI rules that should be recognized by multiple tools.
---

# Cross Tool AI Sync

Use this skill when AI-facing instructions in this repository must stay aligned across tools.

## Canonical Sources

Always update these first:

- `.ai/shared/PROJECT_AI_CONTEXT.md`
- `.ai/shared/AI_SYNC_POLICY.md`
- `.codex/skills/*` for reusable Codex-native behavior

## Sync Command

After shared-context changes, run:

```bash
python3 .codex/skills/cross-tool-ai-sync/scripts/sync_ai_tooling.py
```

## Workflow

1. Identify whether the change is project context, shared AI policy, or reusable skill behavior.
2. Update the canonical shared source.
3. If the behavior should be reusable in Codex, add or update a skill under `.codex/skills/`.
4. Run the sync script to regenerate Cursor and Claude adapter files.
5. Keep `AGENTS.md` and `CLAUDE.md` as stable entrypoints that point back to the shared source.
