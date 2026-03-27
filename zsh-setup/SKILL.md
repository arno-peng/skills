---
name: zsh-setup
description: Configure and troubleshoot zsh themes (Powerlevel10k), plugins, and prompt style. Use when the user wants to adjust terminal zsh appearance, install or tweak Powerlevel10k, add autosuggestions/syntax highlighting, or debug GitHub 443/git clone issues affecting theme installation.
---

# Zsh Setup & Theme Skill

## When to use this skill

Use this skill whenever the user:

- Mentions "zsh", "终端风格", "terminal theme", "Powerlevel10k/p10k", or "oh-my-zsh".
- Wants to:
  - Install or enable Powerlevel10k as the zsh theme.
  - Switch between multi-line and single-line prompts.
  - Add `zsh-autosuggestions` and `zsh-syntax-highlighting`.
  - Improve the look of the prompt without external downloads (fallback mode).
  - Diagnose git/GitHub 443 issues preventing theme installation.

Assume the default shell is zsh on macOS unless told otherwise.

## Quick checklist

1. Confirm `~/.zshrc` exists and is loaded.
2. Ensure `compinit` is called.
3. Ensure `~/.powerlevel10k` exists (or advise how to create it).
4. Ensure `~/.p10k.zsh` exists (or create a sensible default).
5. Add/verify plugin loading for autosuggestions and syntax highlighting.
6. If git clone from GitHub fails, run HTTP/443 diagnostics and apply safe git config tweaks.

---

## Step 1: Inspect current zsh config

- Read `~/.zshrc`.
- Ensure at minimum:

```bash
autoload -Uz compinit && compinit
setopt AUTO_CD
```

- If `compinit` is missing, add it near the top of `~/.zshrc`.

---

## Step 2: Enable Powerlevel10k if installed

### 2.1: Check install paths

- Check for theme directory:
  - `~/.powerlevel10k` should contain `powerlevel10k.zsh-theme` and `config/` profiles.
- Check for user config:
  - `~/.p10k.zsh` is the user-specific theme config.

### 2.2: Wire into `~/.zshrc`

Append (or ensure present) at the end of `~/.zshrc`:

```bash
# Powerlevel10k prompt theme
if [ -d "$HOME/.powerlevel10k" ]; then
  source "$HOME/.powerlevel10k/powerlevel10k.zsh-theme"
  [[ -f "$HOME/.p10k.zsh" ]] && source "$HOME/.p10k.zsh"
fi
```

Reload with:

```bash
exec zsh
```

If `~/.p10k.zsh` is missing but `~/.powerlevel10k/config/p10k-*.zsh` exist, create a default:

```bash
cp ~/.powerlevel10k/config/p10k-lean.zsh ~/.p10k.zsh
```

Then:

```bash
source ~/.p10k.zsh
```

Optionally, advise the user to run `p10k configure` interactively later.

---

## Step 3: Fallback theme when Powerlevel10k cannot be installed

If GitHub is unreachable or `~/.powerlevel10k` cannot be cloned, provide a pure-zsh fallback so the user still sees a nice prompt.

Append inside the Powerlevel10k block’s `else` branch in `~/.zshrc`:

```bash
if [ -d "$HOME/.powerlevel10k" ]; then
  source "$HOME/.powerlevel10k/powerlevel10k.zsh-theme"
  [[ -f "$HOME/.p10k.zsh" ]] && source "$HOME/.p10k.zsh"
else
  autoload -Uz colors && colors
  setopt PROMPT_SUBST
  PROMPT='%F{39}%n%f@%F{214}%m%f %F{82}%~%f %(?.%F{10}✔.%F{196}✘)%f %# '
fi
```

This yields a single-line, colored prompt with user, host, path, and success/fail indicator without any external theme.

---

## Step 4: Add autosuggestions & syntax highlighting

### 4.1: Installation commands (advise the user to run)

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.zsh/zsh-syntax-highlighting
```

### 4.2: Load plugins in `~/.zshrc`

Append near the end of `~/.zshrc` (after Powerlevel10k and other theming, but before any final custom PROMPT overrides):

```bash
# Autosuggestions
if [ -f "$HOME/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh" ]; then
  source "$HOME/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh"
fi

