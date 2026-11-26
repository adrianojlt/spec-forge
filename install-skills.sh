#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$SCRIPT_DIR/skills"
SKILL_DEST="$HOME/.claude/skills"

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

register_antigravity_skills() {
    local config_path="$HOME/.gemini/config/skills.json"
    local target_entry="~/.claude/skills"

    mkdir -p "$(dirname "$config_path")"

    if [[ ! -s "$config_path" ]]; then
        cat > "$config_path" <<'EOF'
{
  "entries": [
    {
      "path": "~/.claude/skills"
    }
  ]
}
EOF
        echo "  [ok] Antigravity skills pointer -> $config_path ($target_entry)"
        return
    fi

    if command -v jq >/dev/null 2>&1; then
        local tmp
        tmp="$(mktemp)"
        jq --arg p "$target_entry" '
            .entries = ((.entries // []) | if any(.[]; .path == $p) then . else . + [{path: $p}] end)
        ' "$config_path" > "$tmp"
        mv "$tmp" "$config_path"
        echo "  [ok] Antigravity skills pointer -> $config_path ($target_entry)"
    elif command -v python3 >/dev/null 2>&1; then
        python3 - "$config_path" "$target_entry" <<'PY'
import json, sys
path, target = sys.argv[1], sys.argv[2]
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
entries = data.setdefault("entries", [])
if not any(isinstance(e, dict) and e.get("path") == target for e in entries):
    entries.append({"path": target})
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
PY
        echo "  [ok] Antigravity skills pointer -> $config_path ($target_entry)"
    elif grep -qF "$target_entry" "$config_path"; then
        echo "  [ok] Antigravity skills pointer already present in $config_path"
    else
        echo "  [skip] $config_path already exists and neither jq nor python3 is available to merge $target_entry"
    fi
}

echo ""
register_antigravity_skills
echo ""
echo "Done. $(ls -1d "$SKILL_SRC"/*/ | wc -l | tr -d ' ') skills installed to $SKILL_DEST"
