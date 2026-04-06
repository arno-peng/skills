#!/usr/bin/env python3

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional

from lib.skills_repo import load_index, repo_root


def format_skill(entry: Dict) -> str:
    portable = "portable" if entry.get("portable") else "personal"
    return (
        f"{entry['name']:<28} "
        f"{entry['scope']:<15} "
        f"{entry['category']:<15} "
        f"{portable:<10} "
        f"{entry['path']}"
    )


def list_skills(entries: List[Dict], scope: Optional[str], category: Optional[str]) -> int:
    filtered = [
        entry
        for entry in entries
        if (scope is None or entry.get("scope") == scope)
        and (category is None or entry.get("category") == category)
    ]

    if not filtered:
        print("No matching skills found.", file=sys.stderr)
        return 1

    print(f"{'NAME':<28} {'SCOPE':<15} {'CATEGORY':<15} {'TYPE':<10} PATH")
    for entry in filtered:
        print(format_skill(entry))
    return 0


def resolve_target_dir(args: argparse.Namespace) -> Path:
    if args.target_dir:
        return Path(args.target_dir).expanduser().resolve()

    project_root = Path(args.project_root).expanduser().resolve()
    tool_dir = ".codex/skills" if args.tool == "codex" else ".cursor/skills"
    return project_root / tool_dir


def install_skill(entry: Dict, repo_root: Path, target_dir: Path, force: bool) -> None:
    source_dir = repo_root / entry["path"]
    if not source_dir.is_dir():
        raise FileNotFoundError(f"Skill source not found: {source_dir}")
    if not (source_dir / "SKILL.md").is_file():
        raise FileNotFoundError(f"SKILL.md missing in {source_dir}")

    destination = target_dir / entry["name"]
    if destination.exists():
        if not force:
            raise FileExistsError(
                f"Destination already exists: {destination}. Use --force to overwrite."
            )
        shutil.rmtree(destination)

    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_dir, destination)
    print(f"Installed {entry['name']} -> {destination}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install skills from this repository using skills-index.json."
    )
    parser.add_argument("skills", nargs="*", help="Skill names to install")
    parser.add_argument(
        "--list", action="store_true", help="List indexed skills instead of installing"
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON when listing")
    parser.add_argument(
        "--scope",
        choices=["general", "personal-custom"],
        help="Filter listed skills by scope",
    )
    parser.add_argument("--category", help="Filter listed skills by category")
    parser.add_argument(
        "--tool",
        choices=["codex", "cursor"],
        default="codex",
        help="Target tool when using --project-root",
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root used to derive .codex/skills or .cursor/skills",
    )
    parser.add_argument(
        "--target-dir",
        help="Explicit target skills directory; overrides --tool and --project-root",
    )
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing installed skills"
    )
    args = parser.parse_args()

    root = repo_root()
    entries = load_index()

    if args.list:
        if args.json:
            filtered = [
                entry
                for entry in entries
                if (args.scope is None or entry.get("scope") == args.scope)
                and (args.category is None or entry.get("category") == args.category)
            ]
            print(json.dumps(filtered, ensure_ascii=False, indent=2))
            return 0 if filtered else 1
        return list_skills(entries, args.scope, args.category)

    if not args.skills:
        parser.error("Provide at least one skill name or use --list.")

    index_by_name = {entry["name"]: entry for entry in entries}
    missing = [name for name in args.skills if name not in index_by_name]
    if missing:
        print("Unknown skill(s): " + ", ".join(missing), file=sys.stderr)
        print("Use --list to inspect available skills.", file=sys.stderr)
        return 1

    target_dir = resolve_target_dir(args)
    for name in args.skills:
        install_skill(index_by_name[name], root, target_dir, args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
