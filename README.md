# spec-forge

Skill pack for Claude Code and Opencode implementing a staged, file-driven planning workflow.

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
  -> /code-review         -> (optional) review report (quality, security, performance, spec, tests)
  -> /task-verify         -> (optional) read-only re-check of a task's acceptance criteria
```

**Agile pipeline** (idea-to-vertical-slices):
```
idea
  -> /grill-me            -> grilled-notes.md (idea exploration + codebase grounding)
  -> /to-prd              -> prd.md (user stories + acceptance criteria)
  -> /to-issues           -> tasks/todo/<prefix>-task-01.md (vertical slices)
  -> /tdd                 -> code + tests (red-green-refactor loop, moves todo/ -> done/)
  -> /code-review         -> (optional) review report (quality, security, performance, spec, tests)
```

Optional, before either pipeline: `/project-principles` -> overview/principles.md (project-wide rules the pipeline reads)

At session end: `/handoff` -> sessions/<name>.md

To start a new project: `/bootstrap-spec-project` -> ~/ai-specs/<project>/

**Full orchestration** (automated pipeline):
```
/orchestrate i=<input> o=<output-dir>
  -> asks which pipeline (Classic or Agile)
  -> chains all skills in sequence
  -> stops at approval gate (Classic: analysis-plan)
  -> auto-retries code-review failures (max 2)
  -> produces final summary
```

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
| `code-review` | one task file | review report (read-only) | Review |
| `task-verify` | one task file | pass/fail report (read-only) | Verification |
| `handoff` | session state | sessions/*.md | Continuity |
| `project-principles` | project rules | overview/principles.md | Governance |
| `bootstrap-spec-project` | project/feature names | directory tree | Scaffolding |
| `improve-codebase-architecture` | current directory | architecture-report.md | Architecture |
| `orchestrate` | input file + output dir | full pipeline execution | Orchestration |
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
| `i` | input / source file | grill-me, draft-discussion, discussion-analysis, analysis-plan, plan-tasks, to-prd, to-issues, task-execute, tdd, code-review, task-verify |
| `o` | output file or directory | all writing skills (file; `plan-tasks` and `to-issues` write to a directory) |
| `c` | codebase root (optional, brownfield) | grill-me, discussion-analysis, analysis-plan, to-prd, to-issues, tdd, code-review |
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

/code-review i=features/auth/tasks/done/auth-task-01.md

/task-verify i=features/auth/tasks/done/auth-task-01.md
```

Agile pipeline:
```
/grill-me i=inbox/idea.md o=features/auth/grilled-notes.md

/to-prd i=features/auth/grilled-notes.md o=features/auth/prd.md

/to-issues i=features/auth/prd.md o=features/auth/tasks/todo/ p=auth

/tdd i=features/auth/tasks/todo/auth-task-01.md

/code-review i=features/auth/tasks/done/auth-task-01.md
```

Other:
```
/orchestrate i=inbox/idea.md o=features/auth/

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

**Primary support: Claude Code and OpenCode**

These skills are designed for **Claude Code** and **OpenCode**. Both tools natively scan `~/.claude/skills/<name>/SKILL.md` and `.claude/skills/<name>/SKILL.md`, so installing once covers both. The skills use tool-specific features like automatic invocation (`/skill-name`) and argument parsing (`i=`, `o=`, `c=`).

**Other AI agents**

The core skill content (procedures, rules, templates) is written in standard Markdown and can be used with other AI coding agents (Cursor, Codex, Windsurf, Aider, etc.) by manually referencing the skill files. These tools don't have built-in skill systems, so you'll need to:

1. Include the skill files in your repo or reference them by path
2. Manually invoke them in prompts (e.g., "Read `skills/grill-me.md` and follow its procedure")
3. Provide context and arguments manually instead of using the `i=`, `o=` syntax

The skills will work, but without the automatic invocation and argument handling that Claude Code/OpenCode provide.

## Workflow guide

### Full orchestration

`/orchestrate` runs the entire pipeline from idea to verified tasks. It:
1. Asks which pipeline (Classic or Agile) and gathers inputs
2. Asks whether to enable code-review and task-verify (both optional, default: off)
3. Chains skills in sequence, passing outputs between them
4. Stops at the approval gate (Classic: `analysis-plan` review)
5. Executes tasks one by one, optionally running `code-review` after each
6. Auto-retries failed reviews up to 2 times, feeding findings back to `task-execute`
7. Optionally runs `task-verify` after each task
8. Produces a final summary with all artifacts and their paths

Use `/orchestrate` when you want to run the full pipeline without manually invoking each skill. You still control the process at approval gates and can stop at any time.

### Classic pipeline

1. Write a rough idea in `inbox/` or `features/<name>/inbox/` (no structure required). Unscoped ideas go in `backlog/`.
2. `/draft-discussion` - Claude asks 8-12 clarifying questions, then writes `discussion.md`. The questions and your verbatim answers are saved alongside in `discussion-qa.md`, written after each round.
3. `/discussion-analysis` - Claude reads discussion, separates facts from assumptions, writes `analysis.md`.
4. `/analysis-plan` - Claude sequences work, identifies dependencies, writes `plan.md`, then STOPS for your review and approval before `plan-tasks` runs.
5. `/plan-tasks` - Claude decomposes the approved plan into atomic tasks, writes one file per task into `tasks/todo/`.
6. `/task-execute` - Claude implements a single task, verifies its acceptance criteria, and moves the file from `tasks/todo/` to `tasks/done/`. Run once per task.
7. `/code-review` (optional) - Claude reviews the code changes for quality, security, performance, spec compliance, and test quality. Produces a report with findings by severity. Read-only.
8. `/task-verify` (optional) - read-only re-check of a task's Given/When/Then against the repo. Useful to audit done work.
9. `/handoff` at session end to write a resumable session document.

Optionally seed `overview/principles.md` first with `/project-principles`. When present, `discussion-analysis`, `analysis-plan`, and `task-execute` read it as binding constraints.

### Agile pipeline

1. `/grill-me` - Claude interrogates your idea with 8-15 grouped questions. Can explore the codebase to answer its own questions. Produces `grilled-notes.md` once all branches are resolved.
2. `/to-prd` - Claude converts grilled notes into a PRD with user stories and Given/When/Then acceptance criteria.
3. `/to-issues` - Claude breaks the PRD into vertical slices (tracer-bullet tasks), each delivering end-to-end user-visible value. Writes task files compatible with the rest of the pipeline.
4. `/tdd` - Claude implements one task using red-green-refactor: confirm interface, write one failing test, write minimum code, refactor, repeat. Moves task to `tasks/done/` when all criteria are covered by passing tests.
5. `/code-review` (optional) - Claude reviews the code changes for quality, security, performance, spec compliance, and test quality. Produces a report with findings by severity. Read-only.

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
    todo/                   <- tasks that need to be implemented
    done/
  features/
    user-auth/
      inbox/
      tasks/
        todo/               <- task files (user-auth-task-01.md, ...)
        done/
      sessions/             <- feature level sessions
  prompts/                  <- custom prompts you might need to use later
  sessions/                 <- app level sessions
```
