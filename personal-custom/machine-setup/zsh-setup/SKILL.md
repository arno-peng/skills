---
name: zsh-setup
description: Configure and troubleshoot zsh themes (Powerlevel10k), plugins, and prompt style. Use when the user wants to adjust terminal zsh appearance, install or tweak Powerlevel10k, add autosuggestions or syntax highlighting, or debug GitHub 443 issues affecting theme installation.
---

# Zsh Setup & Theme Skill

Use this skill whenever the user wants to change zsh appearance, wire Powerlevel10k, add zsh plugins, or troubleshoot GitHub 443 issues affecting theme installation.

Assume macOS with zsh unless the user says otherwise.

## Workflow

1. Inspect `~/.zshrc` and confirm the basic shell setup.
2. Decide whether the task is:
   - theme wiring
   - prompt layout tuning
   - plugin installation
   - GitHub 443 troubleshooting
3. Apply the minimum necessary change first.
4. Reload or source the affected zsh config.
5. For detailed command sequences and troubleshooting paths, read `references/zsh-setup-guide.md`.

## Rules

- Keep `~/.zshrc` changes minimal and reversible.
- Prefer enabling an existing Powerlevel10k install before suggesting a reinstall.
- If GitHub connectivity is broken, diagnose before suggesting theme or plugin reinstallation.
- Keep autosuggestions and syntax-highlighting loading near the end of `~/.zshrc`.
- Use fallback prompt styling only when Powerlevel10k cannot be used.

## Detailed Reference

- `references/zsh-setup-guide.md`
