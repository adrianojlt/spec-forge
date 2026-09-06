#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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
        echo "         install it with one of:"
        echo "           Debian/Ubuntu : sudo apt install jq"
        echo "           Fedora        : sudo dnf install jq"
        echo "           Arch          : sudo pacman -S jq"
        echo "           macOS         : brew install jq"
        echo "         then re-run this script"
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
