# spec-forge

Skill pack for Claude Code implementing a staged, file-driven planning workflow.

## Workflow

```
draft.md
  -> /draft-discussion    -> discussion.md (+ discussion-qa.md)
  -> /discussion-analysis -> analysis.md
  -> /analysis-plan       -> plan.md  (review + approve before next step)
  -> /plan-tasks          -> tasks/todo/<prefix>-task-01.md
                             tasks/todo/<prefix>-task-02.md
                             ...
```

At session end: `/handoff` -> sessions/<name>.md

To start a new project: `/bootstrap-spec-project` -> ~/ai-specs/<project>/

## Skills

| Skill | Input | Output | Stage |
|-------|-------|--------|-------|
| `draft-discussion` | draft.md | discussion.md + discussion-qa.md | Clarification |
| `discussion-analysis` | discussion.md | analysis.md | Analysis |
| `analysis-plan` | analysis.md | plan.md | Planning (approval gate) |
| `plan-tasks` | plan.md | tasks/todo/*.md (one per task) | Decomposition |
| `handoff` | session state | sessions/*.md | Continuity |
| `bootstrap-spec-project` | project/feature names | directory tree | Scaffolding |

## Arguments

All skills use short argument names:

| Arg | Stands for | Used by |
|-----|-----------|---------|
| `i` | input / source file | draft-discussion, discussion-analysis, analysis-plan, plan-tasks |
| `o` | output file or directory | all writing skills (file; `plan-tasks` writes to a directory) |
| `p` | prefix (task IDs) / project name | plan-tasks (prefix), bootstrap-spec-project (project) |
| `f` | feature name | bootstrap-spec-project |
| `n` | next-session purpose | handoff |

## Example invocations

```
/draft-discussion i=inbox/idea.md o=features/auth/discussion.md

/discussion-analysis i=features/auth/discussion.md o=features/auth/analysis.md

/analysis-plan i=features/auth/analysis.md o=features/auth/plan.md

/plan-tasks i=features/auth/plan.md o=features/auth/tasks/todo/ p=auth

/handoff o=sessions/2026-05-23-auth.md n="Begin auth-task-01 implementation"

/bootstrap-spec-project p=my-app f=user-auth
```

## Install modes

**Personal** (`~/.claude/skills/`): skills available in all Claude Code sessions.

**Project** (`<project>/.claude/skills/`): skills available only within that project directory.

See `INSTALL.md` for exact commands.

## Compatibility

Works in both **Claude Code** and **OpenCode** with no extra steps. OpenCode scans `~/.claude/skills/<name>/SKILL.md` and `.claude/skills/<name>/SKILL.md` natively alongside its own paths. Installing once covers both tools.

## Workflow guide

1. Write a rough idea in `inbox/` or `features/<name>/inbox/` (no structure required). Unscoped ideas go in `backlog/`.
2. `/draft-discussion` - Claude asks 8-12 clarifying questions, then writes `discussion.md`. The questions and your verbatim answers are saved alongside in `discussion-qa.md`, written after each round.
3. `/discussion-analysis` - Claude reads discussion, separates facts from assumptions, writes `analysis.md`.
4. `/analysis-plan` - Claude sequences work, identifies dependencies, writes `plan.md`, then STOPS for your review and approval before `plan-tasks` runs.
5. `/plan-tasks` - Claude decomposes the approved plan into atomic tasks, writes one file per task into `tasks/todo/`.
6. Work tasks. Move individual task files from `tasks/todo/` to `tasks/done/` when complete.
7. `/handoff` at session end to write a resumable session document.

No stage produces code unless explicitly required. Every stage writes a reviewable file, and `analysis-plan` requires your explicit approval before the plan is decomposed into tasks.

## Project structure (ai-specs)

After running `/bootstrap-spec-project p=my-app f=user-auth`:

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
