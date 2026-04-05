#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path


SYNC_SECTION = """## Shared AI Sync System

This repository uses a single source of truth for AI-facing project context.

Shared source files:

- `.ai/shared/PROJECT_AI_CONTEXT.md`
- `.ai/shared/AI_SYNC_POLICY.md`

Project-local sync skill:

- `.codex/skills/cross-tool-ai-sync/SKILL.md`

Rules:

- When creating or updating skills, global AI context, or project-level AI context, update the shared source first.
- Put reusable Codex behavior in `.codex/skills/`.
- After updates, run `python3 .codex/skills/cross-tool-ai-sync/scripts/sync_ai_tooling.py`.
- Do not treat generated Cursor or Claude adapter files as the source of truth.
"""


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def append_sync_section(path: Path) -> None:
    if path.exists():
        current = path.read_text(encoding="utf-8")
        if "## Shared AI Sync System" in current:
            return
        new_content = current.rstrip() + "\n\n" + SYNC_SECTION + "\n"
    else:
        title = "# AGENTS.md" if path.name == "AGENTS.md" else "# CLAUDE.md"
        new_content = title + "\n\n" + SYNC_SECTION + "\n"
    path.write_text(new_content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", default=".")
    args = parser.parse_args()

    repo_root = Path(args.target).expanduser().resolve()

    project_context = repo_root / ".ai/shared/PROJECT_AI_CONTEXT.md"
    sync_policy = repo_root / ".ai/shared/AI_SYNC_POLICY.md"
    local_skill = repo_root / ".codex/skills/cross-tool-ai-sync/SKILL.md"
    local_sync_script = repo_root / ".codex/skills/cross-tool-ai-sync/scripts/sync_ai_tooling.py"

    write_file(
        project_context,
        """# Shared Project AI Context

This file is the canonical project-level AI context for this repository.

Fill in the stable project facts that should be shared across Codex, Cursor, Claude, and similar local coding tools.

Recommended sections:

- scope
- first reads
- commands
- architecture summary
- shared UI or coding rules
- repository-specific workflow constraints

When a rule should apply across multiple tools, put the canonical version here or in `AI_SYNC_POLICY.md` first.
""",
    )

    write_file(
        sync_policy,
        """# AI Sync Policy

This repository uses one shared source of truth for AI-facing context and reusable tool-sync behavior.

## Canonical Sources

- `.ai/shared/PROJECT_AI_CONTEXT.md`
- `.ai/shared/AI_SYNC_POLICY.md`
- `.codex/skills/*`

## Required Workflow

1. Update the shared source files first.
2. Add or update reusable Codex skills under `.codex/skills/` when needed.
3. Run:
   `python3 .codex/skills/cross-tool-ai-sync/scripts/sync_ai_tooling.py`
4. Treat generated Cursor and Claude adapter files as managed outputs, not as the source of truth.
""",
    )

    write_file(
        local_skill,
        """---
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
""",
    )

    write_file(
        local_sync_script,
        """#!/usr/bin/env python3

from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[4]
    shared_context = repo_root / ".ai/shared/PROJECT_AI_CONTEXT.md"
    sync_policy = repo_root / ".ai/shared/AI_SYNC_POLICY.md"

    cursor_rule = repo_root / ".cursor/rules/000-shared-ai-context.mdc"
    cursor_command = repo_root / ".cursor/commands/sync-ai-context.md"
    claude_command = repo_root / ".claude/commands/sync-ai-context.md"

    cursor_rule.parent.mkdir(parents=True, exist_ok=True)
    cursor_command.parent.mkdir(parents=True, exist_ok=True)
    claude_command.parent.mkdir(parents=True, exist_ok=True)

    cursor_rule.write_text(
        \"\"\"---
description: Shared AI context and sync policy for this repository
alwaysApply: true
---

# Shared AI Context

This file is managed by `.codex/skills/cross-tool-ai-sync/scripts/sync_ai_tooling.py`.

Before acting on project-wide instructions, read:

- `.ai/shared/PROJECT_AI_CONTEXT.md`
- `.ai/shared/AI_SYNC_POLICY.md`

When creating or updating project-level AI context, shared rules, or reusable skills intended to affect multiple tools:

1. Update the shared source files first
2. Prefer `.codex/skills/*` for reusable Codex behavior
3. Regenerate adapters with:
   `python3 .codex/skills/cross-tool-ai-sync/scripts/sync_ai_tooling.py`

Do not treat managed Cursor adapter files as the source of truth.
\"\"\",
        encoding=\"utf-8\",
    )

    shared_refs = (
        \"- `.ai/shared/PROJECT_AI_CONTEXT.md`\\n\"
        \"- `.ai/shared/AI_SYNC_POLICY.md`\\n\"
        \"- `.codex/skills/cross-tool-ai-sync/SKILL.md`\\n\"
    )

    command_body = (
        \"# Sync AI Context\\n\\n\"
        \"This file is managed by `.codex/skills/cross-tool-ai-sync/scripts/sync_ai_tooling.py`.\\n\\n\"
        \"Use this command when shared AI context or reusable skills have changed and tool adapters must be refreshed.\\n\\n\"
        \"Shared sources:\\n\\n\"
        f\"{shared_refs}\\n\"
        \"Run:\\n\\n\"
        \"```bash\\n\"
        \"python3 .codex/skills/cross-tool-ai-sync/scripts/sync_ai_tooling.py\\n\"
        \"```\\n\"
    )

    cursor_command.write_text(command_body, encoding=\"utf-8\")
    claude_command.write_text(command_body, encoding=\"utf-8\")

    for path in [shared_context, sync_policy, cursor_rule, cursor_command, claude_command]:
        print(path.relative_to(repo_root))


if __name__ == \"__main__\":
    main()
""",
    )

    local_sync_script.chmod(0o755)
    append_sync_section(repo_root / "AGENTS.md")
    append_sync_section(repo_root / "CLAUDE.md")

    print(repo_root)
    print(project_context.relative_to(repo_root))
    print(sync_policy.relative_to(repo_root))
    print(local_skill.relative_to(repo_root))
    print(local_sync_script.relative_to(repo_root))


if __name__ == "__main__":
    main()
