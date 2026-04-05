---
name: work-progress-log
description: Use when the user asks to record project progress, append daily work notes, archive recent work context, or summarize `records/work-progress-context.md` by category or time in the Siuper workspace.
---

# Work Progress Log

Use this skill for the shared progress log in:

- `records/work-progress-context.md`

## When To Use

Trigger this skill when the user asks to:

- record current progress
- save raw work notes
- summarize recent work
- archive work context
- update the daily project log

## Recording Flow

If the user says a task is finished and wants it logged:

1. Draft short bullets first.
2. Use this format:
   `- **[category]** brief factual summary`
3. Wait for confirmation before writing, unless the user explicitly says to write directly.

If the user provides raw notes and clearly wants them saved as-is, append them directly after light cleanup.

## Write Rules

- Always append; do not rewrite old entries.
- Add a `### YYYY-MM-DD` section for today if missing.
- Keep each bullet to one or two short sentences.
- Use a single short category label per bullet.
- Prefer concrete facts such as module, branch, fix, or shipped outcome.

## Summaries

When the user asks for a summary:

1. Read the whole file.
2. Summarize in two views:
   - by project/category
   - by time
3. Keep the response short unless the user asks for detail.

## Category Hints

Infer categories from repo paths when possible:

- `dolphin-im-android`
- `siuper-sdk-android`
- `idl`

