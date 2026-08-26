#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_SRC="$SCRIPT_DIR/CLAUDE.md"

BEGIN_TAG="<!-- BEGIN spec-forge (managed by install-rules) -->"
END_TAG="<!-- END spec-forge -->"

if [[ ! -f "$CLAUDE_SRC" ]]; then
    echo "Error: source not found at $CLAUDE_SRC"
    exit 1
fi

install_managed_section() {
    local target="$1"

    mkdir -p "$(dirname "$target")"
    touch "$target"

    local tmp
    tmp="$(mktemp)"
    if grep -qF "$BEGIN_TAG" "$target" && grep -qF "$END_TAG" "$target"; then
        awk -v begin="$BEGIN_TAG" -v end="$END_TAG" '
            {
                line = $0
                if (!skip) {
                    pos = index(line, begin)
                    if (pos > 0) {
                        if (pos > 1) print substr(line, 1, pos - 1)
                        line = substr(line, pos + length(begin))
                        skip = 1
                    }
                }
                if (skip) {
                    pos = index(line, end)
                    if (pos > 0) {
                        rest = substr(line, pos + length(end))
                        if (rest != "") print rest
                        skip = 0
                    }
                    next
                }
                print line
            }
        ' "$target" > "$tmp"
        mv "$tmp" "$target"
    else
        rm -f "$tmp"
    fi

    {
        printf '%s\n' "$BEGIN_TAG"
        cat "$CLAUDE_SRC"
        printf '%s\n' "$END_TAG"
    } >> "$target"
}

install_managed_section "$HOME/.claude/CLAUDE.md"
echo "  [ok] CLAUDE.md -> $HOME/.claude/CLAUDE.md"

install_managed_section "$HOME/.config/opencode/AGENTS.md"
echo "  [ok] CLAUDE.md -> $HOME/.config/opencode/AGENTS.md"

install_statusline() {
    local src="$SCRIPT_DIR/statusline-command.sh"
    local dest="$HOME/.claude/statusline-command.sh"
    local settings="$HOME/.claude/settings.json"

    if [[ ! -f "$src" ]]; then
        echo "  [skip] statusline: source not found at $src"
        return
    fi

    if ! command -v jq >/dev/null 2>&1; then
        echo "  [skip] statusline: jq not installed"
        return
    fi

    mkdir -p "$HOME/.claude"
    cp "$src" "$dest"
    chmod +x "$dest"

    if [[ ! -s "$settings" ]]; then
        printf '{}\n' > "$settings"
    fi

    local tmp
    tmp="$(mktemp)"
    jq --arg cmd "sh $dest" '.statusLine = {type: "command", command: $cmd}' "$settings" > "$tmp"
    mv "$tmp" "$settings"

    echo "  [ok] statusline -> $dest"
}

install_statusline
