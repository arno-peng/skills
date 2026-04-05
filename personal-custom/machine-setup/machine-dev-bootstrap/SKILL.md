---
name: machine-dev-bootstrap
description: Use when initializing or rebuilding this machine's development environment, especially to restore the standard zsh baseline, terminal behavior, Java/Android paths, proxy helpers, prompt setup, and shell plugin wiring used on this Mac.
---

# Machine Dev Bootstrap

Use this skill when the user wants to bootstrap or restore the baseline development environment on this machine.

## Scope

This skill stores the canonical shell baseline currently used on this Mac.

Primary reference:

- `references/zshrc.bootstrap.zsh`

## Workflow

1. Read the user's current `~/.zshrc` before changing anything.
2. Use `references/zshrc.bootstrap.zsh` as the canonical baseline for the shell setup.
3. Merge carefully instead of blindly replacing unrelated user customizations.
4. Re-check machine-specific values before applying:
   - `JAVA_HOME`
   - `ANDROID_SDK_ROOT` / `ANDROID_HOME`
   - `PROXY_URL` and proxy ports
   - optional plugin/theme paths under `$HOME/.zsh` and `$HOME/.powerlevel10k`
5. Validate with `zsh -n ~/.zshrc`.
6. Reload with `source ~/.zshrc` or `exec zsh`.

## What The Baseline Includes

- `compinit` and zsh completion menu selection
- `Tab` completion with case-insensitive matching
- `Up` / `Down` history search by the already typed prefix
- history de-duplication and `AUTO_CD`
- common aliases
- Java 17 and Android SDK paths
- local proxy helper functions `proxy_on` and `proxy_off`
- Powerlevel10k loading with a pure-zsh fallback prompt
- `zsh-autosuggestions` and `zsh-syntax-highlighting` hooks
- `rbenv` initialization
- Codex project AI sync auto-bootstrap sourcing

## Notes

- The reference file intentionally preserves the current machine values instead of abstracting everything away.
- When the shell baseline changes in a meaningful way, update this skill so future machine setup work uses the same source of truth.
