---
name: md-browser-preview
description: Use when the user asks to organize a markdown document for review, preview a `*.md` file, or open a markdown document in the browser. Renders the markdown through a local HTML template and opens the generated preview in the default browser.
---

# Markdown Browser Preview

Use this skill when the user asks to:

- organize a `*.md` document and preview it
- open a markdown document in the browser
- view rendered markdown instead of raw source

## Workflow

1. If the user also wants content changes, update the markdown file first.
2. Render the markdown file with the local preview script:

```bash
python3 ~/.codex/skills/md-browser-preview/scripts/render_markdown_preview.py /absolute/path/to/file.md
```

3. The script generates a disposable preview HTML file and opens it in the default browser.
4. Keep the markdown file as the source of truth. Do not edit the generated preview HTML manually.

For environments where browser launch should be skipped temporarily:

```bash
python3 ~/.codex/skills/md-browser-preview/scripts/render_markdown_preview.py --no-open /absolute/path/to/file.md
```

## Assets

- HTML template:
  - `~/.codex/skills/md-browser-preview/assets/markdown_preview_template.html`

## Notes

- Prefer absolute markdown paths when invoking the script.
- The renderer is offline and self-contained; it does not require network access.
- If browser launch is blocked, return the generated HTML path.
