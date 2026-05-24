# my-ai-files

Skill pack for Claude Code implementing a staged, file-driven planning workflow.

## Workflow

```
draft.md
  -> /draft-discussion    -> discussion.md
  -> /discussion-analysis -> analysis.md
  -> /analysis-plan       -> plan.md
  -> /plan-tasks          -> tasks/todo/<prefix>-task-01.md
                             tasks/todo/<prefix>-task-02.md
                             ...
```

At session end: `/handoff` -> sessions/<name>.md

To start a new project: `/bootstrap-spec-project` -> ~/ai-specs/<project>/

## Skills

| Skill | Input | Output | Stage |
|-------|-------|--------|-------|
| `draft-discussion` | draft.md | discussion.md | Clarification |
| `discussion-analysis` | discussion.md | analysis.md | Analysis |
| `analysis-plan` | analysis.md | plan.md | Planning |
| `plan-tasks` | plan.md | tasks/todo/*.md (one per task) | Decomposition |
| `handoff` | session state | sessions/*.md | Continuity |
| `bootstrap-spec-project` | project/feature names | directory tree | Scaffolding |

## Example invocations

```
/draft-discussion source_file=inbox/idea.md target_file=features/auth/discussion.md

/discussion-analysis source_file=features/auth/discussion.md target_file=features/auth/analysis.md

/analysis-plan source_file=features/auth/analysis.md target_file=features/auth/plan.md

/plan-tasks source_file=features/auth/plan.md tasks_dir=features/auth/tasks/todo/ prefix=auth

/handoff target_file=sessions/2026-05-23-auth.md next_purpose="Begin auth-task-01 implementation"

/bootstrap-spec-project project_name=my-app feature_name=user-auth
```

## Install modes

**Personal** (`~/.claude/skills/`): skills available in all Claude Code sessions.

**Project** (`<project>/.claude/skills/`): skills available only within that project directory.

See `INSTALL.md` for exact commands.

## Compatibility

Works in both **Claude Code** and **OpenCode** with no extra steps. OpenCode scans `~/.claude/skills/<name>/SKILL.md` and `.claude/skills/<name>/SKILL.md` natively alongside its own paths. Installing once covers both tools.

## Workflow guide

1. Write a rough idea in `inbox/` or `features/<name>/inbox/` (no structure required). Unscoped ideas go in `backlog/`.
2. `/draft-discussion` - Claude asks 8-12 clarifying questions, then writes `discussion.md`.
3. `/discussion-analysis` - Claude reads discussion, separates facts from assumptions, writes `analysis.md`.
4. `/analysis-plan` - Claude sequences work, identifies dependencies, writes `plan.md`.
5. `/plan-tasks` - Claude decomposes plan into atomic tasks, writes one file per task into `tasks/todo/`.
6. Work tasks. Move individual task files from `tasks/todo/` to `tasks/done/` when complete.
7. `/handoff` at session end to write a resumable session document.

No stage produces code unless explicitly required. Each stage is reviewable before the next begins.

## Project structure (ai-specs)

After running `/bootstrap-spec-project project_name=my-app feature_name=user-auth`:

```
~/ai-specs/my-app/
  README.md
  overview/                 <- project docs (architecture, decisions, context)
  backlog/                  <- loose ideas not yet in the planning pipeline
  tasks/
    todo/                   <- simple tasks not tied to a feature
    done/
  features/
    user-auth/
      inbox/
      tasks/
        todo/               <- task files (user-auth-task-01.md, ...)
        done/
      sessions/
  prompts/
  sessions/
```
