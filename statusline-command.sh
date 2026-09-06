#!/bin/sh
unset LC_ALL
export LC_NUMERIC=C
input=$(cat)

if ! command -v jq >/dev/null 2>&1; then
  printf "statusline: jq not installed (run: sudo apt install jq)"
  exit 0
fi

cwd=$(echo "$input" | jq -r '.workspace.current_dir // ""')
model=$(echo "$input" | jq -r '.model.display_name // "Unknown"')
used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
session_name=$(echo "$input" | jq -r '.session_name // empty')

if [ -n "$used_pct" ]; then
  ctx=$(printf "ctx:%.0f%%" "$used_pct")
else
  ctx="ctx:-"
fi

if [ -n "$session_name" ]; then
  printf "%s | %s | %s | %s" "$model" "$ctx" "$cwd" "$session_name"
else
  printf "%s | %s | %s" "$model" "$ctx" "$cwd"
fi