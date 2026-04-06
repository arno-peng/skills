from pathlib import Path
import json
from typing import Dict, List


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_index(index_path: Path = None) -> List[Dict]:
    path = index_path or (repo_root() / "skills-index.json")
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("skills-index.json must contain a top-level list")
    return data