# Syntax highlighting (keep near the end of .zshrc)
if [ -f "$HOME/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ]; then
  source "$HOME/.zsh/zsh-syntax-highlighting.zsh"
fi
```

Reload:

```bash
exec zsh
```

---

## Step 5: Switch Powerlevel10k between multi-line and single-line

All layout is controlled in `~/.p10k.zsh`.

### 5.1: Single-line prompt (recommended default)

- In the `POWERLEVEL9K_LEFT_PROMPT_ELEMENTS` section, ensure only one logical line and no `newline` segment:

```bash
typeset -g POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(
  dir          # current directory
  vcs          # git status
  prompt_char  # prompt symbol
)
```

- In `POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS`, remove `newline` at the end (keep everything on the same line).
- Ensure:

```bash
typeset -g POWERLEVEL9K_PROMPT_ADD_NEWLINE=false
```

Reload just the theme:

```bash
source ~/.p10k.zsh
```

### 5.2: Two-line prompt

To restore a two-line lean style:

- Left prompt elements, with explicit `newline` and prompt char on line 2:

```bash
typeset -g POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(
  dir
  vcs
  newline
  prompt_char
)
```

- Optionally set:

```bash
typeset -g POWERLEVEL9K_PROMPT_ADD_NEWLINE=true
```

Reload with `source ~/.p10k.zsh`.

---

## Step 6: Diagnose and mitigate GitHub:443 / git clone failures

When `git clone https://github.com/...` fails with HTTP/2 or 443 errors:

### 6.1: Basic connectivity checks

Run (or instruct the user to run):

```bash
ping -c 3 github.com || echo 'PING_FAILED'

curl -v --connect-timeout 10 https://github.com 1>/dev/null
```

Interpretation:

- If ping and curl both succeed (HTTP 200, TLS OK), 443 is reachable and DNS/TLS are fine.
- If curl to `/` works but `git clone` hangs or fails with `HTTP2 framing` errors, suspect middleboxes/ISP issues specific to long-lived git HTTP/2 streams.

### 6.2: Check for proxy interference

Check environment:

```bash
env | egrep 'HTTP_PROXY|HTTPS_PROXY|ALL_PROXY|NO_PROXY' || echo 'NO_PROXY_ENV'
git config --global --get-regexp 'http\\..*proxy' || echo 'NO_GIT_PROXY'
```

If proxies are configured and suspicious, suggest disabling them for GitHub or temporarily unsetting them.

### 6.3: Apply safer git HTTP settings

Set conservative defaults (idempotent and safe):

```bash
git config --global http.version HTTP/1.1
git config --global http.lowSpeedLimit 1
git config --global http.lowSpeedTime 600
git config --global http.postBuffer 524288000
git config --global http.sslVerify true
```

Then retry:

```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/.powerlevel10k
```

If clone still fails after all of this, recommend one of:

- Switching to a different network (hotspot / home Wi‑Fi).
- Using a browser to download the ZIP and manually placing it at `~/.powerlevel10k`.

After a manual install, follow Step 2 to wire it into zsh.

---

## Step 7: Minimal alias & quality-of-life defaults

When zsh configuration is almost empty, you can safely add a few helpful defaults:

```bash
setopt HIST_IGNORE_DUPS
setopt HIST_FIND_NO_DUPS
HISTSIZE=10000
SAVEHIST=10000

alias ll='ls -lah'
alias gs='git status'
```

These are simple, low-risk improvements that pair well with the theme and plugins above.

---

## Usage examples

- **"帮我调整下终端 zsh 的风格" / "change my zsh theme"**
  - Use Steps 1–5:
    - Ensure zsh basics in `~/.zshrc`.
    - Install or wire `~/.powerlevel10k`.
    - Create a default `~/.p10k.zsh` (lean).
    - Switch to single-line prompt or two-line prompt as requested.
    - Add autosuggestions and syntax highlighting.

- **"Powerlevel10k 安装不动，443 有问题" / "git clone from GitHub hangs on 443"**
  - Use Step 6:
    - Validate network connectivity with `ping` and `curl`.
    - Check environment/git HTTP proxy.
    - Apply safe git HTTP settings.
    - If all fails, recommend alternative network or manual ZIP download.

