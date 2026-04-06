# Zsh Setup Guide

## Quick Checklist

1. Confirm `~/.zshrc` exists and is loaded.
2. Ensure `compinit` is called.
3. Ensure `~/.powerlevel10k` exists, or advise how to create it.
4. Ensure `~/.p10k.zsh` exists, or create a sensible default.
5. Add or verify plugin loading for autosuggestions and syntax highlighting.
6. If `git clone` from GitHub fails, run HTTP/443 diagnostics and apply safe git config tweaks.

## Inspect Current zsh Config

Ensure at minimum:

```bash
autoload -Uz compinit && compinit
setopt AUTO_CD
```

If `compinit` is missing, add it near the top of `~/.zshrc`.

## Enable Powerlevel10k

Check:

- `~/.powerlevel10k`
- `~/.p10k.zsh`

Ensure the end of `~/.zshrc` contains:

```bash
if [ -d "$HOME/.powerlevel10k" ]; then
  source "$HOME/.powerlevel10k/powerlevel10k.zsh-theme"
  [[ -f "$HOME/.p10k.zsh" ]] && source "$HOME/.p10k.zsh"
fi
```

Reload:

```bash
exec zsh
```

If `~/.p10k.zsh` is missing but `~/.powerlevel10k/config/p10k-*.zsh` exists:

```bash
cp ~/.powerlevel10k/config/p10k-lean.zsh ~/.p10k.zsh
source ~/.p10k.zsh
```

## Fallback Prompt

If Powerlevel10k cannot be installed, use a simple fallback:

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

## Autosuggestions And Syntax Highlighting

Install:

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.zsh/zsh-syntax-highlighting
```

Load near the end of `~/.zshrc`:

```bash
if [ -f "$HOME/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh" ]; then
  source "$HOME/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh"
fi

if [ -f "$HOME/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ]; then
  source "$HOME/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
fi
```

Reload:

```bash
exec zsh
```

## Prompt Layout

Single-line:

```bash
typeset -g POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(
  dir
  vcs
  prompt_char
)
typeset -g POWERLEVEL9K_PROMPT_ADD_NEWLINE=false
source ~/.p10k.zsh
```

Two-line:

```bash
typeset -g POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(
  dir
  vcs
  newline
  prompt_char
)
typeset -g POWERLEVEL9K_PROMPT_ADD_NEWLINE=true
source ~/.p10k.zsh
```

## GitHub 443 Troubleshooting

Connectivity checks:

```bash
ping -c 3 github.com || echo 'PING_FAILED'
curl -v --connect-timeout 10 https://github.com 1>/dev/null
```

Proxy checks:

```bash
env | egrep 'HTTP_PROXY|HTTPS_PROXY|ALL_PROXY|NO_PROXY' || echo 'NO_PROXY_ENV'
git config --global --get-regexp 'http\\..*proxy' || echo 'NO_GIT_PROXY'
```

Safer git HTTP defaults:

```bash
git config --global http.version HTTP/1.1
git config --global http.lowSpeedLimit 1
git config --global http.lowSpeedTime 600
git config --global http.postBuffer 524288000
git config --global http.sslVerify true
```

Retry:

```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/.powerlevel10k
```

If it still fails, recommend another network or a manual ZIP download.

## Low-Risk Defaults

```bash
setopt HIST_FIND_NO_DUPS
HISTSIZE=10000
SAVEHIST=10000

alias ll='ls -lah'
alias gs='git status'
```
