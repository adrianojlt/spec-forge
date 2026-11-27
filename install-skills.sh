#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$SCRIPT_DIR/skills"
SKILL_DESTS=(
    "$HOME/.claude/skills"
    "$HOME/.gemini/config/skills"
)

if [[ ! -d "$SKILL_SRC" ]]; then
    echo "Error: skills directory not found at $SKILL_SRC"
    exit 1
fi

for skill_dest in "${SKILL_DESTS[@]}"; do
    echo "Installing skills to: $skill_dest"
    mkdir -p "$skill_dest"

    for skill_dir in "$SKILL_SRC"/*/; do
        skill_name="$(basename "$skill_dir")"
        dest="$skill_dest/$skill_name"
        mkdir -p "$dest"
        cp -r "$skill_dir"* "$dest/"
        echo "  [ok] $skill_name"
    done
    echo ""
done

echo "Done. $(ls -1d "$SKILL_SRC"/*/ | wc -l | tr -d ' ') skills installed to ${SKILL_DESTS[*]}"
