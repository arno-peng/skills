#!/usr/bin/env python3

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
        """---
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
""",
        encoding="utf-8",
    )

    shared_refs = (
        "- `.ai/shared/PROJECT_AI_CONTEXT.md`\n"
        "- `.ai/shared/AI_SYNC_POLICY.md`\n"
        "- `.codex/skills/cross-tool-ai-sync/SKILL.md`\n"
    )

    command_body = (
        "# Sync AI Context\n\n"
        "This file is managed by `.codex/skills/cross-tool-ai-sync/scripts/sync_ai_tooling.py`.\n\n"
        "Use this command when shared AI context or reusable skills have changed and tool adapters must be refreshed.\n\n"
        "Shared sources:\n\n"
        f"{shared_refs}\n"
        "Run:\n\n"
        "```bash\n"
        "python3 .codex/skills/cross-tool-ai-sync/scripts/sync_ai_tooling.py\n"
        "```\n"
    )

    cursor_command.write_text(command_body, encoding="utf-8")
    claude_command.write_text(command_body, encoding="utf-8")

    for path in [shared_context, sync_policy, cursor_rule, cursor_command, claude_command]:
        print(path.relative_to(repo_root))


if __name__ == "__main__":
    main()
