# INSTALL

## Compatibility

**Primary support: Claude Code, OpenCode, and Google Antigravity**

- **Claude Code and OpenCode** both natively scan `~/.claude/skills/<name>/SKILL.md` and `<project>/.claude/skills/<name>/SKILL.md`.
- **Google Antigravity** (App, IDE, and `agy` CLI) scans `~/.gemini/config/skills/<name>/SKILL.md` globally and `<project>/.agents/skills/<name>/SKILL.md` per project. `install-skills` copies the skills to both `~/.claude/skills/` and `~/.gemini/config/skills/`.

The skills use slash invocation (`/skill-name`), subagents, and prompt argument conventions (`i=`, `o=`, `c=`), all supported across Claude Code, OpenCode, and Antigravity.

**Other AI agents**

The skill content (procedures, rules, templates) is plain Markdown and works with other AI coding agents (Cursor, Codex, Windsurf, Aider, etc.). Where a tool has no Agent Skills discovery, you can:

1. Include the skill files in your repo or reference them by path
2. Invoke them manually in prompts (e.g., "Read `skills/grilling/SKILL.md` and follow its procedure")
3. Provide context and arguments manually instead of using the `i=`, `o=` syntax

## Requirements

- At least one supported CLI/agent installed: Claude Code (`claude`), OpenCode (`opencode`), or Google Antigravity (`agy` / Antigravity IDE / Antigravity 2.0)
- Bash (macOS/Linux) or PowerShell 5.1+ (Windows)

## Install modes

| Mode | Target | Script |
|------|--------|--------|
| Personal | `~/.claude/skills/` + `~/.gemini/config/skills/` | `install-skills.sh` / `install-skills.ps1` |
| Project | `<project>/.claude/skills/` (+ `<project>/.agents/skills.json` for Antigravity) | [Manual install](#manual-install) |
| Global rules | `~/.claude/CLAUDE.md` + `~/.config/opencode/AGENTS.md` + `~/.gemini/config/AGENTS.md` | `install-rules.sh` / `install-rules.ps1` |
| Status line | `~/.claude/settings.json` (Claude Code only) | `install-statusline.sh` / `install-statusline.ps1` |

On Windows, read [Windows](#windows) first: the WSL home is not the Windows home.

## Personal install

Installs skills into `~/.claude/skills/` and `~/.gemini/config/skills/`, making them available across all Claude Code, OpenCode, and Antigravity sessions.

macOS/Linux:

```bash
chmod +x install-skills.sh
./install-skills.sh
```

Windows (PowerShell), installs into `C:\Users\<you>\.claude\skills` and `C:\Users\<you>\.gemini\config\skills`:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-skills.ps1
```

## Global rules install

Copies this repo's `rules/global.md` into `~/.claude/CLAUDE.md` (Claude Code),
`~/.config/opencode/AGENTS.md` (OpenCode), and `~/.gemini/config/AGENTS.md`
(Antigravity), so the behavioral guidelines apply to all sessions.

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
# Personal (Claude Code + OpenCode + Antigravity)
mkdir -p ~/.claude/skills ~/.gemini/config/skills
cp -r skills/* ~/.claude/skills/
cp -r skills/* ~/.gemini/config/skills/

# Project (available only in that project)
mkdir -p /path/to/project/.claude/skills /path/to/project/.agents
cp -r skills/* /path/to/project/.claude/skills/
printf '{\n  "entries": [\n    { "path": ".claude/skills" }\n  ]\n}\n' > /path/to/project/.agents/skills.json
```

PowerShell (project):

```powershell
$dest = "C:\path\to\project\.claude\skills"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Path .\skills\* -Destination $dest -Recurse -Force

$agyDir = "C:\path\to\project\.agents"
New-Item -ItemType Directory -Force -Path $agyDir | Out-Null
Set-Content -Path "$agyDir\skills.json" -Value '{"entries":[{"path":".claude/skills"}]}' -Encoding UTF8
```

### Antigravity sandbox note (separate specs repo)

Antigravity runs terminal commands inside a workspace sandbox by default. When a skill operates across two repositories (for example running in a specs repo while passing `c=/path/to/code-repo`, or passing `i=`/`o=` outside the open workspace), either:

- Add the second directory to the session (`agy --add-dir /path/to/other-repo`), or
- Set **Non-Workspace File Access** to `allow` in Antigravity Settings and approve out-of-sandbox execution when `git`, `Validate` or Definition of Done commands run in `c=`.

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

Open Claude Code or Antigravity (`agy`) in any directory (or the project directory for project installs) and run:

```
/help
```

(In `agy`, you can also run `/skills` to list all discovered skills.)

Skills appear in the command/skills list. If they do not appear:

1. Check that `~/.claude/skills/<skill-name>/SKILL.md` (Claude Code / OpenCode) and `~/.gemini/config/skills/<skill-name>/SKILL.md` (Antigravity) exist.
2. Restart the agent session.
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
