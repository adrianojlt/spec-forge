#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Error: target project directory required"
    echo "Usage: $0 <target-project-directory>"
    exit 1
fi

TARGET_PROJECT="${1%/}"

if [[ ! -d "$TARGET_PROJECT" ]]; then
    echo "Error: target directory does not exist: $TARGET_PROJECT"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$SCRIPT_DIR/skills"
SKILL_DEST="$TARGET_PROJECT/.claude/skills"

if [[ ! -d "$SKILL_SRC" ]]; then
    echo "Error: skills directory not found at $SKILL_SRC"
    exit 1
fi

echo "Installing skills to: $SKILL_DEST"
mkdir -p "$SKILL_DEST"

for skill_dir in "$SKILL_SRC"/*/; do
    skill_name="$(basename "$skill_dir")"
    dest="$SKILL_DEST/$skill_name"
    mkdir -p "$dest"
    cp -r "$skill_dir"* "$dest/"
    echo "  [ok] $skill_name"
done

echo ""
echo "Done. $(ls -1d "$SKILL_SRC"/*/ | wc -l | tr -d ' ') skills installed to $SKILL_DEST"
