# INSTALL

## Compatibility

**Primary support: Claude Code and OpenCode**

Both tools natively scan `~/.claude/skills/<name>/SKILL.md` and `.claude/skills/<name>/SKILL.md`, so installing once covers both. No separate OpenCode install needed. The skills use tool-specific features like automatic invocation (`/skill-name`) and argument parsing (`i=`, `o=`, `c=`).

**Other AI agents**

The skill content (procedures, rules, templates) is plain Markdown and works with other AI coding agents (Cursor, Codex, Windsurf, Aider, etc.). They have no built-in skill system, so you need to:

1. Include the skill files in your repo or reference them by path
2. Invoke them manually in prompts (e.g., "Read `skills/grilling/SKILL.md` and follow its procedure")
3. Provide context and arguments manually instead of using the `i=`, `o=` syntax

## Requirements

- Claude Code CLI installed
- Bash (macOS/Linux) or PowerShell 5.1+ (Windows)

## Install modes

| Mode | Target | Script |
|------|--------|--------|
| Personal | `~/.claude/skills/`, all sessions | `install-skills.sh` / `install-skills.ps1` |
| Project | `<project>/.claude/skills/`, that project only | `install-project.sh` |
| Global rules | `~/.claude/CLAUDE.md` + `~/.config/opencode/AGENTS.md` | `install-rules.sh` / `install-rules.ps1` |
| Status line | `~/.claude/settings.json` | `install-statusline.sh` / `install-statusline.ps1` |

On Windows, read [Windows](#windows) first: the WSL home is not the Windows home.

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

## Project install

Installs skills into `<target-project>/.claude/skills/`. Available only in that project.

```bash
chmod +x install-project.sh
./install-project.sh /path/to/your/project
```

`install-project.sh` has no PowerShell equivalent. On Windows use Git Bash or WSL, or copy manually:

```powershell
$dest = "C:\path\to\project\.claude\skills"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Path .\skills\* -Destination $dest -Recurse -Force
```

## Global rules install

Copies this repo's `rules/global.md` into `~/.claude/CLAUDE.md` (Claude Code) and
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

## Status line install

Installs a custom Claude Code status line
(`model | ctx:NN% | cwd | session`). The status line script is copied to
`~/.claude/` and `statusLine` is set in `~/.claude/settings.json`; all other
settings are preserved.

macOS/Linux (installs `statusline-command.sh`, requires `jq` on PATH; the step
is skipped with a `[skip]` notice if `jq` is missing):

```bash
chmod +x install-statusline.sh
./install-statusline.sh
```

Windows (PowerShell, installs `statusline-command.ps1`, no extra dependency):

```powershell
powershell -ExecutionPolicy Bypass -File .\install-statusline.ps1
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

## Windows

Skills must land in the home directory of the environment where Claude Code actually runs. Windows has two separate home directories, and mixing them is the usual failure:

| Environment | Home | Skills path |
|-------------|------|-------------|
| Windows (PowerShell / CMD) | `C:\Users\<you>` | `C:\Users\<you>\.claude\skills` |
| WSL | `/home/<you>` | `/home/<you>/.claude/skills` |

If you run Claude Code from PowerShell but install from WSL, the skills go to the WSL home and Claude Code never sees them.

Options, in order of preference:

- **PowerShell** (recommended): use the `.ps1` scripts. No bash, no WSL.
- **Git Bash**: ships with Git for Windows and its `$HOME` is `C:\Users\<you>`, so `./install-skills.sh` installs to the right place.
- **WSL, installing into the Windows home**: if you run Claude Code on Windows but only have bash in WSL, override `HOME`:

  ```bash
  HOME=/mnt/c/Users/<YourWindowsUser> ./install-skills.sh
  ```

  Running `./install-skills.sh` plainly inside WSL is correct only when you also run Claude Code inside WSL.

Verify from PowerShell:

```powershell
dir $env:USERPROFILE\.claude\skills
```

The skill files themselves (Markdown) are cross-platform and work on any OS.

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

Skills removed or renamed so far:

- `code-review` renamed to `task-review`
- `grill-me` replaced by `grilling`
- `to-prd`, `to-issues`, `draft-discussion`, `discussion-analysis`,
  `analysis-plan` removed (folded into `orchestrate` and `plan-tasks`)
- `bootstrap-spec-project` removed

If you installed before any of these changes, clean up with:

```bash
cd ~/.claude/skills && rm -rf code-review grill-me to-prd to-issues draft-discussion discussion-analysis analysis-plan bootstrap-spec-project
```

For a project install, use `<project>/.claude/skills/` instead of `~/.claude/skills/`.

PowerShell:

```powershell
$old = 'code-review','grill-me','to-prd','to-issues','draft-discussion','discussion-analysis','analysis-plan','bootstrap-spec-project'
$old | ForEach-Object { Remove-Item -Recurse -Force (Join-Path $env:USERPROFILE ".claude\skills\$_") -ErrorAction SilentlyContinue }
```
