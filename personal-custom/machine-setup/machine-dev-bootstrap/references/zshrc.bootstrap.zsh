# Cursor zsh basic setup
autoload -Uz compinit && compinit

# Better completion behavior
zmodload zsh/complist
setopt COMPLETE_IN_WORD
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'

# Search history by the prefix already typed with Up/Down
autoload -Uz up-line-or-beginning-search down-line-or-beginning-search
zle -N up-line-or-beginning-search
zle -N down-line-or-beginning-search
bindkey "${terminfo[kcuu1]}" up-line-or-beginning-search
bindkey "${terminfo[kcud1]}" down-line-or-beginning-search
bindkey '^[[A' up-line-or-beginning-search
bindkey '^[[B' down-line-or-beginning-search

# Convenience: allow `cd dir` without typing `cd`
setopt AUTO_CD

# History: avoid duplicate consecutive commands
setopt HIST_IGNORE_DUPS
setopt HIST_FIND_NO_DUPS

HISTSIZE=10000
SAVEHIST=10000

# Common aliases
alias ll='ls -lah'
alias gs='git status'

# Android/Java toolchain (Siuper project)
export JAVA_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
export ANDROID_SDK_ROOT="$HOME/Library/Android/sdk"
export ANDROID_HOME="$ANDROID_SDK_ROOT"
export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"
export PATH="/opt/homebrew/bin:$PATH"
export PATH="$ANDROID_SDK_ROOT/platform-tools:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$PATH"

# Force outbound traffic through local proxy (overseas node).
# Use proxy_off to temporarily disable, proxy_on to re-enable.
export PROXY_URL="http://127.0.0.1:7897"
export http_proxy="$PROXY_URL"
export https_proxy="$PROXY_URL"
export HTTP_PROXY="$PROXY_URL"
export HTTPS_PROXY="$PROXY_URL"
export ALL_PROXY="socks5://127.0.0.1:7897"
export all_proxy="$ALL_PROXY"
export NO_PROXY="localhost,127.0.0.1,::1"
export no_proxy="$NO_PROXY"

proxy_on() {
  export http_proxy="$PROXY_URL"
  export https_proxy="$PROXY_URL"
  export HTTP_PROXY="$PROXY_URL"
  export HTTPS_PROXY="$PROXY_URL"
  export ALL_PROXY="socks5://127.0.0.1:7897"
  export all_proxy="$ALL_PROXY"
  export NO_PROXY="localhost,127.0.0.1,::1"
  export no_proxy="$NO_PROXY"
  echo "Proxy ON -> $PROXY_URL"
}

proxy_off() {
  unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY all_proxy NO_PROXY no_proxy
  echo "Proxy OFF"
}

# Powerlevel10k prompt theme
if [ -d "$HOME/.powerlevel10k" ]; then
  source "$HOME/.powerlevel10k/powerlevel10k.zsh-theme"
  [[ -f "$HOME/.p10k.zsh" ]] && source "$HOME/.p10k.zsh"
else
  # Fallback prompt while powerlevel10k is not installed yet.
  autoload -Uz colors && colors
  setopt PROMPT_SUBST
  PROMPT='%F{39}%n%f@%F{214}%m%f %F{82}%~%f %(?.%F{10}✔.%F{196}✘)%f %# '
fi

# Autosuggestions
if [ -f "$HOME/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh" ]; then
  source "$HOME/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh"
fi

# Syntax highlighting (keep near the end of .zshrc)
if [ -f "$HOME/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ]; then
  source "$HOME/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
fi

# rbenv
eval "$(rbenv init - zsh)"

# Auto-bootstrap shared AI sync files for any project entered from the shell.
if [ -f "$HOME/.codex/project-ai-sync-auto.zsh" ]; then
  source "$HOME/.codex/project-ai-sync-auto.zsh"
fi
