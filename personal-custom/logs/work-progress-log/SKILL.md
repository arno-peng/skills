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

## Write Rules

- Always append; do not rewrite old entries.
- Add a `### YYYY-MM-DD` section for today if missing.
- Keep each bullet to one or two short sentences.
- Use a single short category label per bullet.
- Prefer concrete facts such as module, branch, fix, or shipped outcome.
- If the user asks to log a finished task, draft short bullets first and wait for confirmation unless they explicitly want direct write-through.
- If the user provides raw notes and clearly wants them saved as-is, append them after light cleanup.

## Summaries

When the user asks for a summary:

1. Read the whole file.
2. Summarize by project/category and by time.
3. Keep the response short unless the user asks for detail.
