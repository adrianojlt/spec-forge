# my-ai-files

Skill pack for Claude Code implementing a staged, file-driven planning workflow.

## Workflow

```
draft.md
  -> /draft-discussion    -> discussion.md
  -> /discussion-analysis -> analysis.md
  -> /analysis-plan       -> plan.md
  -> /plan-tasks          -> BACKLOG.md
```

At session end: `/handoff` -> sessions/<name>.md

To start a new project: `/bootstrap-spec-project` -> ~/ai-specs/<project>/

## Skills

| Skill | Input | Output | Stage |
|-------|-------|--------|-------|
| `draft-discussion` | draft.md | discussion.md | Clarification |
| `discussion-analysis` | discussion.md | analysis.md | Analysis |
| `analysis-plan` | analysis.md | plan.md | Planning |
| `plan-tasks` | plan.md | BACKLOG.md | Decomposition |
| `handoff` | session state | sessions/*.md | Continuity |
| `bootstrap-spec-project` | project/feature names | directory tree | Scaffolding |

## Example invocations

```
/draft-discussion source_file=inbox/idea.md target_file=features/auth/discussion.md

/discussion-analysis source_file=features/auth/discussion.md target_file=features/auth/analysis.md

/analysis-plan source_file=features/auth/analysis.md target_file=features/auth/plan.md

/plan-tasks source_file=features/auth/plan.md target_file=features/auth/BACKLOG.md

/handoff target_file=sessions/2026-05-23-auth.md next_purpose="Begin AUTH-001 implementation"

/bootstrap-spec-project project_name=my-app feature_name=user-auth
```

## Install modes

**Personal** (`~/.claude/skills/`): skills available in all Claude Code sessions.

**Project** (`<project>/.claude/skills/`): skills available only within that project directory.

See `INSTALL.md` for exact commands.

## Workflow guide

1. Write a rough idea in `inbox/` or `features/<name>/inbox/` (no structure required).
2. `/draft-discussion` - Claude asks 8-12 clarifying questions, then writes `discussion.md`.
3. `/discussion-analysis` - Claude reads discussion, separates facts from assumptions, writes `analysis.md`.
4. `/analysis-plan` - Claude sequences work, identifies dependencies, writes `plan.md`.
5. `/plan-tasks` - Claude decomposes plan into atomic tasks with acceptance criteria, writes `BACKLOG.md`.
6. Work tasks. Move completed tasks from `tasks/todo/` to `tasks/done/`.
7. `/handoff` at session end to write a resumable session document.

No stage produces code unless explicitly required. Each stage is reviewable before the next begins.

## Project structure (ai-specs)

After running `/bootstrap-spec-project project_name=my-app feature_name=user-auth`:

```
~/ai-specs/my-app/
  README.md
  features/
    user-auth/
      inbox/
      tasks/
        todo/
        done/
      sessions/
  prompts/
  sessions/
```
