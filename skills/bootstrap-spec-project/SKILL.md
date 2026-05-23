---
name: bootstrap-spec-project
description: Bootstrap a new ai-specs project directory structure under ~/ai-specs/. Runs a bundled shell script.
argument-hint: "project_name=<name> feature_name=<name>"
disable-model-invocation: true
---

# bootstrap-spec-project

## Purpose
Create a new project structure under `~/ai-specs/<project_name>/` with the standard ai-specs layout. Intended to be run from within `~/ai-specs/` or any directory.

## Inputs
- `$project_name` - name of the project directory to create
- `$feature_name` - name of the first feature to scaffold

## Procedure

**Step 1 - Locate script**
The bundled script lives inside this skill's directory. Resolve the path based on where this SKILL.md is installed:

- Personal install: `~/.claude/skills/bootstrap-spec-project/scripts/bootstrap_spec_project.sh`
- Project install: `<project>/.claude/skills/bootstrap-spec-project/scripts/bootstrap_spec_project.sh`

**Step 2 - Run script**
Execute the script with the two required arguments:

```bash
bash /path/to/skill/scripts/bootstrap_spec_project.sh "$project_name" "$feature_name"
```

The script is idempotent. Running it again on an existing project is safe.

**Step 3 - Report**
Show the full output from the script (created paths). Confirm structure is ready and show the recommended first command to use.

## Hard rules
- Do not create files outside `~/ai-specs/`.
- Do not modify existing files or directories.
- Report the full created path list to the user after the script runs.

## Output
A directory tree under `~/ai-specs/<project_name>/` as defined in `template.md`.

## Validation
After script runs, confirm that the expected directory structure exists.
