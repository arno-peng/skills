#!/usr/bin/env python3

from pathlib import Path
from typing import Dict, List

from lib.skills_repo import load_index, repo_root


BEGIN = "<!-- BEGIN SKILL INDEX -->"
END = "<!-- END SKILL INDEX -->"


def build_en(entries: List[Dict]) -> str:
    category_map = {
        "ai-sync": "AI Sync",
        "docs": "Docs",
        "planning": "Planning",
        "repository-maintenance": "Repository Maintenance",
        "machine-setup": "Machine Setup",
        "design": "Design",
        "logs": "Logs",
    }
    lines = [
        BEGIN,
        "| Skill | Scope | Category | Purpose | Path |",
        "|---|---|---|---|---|",
    ]
    for entry in entries:
        lines.append(
            "| `{name}` | {scope} | {category} | {summary} | `{path}/` |".format(
                name=entry["name"],
                scope="General" if entry["scope"] == "general" else "Personal Custom",
                category=category_map.get(entry["category"], entry["category"]),
                summary=entry["summary"],
                path=entry["path"],
            )
        )
    lines.append(END)
    return "\n".join(lines)


def build_zh(entries: List[Dict]) -> str:
    category_map = {
        "ai-sync": "AI Sync",
        "docs": "Docs",
        "planning": "Planning",
        "repository-maintenance": "Repository Maintenance",
        "machine-setup": "Machine Setup",
        "design": "Design",
        "logs": "Logs",
    }
    scope_map = {"general": "General", "personal-custom": "Personal Custom"}
    lines = [
        BEGIN,
        "| Skill | 范围 | 分类 | 用途 | 路径 |",
        "|---|---|---|---|---|",
    ]
    for entry in entries:
        lines.append(
            "| `{name}` | {scope} | {category} | {summary} | `{path}/` |".format(
                name=entry["name"],
                scope=scope_map[entry["scope"]],
                category=category_map.get(entry["category"], entry["category"]),
                summary=entry.get("summary_zh", entry["summary"]),
                path=entry["path"],
            )
        )
    lines.append(END)
    return "\n".join(lines)


def replace_section(path: Path, replacement: str) -> None:
    text = path.read_text(encoding="utf-8")
    start = text.find(BEGIN)
    end = text.find(END)
    if start == -1 or end == -1 or end < start:
        raise ValueError("Missing skill index markers in {}".format(path))
    end += len(END)
    updated = text[:start] + replacement + text[end:]
    path.write_text(updated, encoding="utf-8")


def main() -> int:
    root = repo_root()
    entries = load_index()
    replace_section(root / "README.md", build_en(entries))
    replace_section(root / "README.zh.md", build_zh(entries))
    print("Updated README skill index sections.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
