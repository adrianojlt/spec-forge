# spec-forge

Skill pack for Claude Code implementing a staged, file-driven planning workflow.

## Workflows

**Classic pipeline** (structured spec-first):
```
draft.md
  -> /draft-discussion    -> discussion.md (+ discussion-qa.md)
  -> /discussion-analysis -> analysis.md
  -> /analysis-plan       -> plan.md  (review + approve before next step)
  -> /plan-tasks          -> tasks/todo/<prefix>-task-01.md
                             tasks/todo/<prefix>-task-02.md
                             ...
  -> /task-execute        -> implements one task, verifies, moves todo/ -> done/
  -> /task-verify         -> read-only re-check of a task's acceptance criteria
```

**Agile pipeline** (idea-to-vertical-slices):
```
idea
  -> /grill-me            -> grilled-notes.md (idea exploration + codebase grounding)
  -> /to-prd              -> prd.md (user stories + acceptance criteria)
  -> /to-issues           -> tasks/todo/<prefix>-task-01.md (vertical slices)
  -> /tdd                 -> code + tests (red-green-refactor loop, moves todo/ -> done/)
```

Optional, before either pipeline: `/project-principles` -> overview/principles.md (project-wide rules the pipeline reads)

At session end: `/handoff` -> sessions/<name>.md

To start a new project: `/bootstrap-spec-project` -> ~/ai-specs/<project>/

Codebase health check (any time): `/improve-codebase-architecture` -> architecture-report.md

Coding standards (language-specific): `/coding-principles` (generic) or `/java-coding-standards`, `/go-coding-standards`, `/rust-coding-standards`, `/swift-coding-standards`, `/typescript-coding-standards`, `/python-coding-standards`, `/kotlin-coding-standards`

## Skills

