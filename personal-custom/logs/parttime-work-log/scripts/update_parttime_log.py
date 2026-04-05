#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from datetime import date as date_cls
from pathlib import Path


def month_title(year: int, month: int) -> str:
    return f"# {year}年{month}月兼职工作记录\n"


def ensure_month_file(path: Path, year: int, month: int) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(month_title(year, month) + "\n", encoding="utf-8")


def upsert_day_block(text: str, day: str, hours: str | None, content: str | None) -> str:
    date_header = f"## {day}"
    pattern = re.compile(rf"(?ms)^## {re.escape(day)}\n.*?(?=^## |\Z)")
    hours_value = hours or ""
    content_value = (content or "").rstrip()
    new_block = (
        f"{date_header}\n\n"
        f"### 工作时长: {hours_value}\n\n"
        f"### 工作内容:\n"
        f"{content_value}\n"
    )

    if pattern.search(text):
        return pattern.sub(new_block + "\n", text).rstrip() + "\n"

    base = text.rstrip() + "\n\n" if text.strip() else ""
    return base + new_block + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=str(date_cls.today()))
    parser.add_argument("--hours", default="")
    parser.add_argument("--content", default="")
    args = parser.parse_args()

    year, month, _ = map(int, args.date.split("-"))
    target = Path.home() / "personal" / "parttime" / f"{year:04d}-{month:02d}.md"

    ensure_month_file(target, year, month)
    original = target.read_text(encoding="utf-8")
    updated = upsert_day_block(original, args.date, args.hours, args.content)
    target.write_text(updated, encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
