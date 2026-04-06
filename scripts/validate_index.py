#!/usr/bin/env python3

import sys
from pathlib import Path
from typing import Dict, List, Set

from lib.skills_repo import load_index, repo_root


VALID_SCOPES = set(["general", "personal-custom"])


def discover_repo_skills(repo_root: Path) -> Set[str]:
    skills = set()
    for path in repo_root.rglob("SKILL.md"):
        if ".git" in path.parts:
            continue
        skills.add(str(path.parent.relative_to(repo_root)))
    return skills


def validate_entry(entry: Dict, repo_root: Path) -> List[str]:
    errors = []
    required = ["name", "scope", "category", "path", "portable", "summary", "summary_zh"]
    for key in required:
        if key not in entry:
            errors.append("missing key `{}` in entry {}".format(key, entry))

    if errors:
        return errors

    if entry["scope"] not in VALID_SCOPES:
        errors.append(
            "invalid scope `{}` for skill `{}`".format(entry["scope"], entry["name"])
        )

    skill_path = repo_root / entry["path"]
    if not skill_path.is_dir():
        errors.append("missing directory for `{}`: {}".format(entry["name"], skill_path))
        return errors

    if skill_path.name != entry["name"]:
        errors.append(
            "path/name mismatch for `{}`: path ends with `{}`".format(
                entry["name"], skill_path.name
            )
        )

    if not (skill_path / "SKILL.md").is_file():
        errors.append("SKILL.md missing for `{}`".format(entry["name"]))

    parts = Path(entry["path"]).parts
    if len(parts) < 3:
        errors.append(
            "path for `{}` should look like <scope>/<category>/<skill-name>".format(
                entry["name"]
            )
        )
    elif parts[0] != entry["scope"]:
        errors.append(
            "scope/path mismatch for `{}`: scope is `{}` but path starts with `{}`".format(
                entry["name"], entry["scope"], parts[0]
            )
        )
    elif parts[1] != entry["category"]:
        errors.append(
            "category/path mismatch for `{}`: category is `{}` but path uses `{}`".format(
                entry["name"], entry["category"], parts[1]
            )
        )

    return errors


def main() -> int:
    root = repo_root()
    entries = load_index()

    errors = []
    warnings = []
    names = set()
    paths = set()
    indexed_paths = set()

    for entry in entries:
        name = entry.get("name")
        path = entry.get("path")
        if name in names:
            errors.append("duplicate skill name `{}`".format(name))
        if path in paths:
            errors.append("duplicate skill path `{}`".format(path))
        if name:
            names.add(name)
        if path:
            paths.add(path)
            indexed_paths.add(path)
        errors.extend(validate_entry(entry, root))
        skill_md = root / path / "SKILL.md" if path else None
        scripts_dir = root / path / "scripts" if path else None
        if skill_md and skill_md.is_file():
            line_count = sum(1 for _ in skill_md.open("r", encoding="utf-8"))
            has_scripts = scripts_dir.is_dir() and any(scripts_dir.iterdir())
            if line_count > 120:
                warnings.append(
                    "skill `{}` is long ({} lines); consider references or scripts".format(
                        name, line_count
                    )
                )
            if line_count > 80 and not has_scripts:
                warnings.append(
                    "skill `{}` is {} lines with no scripts/; verify it benefits from being a skill".format(
                        name, line_count
                    )
                )

    discovered = discover_repo_skills(root)
    unindexed = sorted(discovered - indexed_paths)
    missing = sorted(indexed_paths - discovered)

    for path in unindexed:
        errors.append("skill directory is present but not indexed: {}".format(path))
    for path in missing:
        errors.append("indexed path is missing in repository: {}".format(path))

    if errors:
        for error in errors:
            print("ERROR: {}".format(error), file=sys.stderr)
        return 1

    for warning in warnings:
        print("WARN: {}".format(warning), file=sys.stderr)

    print("Index validation passed.")
    print("Indexed skills: {}".format(len(entries)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