| Skill | Input | Output | Stage |
|-------|-------|--------|-------|
| `grill-me` | idea or draft file | grilled-notes.md | Idea Exploration |
| `draft-discussion` | draft.md | discussion.md + discussion-qa.md | Clarification |
| `discussion-analysis` | discussion.md | analysis.md | Analysis |
| `analysis-plan` | analysis.md | plan.md | Planning (approval gate) |
| `to-prd` | grilled-notes or discussion | prd.md | Requirements |
| `plan-tasks` | plan.md | tasks/todo/*.md (one per task) | Decomposition |
| `to-issues` | prd.md | tasks/todo/*.md (vertical slices) | Decomposition |
| `task-execute` | one task file | code + task moved to tasks/done/ | Execution |
| `tdd` | one task file | code + tests, task moved to tasks/done/ | Execution (TDD) |
| `task-verify` | one task file | pass/fail report (read-only) | Verification |
| `handoff` | session state | sessions/*.md | Continuity |
| `project-principles` | project rules | overview/principles.md | Governance |
| `bootstrap-spec-project` | project/feature names | directory tree | Scaffolding |
| `improve-codebase-architecture` | current directory | architecture-report.md | Architecture |
| `coding-principles` | any language | guidelines reference | Code Quality |
| `java-coding-standards` | Java code | guidelines reference | Code Quality |
| `go-coding-standards` | Go code | guidelines reference | Code Quality |
| `rust-coding-standards` | Rust code | guidelines reference | Code Quality |
| `swift-coding-standards` | Swift code | guidelines reference | Code Quality |
| `typescript-coding-standards` | TypeScript code | guidelines reference | Code Quality |
| `python-coding-standards` | Python code | guidelines reference | Code Quality |
| `kotlin-coding-standards` | Kotlin code | guidelines reference | Code Quality |

## Arguments

All skills use short argument names:

| Arg | Stands for | Used by |
|-----|-----------|---------|
| `i` | input / source file | grill-me, draft-discussion, discussion-analysis, analysis-plan, plan-tasks, to-prd, to-issues, task-execute, tdd, task-verify |
| `o` | output file or directory | all writing skills (file; `plan-tasks` and `to-issues` write to a directory) |
| `c` | codebase root (optional, brownfield) | grill-me, discussion-analysis, analysis-plan, to-prd, to-issues, tdd |
| `p` | prefix (task IDs) / project name | plan-tasks (prefix), to-issues (prefix), bootstrap-spec-project (project) |
| `f` | feature name | bootstrap-spec-project |
| `n` | next-session purpose | handoff |

## Example invocations

Classic pipeline:
```
/draft-discussion i=inbox/idea.md o=features/auth/discussion.md

/discussion-analysis i=features/auth/discussion.md o=features/auth/analysis.md

/analysis-plan i=features/auth/analysis.md o=features/auth/plan.md

/plan-tasks i=features/auth/plan.md o=features/auth/tasks/todo/ p=auth

/task-execute i=features/auth/tasks/todo/auth-task-01.md

/task-verify i=features/auth/tasks/done/auth-task-01.md
```

Agile pipeline:
```
/grill-me i=inbox/idea.md o=features/auth/grilled-notes.md

/to-prd i=features/auth/grilled-notes.md o=features/auth/prd.md

/to-issues i=features/auth/prd.md o=features/auth/tasks/todo/ p=auth

/tdd i=features/auth/tasks/todo/auth-task-01.md
```

Other:
```
/handoff o=sessions/2026-05-23-auth.md n="Begin auth-task-02 implementation"

/project-principles o=overview/principles.md

/bootstrap-spec-project p=my-app f=user-auth

/improve-codebase-architecture
```

Brownfield (ground analysis/plan in an existing repo):

```
/discussion-analysis i=features/auth/discussion.md o=features/auth/analysis.md c=/path/to/repo

/analysis-plan i=features/auth/analysis.md o=features/auth/plan.md c=/path/to/repo

/to-prd i=features/auth/grilled-notes.md o=features/auth/prd.md c=/path/to/repo
```

## Install modes

**Personal** (`~/.claude/skills/`): skills available in all Claude Code sessions.

**Project** (`<project>/.claude/skills/`): skills available only within that project directory.

See `INSTALL.md` for exact commands.

## Compatibility

Works in both **Claude Code** and **OpenCode** with no extra steps. OpenCode scans `~/.claude/skills/<name>/SKILL.md` and `.claude/skills/<name>/SKILL.md` natively alongside its own paths. Installing once covers both tools.

## Workflow guide

### Classic pipeline

1. Write a rough idea in `inbox/` or `features/<name>/inbox/` (no structure required). Unscoped ideas go in `backlog/`.
2. `/draft-discussion` - Claude asks 8-12 clarifying questions, then writes `discussion.md`. The questions and your verbatim answers are saved alongside in `discussion-qa.md`, written after each round.
3. `/discussion-analysis` - Claude reads discussion, separates facts from assumptions, writes `analysis.md`.
4. `/analysis-plan` - Claude sequences work, identifies dependencies, writes `plan.md`, then STOPS for your review and approval before `plan-tasks` runs.
5. `/plan-tasks` - Claude decomposes the approved plan into atomic tasks, writes one file per task into `tasks/todo/`.
6. `/task-execute` - Claude implements a single task, verifies its acceptance criteria, and moves the file from `tasks/todo/` to `tasks/done/`. Run once per task.
7. `/task-verify` (optional) - read-only re-check of a task's Given/When/Then against the repo. Useful to audit done work.
8. `/handoff` at session end to write a resumable session document.

Optionally seed `overview/principles.md` first with `/project-principles`. When present, `discussion-analysis`, `analysis-plan`, and `task-execute` read it as binding constraints.

### Agile pipeline

1. `/grill-me` - Claude interrogates your idea with 8-15 grouped questions. Can explore the codebase to answer its own questions. Produces `grilled-notes.md` once all branches are resolved.
2. `/to-prd` - Claude converts grilled notes into a PRD with user stories and Given/When/Then acceptance criteria.
3. `/to-issues` - Claude breaks the PRD into vertical slices (tracer-bullet tasks), each delivering end-to-end user-visible value. Writes task files compatible with the rest of the pipeline.
4. `/tdd` - Claude implements one task using red-green-refactor: confirm interface, write one failing test, write minimum code, refactor, repeat. Moves task to `tasks/done/` when all criteria are covered by passing tests.

### Architecture review

`/improve-codebase-architecture` (no arguments) - runs in the current directory. Identifies shallow modules, scattered concepts, and tight coupling. Produces `architecture-report.md` with evidence-backed candidates and specific proposals. No code changes.

Stages before `task-execute` produce no code: each writes a reviewable file, and `analysis-plan` requires your explicit approval before the plan is decomposed into tasks. `task-execute` is the only skill that writes code, and only for one approved task at a time.

## Project structure (ai-specs)

After running `/bootstrap-spec-project p=my-app f=user-auth`:

```
~/ai-specs/my-app/
  README.md
  overview/                 <- project docs (architecture, decisions, context)
    principles.md           <- project-wide rules read by the pipeline (/project-principles)
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
