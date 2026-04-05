#!/usr/bin/env python3

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional


def load_index(index_path: Path) -> List[Dict]:
    with index_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("skills-index.json must contain a top-level list")
    return data


def resolve_source_roots(source_roots: List[str]) -> List[Path]:
    return [Path(root).expanduser().resolve() for root in source_roots]


def find_source_dir(
    skill_name: str,
    source_roots: List[Path],
    explicit_dirs: List[Path],
) -> Optional[Path]:
    candidates = []

    for source_dir in explicit_dirs:
        if source_dir.name == skill_name and (source_dir / "SKILL.md").is_file():
            candidates.append(source_dir)

    for root in source_roots:
        candidate = root / skill_name
        if (candidate / "SKILL.md").is_file():
            candidates.append(candidate)

    unique = []
    seen = set()
    for candidate in candidates:
        real = str(candidate.resolve())
        if real not in seen:
            seen.add(real)
            unique.append(candidate)

    if not unique:
        return None

    if len(unique) > 1:
        print(
            "Multiple sources found for `{}`; using first match: {}".format(
                skill_name, unique[0]
            ),
            file=sys.stderr,
        )

    return unique[0]


def sync_one(source_dir: Path, destination_dir: Path, dry_run: bool) -> None:
    if source_dir.resolve() == destination_dir.resolve():
        print("Keeping repository copy for {}".format(destination_dir))
        return

    if dry_run:
        print("Would sync {} -> {}".format(source_dir, destination_dir))
        return

    destination_dir.parent.mkdir(parents=True, exist_ok=True)
    if destination_dir.exists():
        shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)
    print("Synced {} -> {}".format(source_dir, destination_dir))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync local skill source directories into this repository."
    )
    parser.add_argument("skills", nargs="*", help="Skill names to sync")
    parser.add_argument("--all", action="store_true", help="Sync all indexed skills")
    parser.add_argument(
        "--source-root",
        action="append",
        default=[],
        help="Root directory that directly contains skill folders",
    )
    parser.add_argument(
        "--source-dir",
        action="append",
        default=[],
        help="Explicit source skill directory",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    args = parser.parse_args()

    if not args.all and not args.skills:
        parser.error("Provide skill names or use --all.")
    if not args.source_root and not args.source_dir:
        parser.error("Provide at least one --source-root or --source-dir.")

    repo_root = Path(__file__).resolve().parents[1]
    index_path = repo_root / "skills-index.json"
    entries = load_index(index_path)
    index_by_name = {entry["name"]: entry for entry in entries}

    selected_names = list(index_by_name.keys()) if args.all else args.skills
    missing_names = [name for name in selected_names if name not in index_by_name]
    if missing_names:
        print("Unknown skill(s): " + ", ".join(missing_names), file=sys.stderr)
        return 1

    source_roots = resolve_source_roots(args.source_root)
    explicit_dirs = [Path(path).expanduser().resolve() for path in args.source_dir]

    for name in selected_names:
        destination_dir = repo_root / index_by_name[name]["path"]
        source_dir = find_source_dir(name, source_roots, explicit_dirs)
        if source_dir is None:
            if (destination_dir / "SKILL.md").is_file():
                print(
                    "No external source found for `{}`; keeping repository copy.".format(
                        name
                    ),
                    file=sys.stderr,
                )
                source_dir = destination_dir
            else:
                print("No source found for `{}`".format(name), file=sys.stderr)
                return 1

        sync_one(source_dir, destination_dir, args.dry_run)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
