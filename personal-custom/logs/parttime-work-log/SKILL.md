---
name: parttime-work-log
description: Use when the user wants to record, update, or summarize part-time work in the local personal log under `~/personal/parttime/`. Supports daily work duration, work content, and monthly summaries in markdown.
---

# Parttime Work Log

Use this skill for the personal兼职工作记录 stored in:

- `~/personal/parttime/YYYY-MM.md`

## When To Use

Trigger this skill when the user asks to:

- 记录兼职工作
- 更新今天的兼职工作时长或内容
- 汇总兼职工作记录
- 输出按日期或按事项的兼职总结

## Write Rules

- Store data in `~/personal/parttime/YYYY-MM.md`.
- Reuse the current month file if it already exists.
- If today's section exists, update that section instead of creating a duplicate date block.
- Keep the exact Chinese headings:
  - `## YYYY-MM-DD`
  - `### 工作时长:`
  - `### 工作内容:`
- Keep the user's wording; only normalize formatting lightly.

## Summary Rules

When the user asks for a summary:

1. Read the relevant monthly file(s).
2. Summarize by date or by work topic when useful.
3. Keep it brief unless the user asks for detail.

## Command

Use the helper script for deterministic updates:

```bash
python3 ~/.codex/skills/parttime-work-log/scripts/update_parttime_log.py --date 2026-04-05 --hours "3小时" --content "1、事项 A\n2、事项 B"
```
