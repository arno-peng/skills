#!/usr/bin/env python3

import json
import sys
from pathlib import Path
from typing import Dict, List, Set


VALID_SCOPES = set(["general", "personal-custom"])


def load_index(index_path: Path) -> List[Dict]:
    with index_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("skills-index.json must contain a top-level list")
    return data


def discover_repo_skills(repo_root: Path) -> Set[str]:
    skills = set()
    for path in repo_root.rglob("SKILL.md"):
        if ".git" in path.parts:
            continue
        skills.add(str(path.parent.relative_to(repo_root)))
    return skills


def validate_entry(entry: Dict, repo_root: Path) -> List[str]:
    errors = []
    required = ["name", "scope", "category", "path", "portable", "summary"]
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
    repo_root = Path(__file__).resolve().parents[1]
    index_path = repo_root / "skills-index.json"
    entries = load_index(index_path)

    errors = []
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
        errors.extend(validate_entry(entry, repo_root))

    discovered = discover_repo_skills(repo_root)
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

    print("Index validation passed.")
    print("Indexed skills: {}".format(len(entries)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
