# INSTALL

## Compatibility

Skills installed here work in both **Claude Code** and **OpenCode**. OpenCode scans `~/.claude/skills/` and `.claude/skills/` natively. No separate OpenCode install needed.

## Requirements

- Claude Code CLI installed
- Bash (macOS/Linux) or PowerShell 5.1+ (Windows)

## Personal install

Installs skills into `~/.claude/skills/`. Available in all Claude Code sessions.

macOS/Linux:

```bash
chmod +x install-skills.sh
./install-skills.sh
```

Windows (PowerShell), installs into `C:\Users\<you>\.claude\skills`:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-skills.ps1
```

See the Windows section in `README.md` if you use WSL - the WSL home is not the Windows home.

## Global rules install

Copies this repo's `CLAUDE.md` into `~/.claude/CLAUDE.md` (Claude Code) and
`~/.config/opencode/AGENTS.md` (OpenCode), so the behavioral guidelines apply
to all sessions.

The content is written as a managed block between
`<!-- BEGIN spec-forge -->` and `<!-- END spec-forge -->` markers. Only that
block is replaced on re-run; everything else in those files is preserved.

macOS/Linux:

```bash
chmod +x install-rules.sh
./install-rules.sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File .\install-rules.ps1
```

### Status line

The same scripts also install a custom Claude Code status line
(`model | ctx:NN% | cwd | session`). The status line script is copied to
`~/.claude/` and `statusLine` is set in `~/.claude/settings.json`; all other
settings are preserved.

- macOS/Linux: installs `statusline-command.sh`, requires `jq` on PATH
  (the step is skipped with a `[skip]` notice if `jq` is missing).
- Windows: installs `statusline-command.ps1`, no extra dependency.

## Project install

Installs skills into `<target-project>/.claude/skills/`. Available only in that project.

```bash
chmod +x install-project.sh
./install-project.sh /path/to/your/project
```

## Manual install

```bash
# Personal
mkdir -p ~/.claude/skills
cp -r skills/* ~/.claude/skills/

# Project
mkdir -p /path/to/project/.claude/skills
cp -r skills/* /path/to/project/.claude/skills/
```

## Verify installation

Open Claude Code in any directory (or the project directory for project installs) and run:

```
/help
```

Skills appear in the command list. If they do not appear:

1. Check that `.claude/skills/<skill-name>/SKILL.md` exists.
2. Restart Claude Code.
3. Verify you are in the correct directory for project-scoped skills.

## Update

Re-run the install script. It overwrites existing files. Idempotent for additions and changes.

### Removing stale skills (manual)

The installers only copy; they never prune. A skill that was deleted or renamed
in this repo keeps living in your install directory and keeps showing up in
Claude Code alongside the new name. Remove those directories yourself.

`to-prd` and `to-issues` were deleted, and `code-review` was renamed to
`task-review`. If you installed before that change, clean up with:

```bash
rm -rf ~/.claude/skills/to-prd ~/.claude/skills/to-issues ~/.claude/skills/code-review
```

For a project install, use `<project>/.claude/skills/` instead of `~/.claude/skills/`.

PowerShell:

```powershell
Remove-Item -Recurse -Force $env:USERPROFILE\.claude\skills\to-prd, $env:USERPROFILE\.claude\skills\to-issues, $env:USERPROFILE\.claude\skills\code-review -ErrorAction SilentlyContinue
```
