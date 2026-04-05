#!/usr/bin/env python3
import html
import re
import subprocess
import sys
from pathlib import Path


def escape_inline(text: str) -> str:
    return html.escape(text, quote=False)


def render_inline(text: str) -> str:
    text = escape_inline(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def is_ordered_item(line: str) -> bool:
    return bool(re.match(r"^\d+\.\s+", line))


def ordered_item_body(line: str) -> str:
    return re.sub(r"^\d+\.\s+", "", line, count=1)


def render_markdown(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    out = []
    in_code = False
    code_lines = []
    paragraph = []
    in_list = None
    list_items = []
    in_blockquote = False
    quote_lines = []
    table_buffer = []

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            out.append(f"<p>{render_inline(' '.join(part.strip() for part in paragraph))}</p>")
            paragraph = []

    def flush_list():
        nonlocal in_list, list_items
        if in_list and list_items:
            tag = "ol" if in_list == "ol" else "ul"
            items = "".join(f"<li>{render_inline(item)}</li>" for item in list_items)
            out.append(f"<{tag}>{items}</{tag}>")
        in_list = None
        list_items = []

    def flush_blockquote():
        nonlocal in_blockquote, quote_lines
        if quote_lines:
            inner = " ".join(line.strip() for line in quote_lines)
            out.append(f"<blockquote><p>{render_inline(inner)}</p></blockquote>")
        in_blockquote = False
        quote_lines = []

    def flush_table():
        nonlocal table_buffer
        if len(table_buffer) < 2:
            table_buffer = []
            return
        header = [cell.strip() for cell in table_buffer[0].strip().strip("|").split("|")]
        divider = table_buffer[1]
        if "|" not in divider or not re.match(r"^\s*\|?[\s:-|]+\|?\s*$", divider):
            table_buffer = []
            return
        body_rows = table_buffer[2:]
        parts = ["<table><thead><tr>"]
        parts.extend(f"<th>{render_inline(cell)}</th>" for cell in header)
        parts.append("</tr></thead><tbody>")
        for row in body_rows:
            cols = [cell.strip() for cell in row.strip().strip("|").split("|")]
            parts.append("<tr>")
            for cell in cols:
                parts.append(f"<td>{render_inline(cell)}</td>")
            parts.append("</tr>")
        parts.append("</tbody></table>")
        out.append("".join(parts))
        table_buffer = []

    for raw_line in lines:
        line = raw_line.rstrip("\n")

        if in_code:
            if line.strip().startswith("```"):
                code = "\n".join(code_lines)
                out.append(f"<pre><code>{html.escape(code)}</code></pre>")
                in_code = False
                code_lines = []
            else:
                code_lines.append(line)
            continue

        if line.strip().startswith("```"):
            flush_paragraph()
            flush_list()
            flush_blockquote()
            flush_table()
            in_code = True
            code_lines = []
            continue

        if "|" in line and not paragraph and not in_list and not in_blockquote:
            table_buffer.append(line)
            continue
        if table_buffer and ("|" in line or not line.strip()):
            if line.strip():
                table_buffer.append(line)
                continue
            flush_table()

        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            flush_list()
            flush_blockquote()
            flush_table()
            continue

        if stripped == "---" or stripped == "***":
            flush_paragraph()
            flush_list()
            flush_blockquote()
            flush_table()
            out.append("<hr />")
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            flush_paragraph()
            flush_list()
            flush_blockquote()
            flush_table()
            level = len(heading.group(1))
            body = render_inline(heading.group(2))
            out.append(f"<h{level}>{body}</h{level}>")
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            flush_list()
            flush_table()
            in_blockquote = True
            quote_lines.append(stripped[1:].lstrip())
            continue
        flush_blockquote()

        if stripped.startswith(("- ", "* ")):
            flush_paragraph()
            flush_table()
            if in_list not in (None, "ul"):
                flush_list()
            in_list = "ul"
            list_items.append(stripped[2:].strip())
            continue

        if is_ordered_item(stripped):
            flush_paragraph()
            flush_table()
            if in_list not in (None, "ol"):
                flush_list()
            in_list = "ol"
            list_items.append(ordered_item_body(stripped).strip())
            continue

        if in_list:
            flush_list()

        paragraph.append(stripped)

    flush_paragraph()
    flush_list()
    flush_blockquote()
    flush_table()

    return "\n".join(out)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: render_markdown_preview.py [--no-open] /absolute/path/to/file.md", file=sys.stderr)
        return 1

    args = sys.argv[1:]
    should_open = True
    if args[0] == "--no-open":
        should_open = False
        args = args[1:]

    if not args:
        print("Usage: render_markdown_preview.py [--no-open] /absolute/path/to/file.md", file=sys.stderr)
        return 1

    md_path = Path(args[0]).expanduser().resolve()
    if not md_path.exists():
        print(f"Markdown file not found: {md_path}", file=sys.stderr)
        return 1

    template_path = Path("~/.codex/skills/md-browser-preview/assets/markdown_preview_template.html").expanduser()
    safe_stem = re.sub(r"[^A-Za-z0-9._-]+", "_", md_path.stem) or "preview"
    output_path = Path(f"/tmp/local_ai_markdown_preview_{safe_stem}.html")

    markdown_text = md_path.read_text(encoding="utf-8")
    rendered = render_markdown(markdown_text)
    title = md_path.stem
    meta = f"Source: {md_path}"

    template = template_path.read_text(encoding="utf-8")
    page = (
        template
        .replace("{{title}}", html.escape(title))
        .replace("{{meta}}", html.escape(meta))
        .replace("{{content}}", rendered)
    )

    output_path.write_text(page, encoding="utf-8")
    if should_open:
        subprocess.run(["open", str(output_path)], check=False)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
