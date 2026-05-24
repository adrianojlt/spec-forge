# INSTALL

## Compatibility

Skills installed here work in both **Claude Code** and **OpenCode**. OpenCode scans `~/.claude/skills/` and `.claude/skills/` natively. No separate OpenCode install needed.

## Requirements

- Claude Code CLI installed
- Bash (macOS/Linux)

## Personal install

Installs skills into `~/.claude/skills/`. Available in all Claude Code sessions.

```bash
chmod +x install-personal.sh
./install-personal.sh
```

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

Re-run the install script. It overwrites existing files. Idempotent.
